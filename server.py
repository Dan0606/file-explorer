import socket
HOST = '127.0.0.1'
PORT = 52472 

def download_file(s, client, path):
    client.send(path.encode())
    resp = client.recv(10).decode()
    filesize = int(resp)
    data = s.recv(filesize)
    while len(data) < filesize:
        print("downloading..." + str(len(data)/filesize*100) + "%")
        data += s.recv(filesize - len(data))
    destFilePath = "C:\\temp\\"
    f2 = open(destFilePath, "wb")
    f2.write(data)
    f2.close()


def get_files(s, client, path):
    while True:
        client.send(path.encode())
        isFileExists = client.recv(1024).decode()
        while isFileExists != "FILE EXISTS":
            if isFileExists == "FILE DOESNT EXISTS":
                print("folder doesnt exists.")
            elif isFileExists == "ACCESS DENIED":
                print("access to the folder denied.")
            path = deletePathLastElement(path)
            addToPath = input("choose folder from the folders above\n--->>> ")
            path += addToPath + "\\"
            get_files(s, client, path)
        folderLength = int(client.recv(1024).decode())
        client.send("YES".encode())
        data = ""
        while len(data) < folderLength:
            data += client.recv(1024).decode()
        allFiles = data.split(";")
        for f in allFiles:
            if f == "":
                print("file is empty")
            else:
                print(f)
        keepGo = input("Keep Go? ").lower()
        while keepGo != "yes" and keepGo != "no":
            keepGo = input("you have to choose yes or no -> ")
        if keepGo == "no":
            client.send("EXIT".encode())
            print("leaving...")
            break
        elif keepGo == "yes":
            folderOrBack = input("folder name to enter the folder\nback to go to the previous folder\ndown + file name to download specific file\n--->>>  ")
            if folderOrBack.lower() == "back":
                path = deletePathLastElement(path) 
            elif folderOrBack.lower().split(" ")[0] == "down":
                print("started")
                download_file(s, client, path + folderOrBack.split(" ")[1] + "\\")    
                print("finished")
            else:
                path += folderOrBack + "\\"
            client.send("KEEP GO".encode())  
         


def deletePathLastElement(path):
    splitPath = path.split("\\")
    splitPath.pop(-1)
    backPath = ""
    for path in splitPath:
        if splitPath.index(path) != len(splitPath) - 1:
            backPath += path + "\\"
    return backPath    


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # create TCP socket
    s.bind((HOST, PORT)) 
    s.listen() # open the socket for client connections
    print("waiting for clients...")
    client_connection1, _ = s.accept() 
    client_connection1.send("HELLO".encode())
    client_connection1.recv(1024).decode()
    whatToDo = input("command - ")
    if whatToDo.lower() == "dir":
        client_connection1.send("DIR".encode())
        get_files(s, client_connection1, "C:\\")

    
        
    s.close()

main()
