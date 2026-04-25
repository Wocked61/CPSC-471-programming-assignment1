# CPSC-471-programming-assignment1
Names and Emails:
- Dylan Phan - DylanP@csu.fullerton.edu
- Logan Arroyo - 
- Vincent Nguyen - nguyenvincent04@csu.fullerton.edu 


  Goals:

To understand the challenges of protocol
To discover and appreciate the challenges of developing complex, real-world network
Make sense of real-world sockets programming
To utilize a sockets programming API to construct simpliﬁed FTP server and client
SUBMISSION GUIDELINES:
This assignment may be completed using C++, Java, or Python.
Please hand in your source code electronically (do not submit .o or executable code) through Canvas. You must make sure that this code compiles and runs correctly.
•  Only one person within each group should submit.

Write a README ﬁle (text ﬁle, do not submit a .doc ﬁle) which contains
Names and email addresses of all
The programming language you use (e.g. C++, Java, or Python)
How to execute your
Anything special about your submission that we should take note
Place all your ﬁles under one directory with a unique name (such as p1-[userid] for assignment 1, g. p1-ytian1).
Tar the contents of this directory using the following command(Linux). tar cvf [directory_ name].tar [directory_name] g. tar -cvf p1-ytian1.tar p1- ytian1/
Use CANVAS to upload the tared ﬁle you created
 

Grading Guideline:
Protocol design 10’
Program compiles: 5’
Correct get command: 25’
Correct put command: 25’
Correct ls command: 10’
Correct format: 5’
Correct use of the two connections: 15’
README ﬁle included: 5’
Late submissions shall be penalized 10%. No assignments shall be accepted after 24
 

For the project, each of you please do study as follows:

 

Study the related contents about File Transfer Protocol (FTP)
Study socket programming 
Study the FTP related system calls in the language you chose 
Refer to the sample code and start your own design 
 

Resources about socket programming: 
 

Socket Programming in C/C++
https://www.geeksforgeeks.org/socket-programming-cc/Links to an external site.

 

Socket Programming in Java
https://www.geeksforgeeks.org/socket-programming-in-java/Links to an external site.

 

Socket Programming in Python
https://www.geeksforgeeks.org/socket-programming-python/


Programming Language: Python

How to Execute:
  Start the server:
    python server.py <port>
    Example: python server.py 1234

  Start the client (in a separate terminal):
    python Cli.py <server_host> <server_port>
    Example: python Cli.py localhost 1234

  Client commands:
    ftp> ls               (list files on server)
    ftp> get <filename>   (download file from server)
    ftp> put <filename>   (upload file to server)
    ftp> quit             (disconnect)

Special Notes:
- Two TCP connections are used per session: a persistent control
  channel for commands and a data channel opened and closed per
  transfer.
- The client picks an ephemeral port for each data transfer and
  sends it to the server as part of the command.
- Tested on Windows using Python 3.
