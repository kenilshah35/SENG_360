# Secure Chat Application

## Seng 360 - Assignment 3

### Group 7 - Ella Kuypers, Kenil Shah, Roy Li

A simple chatroom application that supports multiple users via a server/client model with threading.

**Demo Video:** <https://www.youtube.com/watch?v=0ralYvtiRK4>


## Features

1. Secure login process(key exchange).
2. Login system with account locking, sign-up, delete.
3. Online user list display.
4. Docker MySQL DB container for storing credentials.

## Setup Instructions

1. Start the docker container for the login credentials database using the following commands:

        docker-compose build
        docker-compose up

## Server Instructions

1. Start the chat server by running:

        python3 server.py

## Client Instructions

1. To start a chat client, open a new terminal window and run the following command:

        python3 client.py

## Credentials Database

Credentials for the login system are stored on a My SQL database hosted on a docker container. To access the database do the following:

1. Identify the id of the container by listing the running containers

        docker ps

2. Run the following command with the container id.

        docker exec -t <container-id> bash

3. Once logged into the container run the following command to access the database:

        mysql --user=root --password=pumpkin dev

If you'd like to add users automatically upon building the container edit the *init.sql* file and add INSERT commands for the credentials table **before** building the container.

If you'd like to do a complete reset of the docker setup use the following guide: <https://docs.tibco.com/pub/mash-local/4.1.1/doc/html/docker/GUID-BD850566-5B79-4915-987E-430FC38DAAE4.html>

## References

A list of the sources used to guide our implementation.

### Client/Server

- <https://hackernoon.com/a-simple-guide-to-building-chat-applications-in-python-q5633t1c>
- <https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170>
- <https://www.youtube.com/watch?v=3QiPPX-KeSc>

### Key Exchange

- <https://medium.com/@sadatnazrul/diffie-hellman-key-exchange-explained-python-8d67c378701c>

### Docker MySQL Database

- <https://docs.docker.com/language/python/develop/>
