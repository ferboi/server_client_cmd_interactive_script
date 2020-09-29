import sys
import socket
import getopt
import threading
import subprocess
import pdb
import optparse
import select

# define some global variables
listen = False
command = False
upload = False
target_boolean = False
execute = ""
target = ''
upload_destination = ""
port = 0
Port = False

def usage():
    print("BHP Net Tool")
    print()
    print('There two modes that can be used in this script. 1. Listening mode(server mode), 2. Client mode')
    print('In the client mode you can: \n1. Execute command against a server. \n2. Create a cmd shell with a computer server. \n3. Upload a file to a computer.')
    print('In the listening mode you communicate with a client by receiving input and sending output.')
    print('Options used by this script are "-l, -t, -p, -e, -u, -c"')
    print()
    print('[*]Note: The -l option must be used along side -e, -u, and -c options for them to work.')
    print('[*]Note: The -l option is a requirement to enter listening mode.')
    print('[*]Note: If you do not specify the port for listening mode port 9999 is used by default')
    print('[*]Note: The -l option should not be used with -t option; therefore it cannot be used with -e, -u and -c options')
    print('[*]Note: To enter the client mode, the -t and -p options are requirements')
    print('[*]Note: If you want to make use of the -e option make it the last option entered along with the command wih spacing where required.')
    print()
    print("-l - listen on [host]:[port] for incoming connections. [*]Usage: -l")
    print("-e --execute=command_to_run - execute the given command upon receiving a connection. [*]Usage: -e command")
    print("-c - initialize a command shell. [*]Usage: -c")
    print("-u --upload=destination - upon receiving connection upload a file and write to [destination]. [*]Usage: -u [upload_location]")
    print()
    print("How to execute server mode: ")
    print("python interactive_script.py -l -p [port_num]")
    print()
    print('Execution examples for client mode: ')
    print("python interactive_script.py -t [ip_address] -p [port_num] -u C:\\Users\\user\\Documents\\text.txt")
    print("python interactive_script.py -t [ip_address] -e cat /etc/passwd")
    print("python interactive_script.py -t [ip_address] -c") 
    

    sys.exit()

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    global upload
    global Port
    global target_boolean
    
    
    execute_counter = 0
    # -l -e -c -u -p -t

    print('Please if you make use of the -e option; make sure that it is the last one enterd along with its arguments.')
    print()

    if len(sys.argv[1:]):
        argumentlist = sys.argv[1:]
        if '-l' in argumentlist and '-t' in argumentlist:
            usage()
            exit()
            
        
        if '-l' in argumentlist:
            listen = True
            print('You have entered listening mode, The server created listens for commands from clients and responds to them.\n')

        for word in argumentlist:
            if '-t' in word:
                target_boolean = True
                print('You have entered client mode, Here you can use a shell with a server or send a command to a server.\n')
                continue
            if target_boolean:
                target = word
                break

        if '-c' in argumentlist:
            command = True

        for word in argumentlist:
            if '-u' in word:
                upload = True
                continue
            if upload:
                upload_destination = word
                break

        if '-p' in argumentlist:
            for word in argumentlist:
                if '-p' in word:
                    Port = True
                    continue    
                if Port:
                    port = int(word)
                    break
        else:
            port = 9999

        for word in argumentlist:
            if '-e' in word:
                execute_counter += 1
                continue
            if execute_counter == 1:
                execute += ' '
                execute += word
                    


    else:
        usage()
        print('Exception')
        exit()
    
    # read the commandline options
    

    # are we going to listen or just send data from stdin?
    if target_boolean and port:
        # connect to server and send data
        client_sender()

    #Next we are going to listen and potentially upload things, execute commands, and drop shell back
    #depending on our command line options above
    if listen:
        server_loop()

def client_sender():
    global target
    global port
    global upload
    global execute
    global command
    global upload_destination

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # If shell execution is true
    if command:
        client.connect((target, port))
        try:
            while True:
                # show a simple prompt
                cmd = input("<BHP:#> ")
                if cmd == 'quit':
                    client.close()
                    print('[*]Connection Closed. Exiting...')
                    exit()
                if len(str.encode(cmd)) > 0:
                    # send command
                    client.send(str.encode(cmd))
                final_data = ''
                while True:
                    data = str(client.recv(4069), 'utf-8')
                    final_data += data
                    if len(data) <= 4069:
                        break
                print(final_data)
                print()
        except:
            print("[*]Exception! Exiting.")
            print("[*]Check your server instance for more information.")
            client.close()
            # Tear down the connection


    # check for command exection
    if execute:
        # run the command

        try:
            # connect to our target host
            client.connect((target, port))
            print('[+]Connection Established...')

            client.send(execute.encode())
            
            #now wait  = 1
            final_data = ''
            while True:
                data = str(client.recv(4069), 'utf-8')
                final_data += data
                if len(data) <= 4069:
                    break
            print(final_data)
            client.close()

        except:
            print("[*]Exception! Exiting.")
            print("[*]Check your server instance for more information.")
            client.close()
            # Tear down the connection
    
    # now we go into another loop if a command shell was requested
    # if upload:
    #     # read in all of the bytes and write to our destination
    #     file_buffer = ""

    #     # keep reading data until none is available
    #     while True:
    #         data = client_socket.recv(1024)

    #         if not data:
    #             break
    #         else:
    #             file_buffer += data
        
    #     # now we take these bytes and try to write them out
    #     try:
    #         file_descriptor = open(upload_destination, "wb")
    #         file_descriptor.write(file_buffer)
    #         file_descriptor.close()

    #         # acknowledge that we wrote the file out
    #         client_socket.send("successfully saved file to %s\n" %upload_destination)
    #     except:
    #         client_socket.send("Failed to save file to %s\n" %upload_destination)




def server_loop():
    # We listen on all interfaces
    global port
    target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(1)
    
    #while True:
    client_socket, addr = server.accept()
    if client_socket:
        print('[+]A client has connected...')
        client_handler(client_socket, addr)
        # spin off a thread to handle our new client
        #client_thread = threading.Thread(target=client_handler, args=(client_socket, addr))
        #client_thread.start()



def run_command(command):
    # trim the newline
    command = command.rstrip()

    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to exectue command.\r\n"
    
    # send the output back tot he client
    return output

def client_handler(client_socket, addr):
    while True:
        data = str(client_socket.recv(1024), 'utf-8')
        output = run_command(data)
        try:
            client_socket.send(output)
        except:
            client_socket.send(output.encode())
        print('[+]Replied to client: ' + addr[0])






        
main()