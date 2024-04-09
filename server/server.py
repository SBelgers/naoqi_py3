from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import timeit
import re
from nao_nocv_server import Robot


def delay_test(**kwargs):
    client_time = kwargs.get("time")
    server_time = timeit.default_timer()
    delay = client_time - server_time
    return "Delay: {delay} ns".format(delay=delay)


def kwarg_test(**kwargs):
    return "arguments: {kwargs}".format(kwargs=kwargs)


def dict_to_utf8(dictionary):
    def encode_dict_to_utf8(d):
        encoded_dict = {}
        for k, v in d.items():
            if isinstance(k, unicode):
                k = k.encode("utf-8")
            if isinstance(v, unicode):
                v = v.encode("utf-8")
            elif isinstance(v, dict):
                v = encode_dict_to_utf8(v)
            encoded_dict[k] = v
        return encoded_dict

    encoded_dict = encode_dict_to_utf8(dictionary)
    return encoded_dict


class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        try:
            try:
                parsed_data = json.loads(post_data)
            except ValueError:
                self.send_error(400, "Invalid JSON format")
                return
            parsed_data = dict_to_utf8(parsed_data)
            function_name = parsed_data.get("function", "")
            kwargs = parsed_data.get("kwargs", {})

            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", function_name):
                self.send_error(400, "Invalid function name")
                return

            print("Function:", function_name, "kwargs:", kwargs)
            if hasattr(self.server.robot, function_name) and callable(
                getattr(self.server.robot, function_name)
            ):
                function = getattr(self.server.robot, function_name)
                print("running function: ", function)
                try:
                    response = function(**kwargs)
                except Exception as e:
                    response = {"status": "serverError", "message": str(e)}
            else:
                response = {
                    "status": "serverError",
                    "message": "Function not found",
                }
            if response["status"] == "success":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response))
            else:
                self.send_error(500, json.dumps(response))
        except Exception as e:
            response = {"status": "serverError", "message": str(e)}
            self.send_error(500, json.dumps(response))
            print("Error:", response)


class MyHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.robot = None


def run_server():
    server_address = ("", 8000)
    with Robot("nao", "192.168.0.103", 9559) as robot:
        httpd = MyHTTPServer(server_address, MyServer)
        httpd.robot = robot
        print("Server running on port 8000")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    run_server()
