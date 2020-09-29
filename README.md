# server_client_cmd_interactive_script

This python script can operate in either client or server mode.

In client mode you can perform 3 functions:
1. Send a command to the server running on the target machine.
2. Create an interactive terminal session with the server on the target machine.
3. Upload a file to the server on the target machine. (This has not being tested explicitly).

In server mode it's sole function is to respond to any request from a client.

Note: The script can only be run in one of the two modes which are client or server mode. When the server instance is started on the machine you want to connect to, you can then run it as a client on your own machine.

Information on how to make use of the script would be printed to you when you try to run it.
