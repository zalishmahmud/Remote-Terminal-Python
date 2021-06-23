# Remote-Terminal-Python
This is a Python project based on firebase (pyrebase) RealTime Database to Remotely accessing Device Terminal without any port forwarding or Public IP.


## information

#### Fill up the firebase Configuration for both Host.py and client.py files
![Firebase Configuration](https://github.com/zalishmahmud/Remote-Terminal-Python/blob/main/images/firebaseConfig.jpg?raw=true)


#### DataBase Information:
![structe of firebase database](https://github.com/zalishmahmud/Remote-Terminal-Python/blob/main/images/databaseStructure.jpg?raw=true)

#### Add Device Name ( at client.py) from database information as follow:
![Firebase Configuration](https://github.com/zalishmahmud/Remote-Terminal-Python/blob/main/images/clientDevice.jpg?raw=true)


## Commands:

### Any Device Specific command can be executed as it's based on Subprocess Library.

### Built in Commands:
```
upload <filename>  to upload file from client to Host device.

download <filename> to download file from host device to client.

status              to check host connected or not.

exit                to stop both host and client file executions.
```

