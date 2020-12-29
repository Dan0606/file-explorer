import socket
import os
HOST = '127.0.0.1'
PORT = 52472 

def show_files(s):
    path = s.recv(1024).decode()
    try:
        allFiles = os.listdir(path)
        s.send("FILE EXISTS".encode())
    except FileNotFoundError:
        s.send("FILE DOESNT EXISTS".encode())
        show_files(s)
    except PermissionError:
        s.send("ACCESS DENIED".encode())
        show_files(s)
    allFilesWithType = []
    for i in allFiles: 
        if os.path.isfile(path + i):
            allFilesWithType.append(i + "-file")
        else:
            allFilesWithType.append(i + "-folder")
    strAllFilesWithType = (";".join(allFilesWithType))
    allFilesWithTypeLength = len(strAllFilesWithType)
    s.send(str(allFilesWithTypeLength).encode())
    startSending = s.recv(1024).decode()
    if startSending == "YES":
        s.send(strAllFilesWithType.encode())
    keepGo = s.recv(1024).decode()
    if keepGo != "EXIT":
        show_files(s)

                

        """keepGo = input("keep going? ")
        if keepGo.lower() == "no":
            break
        elif keepGo.split(" ")[0].lower() == "dir":
            currentPath += keepGo.split(" ")[1] + "\\"
            show_files(s, currentPath)
        elif keepGo.lower() == "back":
            currentPathAllPath = currentPath.split("\\")
            currentPath = ""
            pathToDisapear = currentPathAllPath[-2]
            print(pathToDisapear)
            for path in currentPathAllPath:
                if path != pathToDisapear:
                    currentPath += path + "\\"
            print(currentPath)
            show_files(s, currentPath)
        else:
            print("unvalid input, if you want to quit type no")"""


def send_file(s):
    path = s.recv(1024).decode()
    f1 = open(path, "rb")
    fileBinaryText = f1.read()
    filesize = str(len(fileBinaryText))
    while len(filesize) < 10:
        filesize = "0" + filesize
    s.send(filesize.encode())
    s.send(fileBinaryText)
    f1.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.recv(1024).decode()
    s.send("HELLO".encode())
    whatToDo = s.recv(1024).decode()
    if whatToDo == "DIR":
        show_files(s)
    s.close()
    

main()

