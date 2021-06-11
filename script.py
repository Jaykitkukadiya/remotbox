import os
import socket
import subprocess
import sys
import os
import tqdm
import mouse
import time
# from com.chaquo.python import python

conn = None

def main(password):
    try:
        # os.chdir("/storage/emulated/0/download/")
        # filedir = str(python.getPlatform().getApplication().getFilesDir())
        # filename = os.path.join(os.path.dirname(__file__) , "passwordx.txt")
        # with open(filename , 'w' , encoding='utf8' ,errors="ignore") as f:
        #     f.write("this is password")
        # with open(filename , 'r' , encoding='utf8' ,errors="ignore") as f:
        #     data = f.read().lower()

        global conn
        passw = str(password)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.43.242",9999))

        print(s.recv(200).decode('ebcdic_cp_nl') , end="")
        s.send(passw.encode('ebcdic_cp_nl'))   # this is take password and send to server
        mess,flag = s.recv(700).decode('ebcdic_cp_nl').split("^")   # receve a home path and flag(wether password is right or not)
        print(mess , end="")
        if int(flag) == 1:
            conn = s
            return 1
        else:
            s.close()
            return 0

    
    except Exception as e:
        return f"some error : {e}"

def update(strg):
    global conn
    # try:
        # return str(str(strg) + "this is tested ************")
    command = str(strg)  #take command from user to be execute

    if command != "":   # if command is not empty then can send to server else loop will continue
        conn.send(command.encode('ebcdic_cp_nl'))  #send command to server so server can identify which code is execute like if command is cpythis,keybordmode,mousemode then execute server appropriatly else normal execution by server
        print("sended")
        if(command == "quit"):  # if command is quit then loop is break and also this command send first to server so server has also break execution of their main loop
            conn.close()
            return "closed"
        
        elif command[:7] == "cpythis": # if command is cpythis(this is userdefine command) then execute its block
            start_time = time.time()
            fname , filesize = str(conn.recv(1024).decode('ebcdic_cp_nl')).split("^") # receve file name and size of file which we will selected so we can understand how many times we execute loop and name is requir for make new file of this name
            print(filesize)
            filename = os.path.join("/storage/emulated/0/Download" , fname)
            # print(os.path.dirname(file))
            filesize = int(filesize) # filesize is string so there must be convert into int
            receved_size = 0 # this is flag generally used for how many byte receve by server out of filesize
            with open(filename , "wb") as f: #this code open file in binary write mode or create new file and then open ( binary mode only allow us to write binary data not a string)
                while receved_size < filesize :# when receve size is eq to file size then loop is break
                    bytes_read = conn.recv(1024) #receve byte from server
                    f.write(bytes_read) #hear no need to decode coz it already in byte form
                    receved_size += len(bytes_read) # incress receved size by byteread
            return f"file received successfully \nname:{fname}\nsize:{filesize}\npath:Internal storage/Download/...\ntotle time:{time.time() - start_time} secound \n " # print message while loop is break means file is successful transfer

        else:
            rec = conn.recv(100000)     # if code is not above then it is default run on cmd then receve to server
            return "\n\n" + rec.decode('ebcdic_cp_nl')

    # except Exception as e:
    #     return f"some error : {e}"

   

