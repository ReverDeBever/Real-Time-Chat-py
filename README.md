# Chat thing in python

A small chat server using asyncio library in python.
Open ```client.py``` with ```python client.py``` enter your host and name. Then you can chat with all the clients that are in the same server. To host your own server, open ```server.py``` with ```python server.py```. 
You can then enter on what ip you want to host the server. You can use 127.x.x.x or your local ip from your device. If you want to make it public, then forward port 5000 with the chosen local ip. 
Your host should be (public ip) x.x.x.x:5000. You can also use a domain. Add a new type A DNS and type the name and your public ip. After that make a type SRV DNS. Name it _(chosen name from the type A DNS)._tcp.(chosen name from the type A DNS). Prio: 10, Port: 5000, SRV Weight: 10, Content: (chosen name from the type A DNS).yourdomain.com

The default server is being runned on my own server (test.reverbever.online).
