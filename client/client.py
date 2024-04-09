import requests
import timeit


class Client:
    def __init__(self, url: str) -> None:
        self.url = url

    def post_request(self, function: str, **kwargs) -> str:
        data = {"function": function, "kwargs": kwargs}
        print(data)
        response = requests.post(self.url, json=data)
        print(response)
        if response.status_code != 200:
            raise Exception(
                "POST request failed with status code:", response.status_code
            )
        return response.content.decode("utf-8")

    def _delay_test(self) -> str:
        return self.post_request(
            "delay_test", client_time=timeit.default_timer()
        )

    def _kwarg_test(self, **kwargs) -> str:
        return self.post_request("kwarg_test", **kwargs)

    def Say(self, text: str, POST: bool = True) -> str:
        """Make the robot say something

        Args:
            text (str): Text to say.
            POST (bool, optional): Legacy option. Unsure what it does.

        Returns:
            str: response code
        """

        return self.post_request("Say", text=text, POST=POST)


if __name__ == "__main__":
    url = "http://192.168.43.132:8000"
    robot = Client(url)
    print(robot.Say(text="Hello simon!"))
    print(robot._delay_test())
