<h1>${\textsf{\color{purple}Kuko}}$</h1>

Kuko is a web service that works with Apache Zookeeper. It enables users to create and manage interactive quizzes via terminal commands or with POST/GET requests.

<strong>1 - How to execute the application:</strong>

- Before running any script, there must be an active Apache Zookeeper server on the local network. 
This can be done by executing the following command in the directory where Apache Zookeeper is installed:<br>
`$ bin/zkCli.sh`

- Apache Zookeeper download link (version 3.8.4):<br>
https://www.apache.org/dyn/closer.lua/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz

- Then, the application server script must be executed, through the command:<br>
`$ python3 kuko_server.py [host] [port]`

- After this, any clients can use the application in the terminal through the command:<br>
`$ python3 kuko_client.py [id_participant] [host] [port]`

- To serve the application in Flask, the following script must be executed through the command:<br>
`$ python3 kuko_flask.py [id_participant] [host] [port]`

<strong>2 - How to use the application:</strong>

- It is possible to use the application through the terminal using direct inputs. 
Some examples of commands are:

	- QUESTION:<br>
	    `$ 10;What's the capital of Germany?;Frankfurt am Main;Berlin;Cologne;Munich;2`<br>
	- QSET:<br>
	    `$ 20;4;5;6;7;8`<br>
	- QUIZ:<br>
	    `$ 30;3;5;5;5;5;5`<br>
	- REG:<br>
	    `$ 60;3`<br>
	- LAUNCH:<br>
	    `$ 40;3`<br>
	- GET:<br>
	    `$ 70;3`<br>
	- ANS:<br>
	    `$ 80;3;2`<br>
	- NEXT:<br>
	    `$ 50;3`<br>
	- REL:<br>
	    `$ 90;3`<br>

- If kuko_flask.py is being executed, 
the application is being served in Flask, so it is also possible to perform operations 
through the POST and GET methods. Some examples are:

	- curl with POST method, to perform the QUESTION operation:<br>
	    `$ curl -X POST -H "Content-Type: application/json" -d 
	    '{"question": "What's the capital of Australia?", 
	    "answers": "Canberra;Melbourne;Sydney;Perth;Brisbane", 
	    "k":2}' http://127.0.0.1:5005/question`
	
	- curl with GET method, to perform the REL operation:<br>
	    `$ curl -G -d "quiz=1" http://127.0.0.1:5005/rel`
	
	- URL with GET method to perform the GET operation:<br>
	    `http://127.0.0.1:5005/get?quiz=3`

<strong>3 - Other Information:</strong>

- The Flask application always uses host 127.0.0.1 and port 5005. 
- The flask_cors extension needs to installed to enable Cross Origin Resource Sharing. 
This extension needs to be installed separately from the Flask framework with the following command:<br>
`$ pip install -U flask-cors`
- The Apache Zookeeper client always uses host 127.0.0.1 and port 2181. 
- RSA keys for SSL certificates have a size of 2048 bits.

<strong>Developed By:</strong><br>
Rayan S. Santana
