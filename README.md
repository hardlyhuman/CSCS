# CSCS

## Overall Objective

Implements architecture and design of a network based machine statistics collection system.

## Functional Requirements

The system allows collection of machine statistics in an intranet environment. The system implements the
following specifications.
### Client Script
1. This script will be uploaded and executed to 100s of machines in the intranet. These machines are meant to be monitored for system level statistics like memory usage, CPU usage, total uptime and windows security event logs (in case of windows OS).
2. When executed, the client script collects the statistics and return them to the server script for cumulation.
3. The client script must encrypt the data before returning it to server.
### Server Script
1. Installed on a single central machine in the same intranet.
2. Each client is configured in a server config xml file something like this
	
	`<client ip=’127.0.0.1’ port=’22’ username=’username’ password=’password’ mail="asa@asda.com">
		<alert type="memory" limit="50%" />
		<alert type="cpu" limit="20%" />
	</client>`
3. Email configurations for the sender are configured in a server email_config json file which is something like this
	`
4. When executed, the server script should connect to each client using ssh, upload the client script in a temp directory, execute it and get the response.
5. After receiving the response from the client script, server script should decode it and stores it into a relational database along with client ip. This collected data is consumed by another application, that is out of scope, but you may design the database table yourself.
6. The server based upon the "alert" configuration of each client sends a mail notification. The notification is sent to the client configured email address using SMTP. Use a simple text mail format with some detail about the alert. event logs must be sent via email every time without any condition.

## Other Technical and Non-functional Requirements

- Paramiko has been used for ssh communication.
- Win32api has been used for statistics.
- SMTP ie smtplib has been used to send emails. 
- Pycrypto has been used for encryption purposes.

Clone the repository into a directory of your own choice.

`git clone https://github.com/SriHarshaGajavalli/CSCS`
`cd CSCS`


## Installation

- create a virtual environment

  `mkvirtualenv cscs` 
- run (Make sure python 3.5.x is installed before you run this)

  `sudo pip3 install -r Source/requirements.txt`
- Start the ssh service in Linux: (Ensure ssh service is started in all the clients and python 3.5.x is installed) 

  `systemctl start ssh`


## Usage

- change the working directory to Source using cd.
	
	`cd Source/`
- To setup the database, run

   `python Database.py`
- Edit config.xml and email_config.json with appropriate configurations 
- On server, run

   `python server.py`
   

Do star it, follow me, if you like this. Stay tuned to me for more updates!


