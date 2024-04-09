from client import Client

if __name__ == "__main__":
    url = "http://localhost:8000"
    client = Client(url)
    print(client._test_function())
    print(client._delay_test())
    print(client._kwarg_test("arg1", "arg2", "arg3"))
