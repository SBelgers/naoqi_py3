try:
    import naoqi
except:
    print("Error importing naoqi")
    pass
import timeit


class Robot:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

    def __enter__(self):
        self.connect_proxies()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect_proxies()

    def delay_test(self, client_time):
        server_time = timeit.default_timer()
        delay = client_time - server_time
        response = {"status": "success", "delay": delay}
        return response

    def kwarg_test(**kwargs):
        return "arguments: {kwargs}".format(kwargs=kwargs)

    def connect_proxies(self):
        def connect_single_proxy(proxy_name):
            try:
                proxy = naoqi.ALProxy(proxy_name, self.ip, self.port)
                return proxy
            except Exception as e:
                print(
                    "Error connecting to {proxy_name}: {e}".format(
                        proxy_name=proxy_name, e=e
                    )
                )
                return None

        self.proxies = {
            "ALTextToSpeech": "unset",
            "ALSonar": "unset",
            "ALLeds": "unset",
        }
        for name, proxy in self.proxies.items():
            self.proxies[name] = connect_single_proxy(name)

    def disconnect_proxies(self):
        def disconnect_single_proxy(proxy, name):
            try:
                proxy._close()
                return True
            except Exception as e:
                print(
                    "Error disconnecting from '{name}' ({proxy}): {e}".format(
                        proxy=proxy, name=name, e=e
                    )
                )
                return False

        for name, proxy in self.proxies.items():
            disconnect_single_proxy(proxy, name)

    def Say(self, text, POST=True):
        response = {}
        try:
            if POST:
                self.proxies["ALTextToSpeech"].post.say(text)
                response["status"] = "success"
            elif not POST:
                self.proxies["ALTextToSpeech"].say(text)
                response["status"] = "success"
        except Exception as e:
            response["status"] = "nao_nocvError"
            response["message"] = str(e)
        return response


if __name__ == "__main__":
    with Robot("nao", "192.168.0.103", 9559) as robot:
        print("Say", robot.Say("Hello, world!"))
        print("EyeLed", robot.EyeLed([255, 0, 0], 0.5))
