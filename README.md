Still WIP

Two-part control system for Aldebran Nao robots using Python 2.7. 

As of now, very easy to exploit.

Part 1: Server
Python code to run a HTTP server. Requires Python 2.7.x and Aldebran Naoqi.
Receives POST-requests with {'function': $function_name, 'kwargs': {'arg1': $arg1, ...}}. 

If the specified function is valid, it runs it with the keyword arguments.

Part 2: Client
Connects to the Server, and send POST-Requests. 
Contains functions for ease of use, although this is not strictly needed.

