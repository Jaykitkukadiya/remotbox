import socket
import subprocess
import sys
import os
import tqdm
import mouse

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.105",9999))

print(s.recv(200).decode('ebcdic_cp_nl') , end="")
s.send(input().encode('ebcdic_cp_nl'))   # this is take password and send to server
mess,flag = s.recv(700).decode('ebcdic_cp_nl').split("^")   # receve a home path and flag(wether password is right or not)
print(mess , end="")

if int(flag) == 1: #if home path is right then further we can enter command
    def sendcmd(conn):
        while True:

            command = input()  #take command from user to be execute

            if command != "":   # if command is not empty then can send to server else loop will continue
                conn.send(command.encode('ebcdic_cp_nl'))  #send command to server so server can identify which code is execute like if command is cpythis,keybordmode,mousemode then execute server appropriatly else normal execution by server
                if(command == "quit" or command == "quitboth"):  # if command is quit then loop is break and also this command send first to server so server has also break execution of their main loop
                    break
                
                elif command[:7] == "cpythis": # if command is cpythis(this is userdefine command) then execute its block
                    filename , filesize = str(conn.recv(1024).decode('ebcdic_cp_nl')).split("^") # receve file name and size of file which we will selected so we can understand how many times we execute loop and name is requir for make new file of this name
                    print(filesize)
                    filesize = int(filesize) # filesize is string so there must be convert into int
                    receved_size = 0 # this is flag generally used for how many byte receve by server out of filesize
                    with open(filename , "wb") as f: #this code open file in binary write mode or create new file and then open ( binary mode only allow us to write binary data not a string)
                        while receved_size < filesize: # when receve size is eq to file size then loop is break
                            bytes_read = conn.recv(20480) #receve byte from server
                            f.write(bytes_read) #hear no need to decode coz it already in byte form
                            receved_size += len(bytes_read) # incress receved size by byteread
                    print("file recived successful")  # print message while loop is break means file is successful transfer

                elif command[:2] == "km":      # if command is keybordmode(this is userdefine command) then execute its block
                    print("keybord mode> ")     
                    while True:
                        word = input()  # take input string which we wants to write
                        conn.send(word.encode('ebcdic_cp_nl'))    #send string to server
                        if word == "off":   # if word is off then loop is break but also doing this this string sent to server so server can also off their loop of this block
                            break
                    rec = conn.recv(500)  # this is receve a current path of servers dir
                    print("\n\n" + rec.decode('ebcdic_cp_nl') ,end="")
                elif command[:2] == "mm":    # if command is mousemode(this is userdefine command) then execute its block
                    print("mouse mode > ")
                    while True:
                        # mouse_command = input()      # take input string which we wants to write like cord = x_pos*y_pos , click left = cl , click right = cr , click middel = cm
                        mouse_command = mouse.get_position()      # take input string which we wants to write like cord = x_pos*y_pos , click left = cl , click right = cr , click middel = cm
                        conn.send(mouse_command.encode('ebcdic_cp_nl'))       #send this command to server
                        if mouse_command == "off" or mouse_command == "err":      # if mouse_command is off then loop is break but also doing this this string sent to server so server can also off their loop of this block
                            break
                    rec = conn.recv(500)        #this is receve a current path of servers dir
                    print("\n\n" + rec.decode('ebcdic_cp_nl') ,end="")
                else:
                    rec = conn.recv(100000)     # if code is not above then it is default run on cmd then receve to server
                    print("\n\n" + rec.decode('ebcdic_cp_nl') ,end="")
    sendcmd(s)  

    s.close()
else:
    s.close()