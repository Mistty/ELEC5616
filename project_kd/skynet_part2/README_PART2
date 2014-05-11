Welcome to SkyNet
=================

Usage -- uploading and viewing secrets
======================================
smerity@pegasus:~/usyd/elec5616_proj/framework_part2$ python3.2 bot.py
Listening on port 1337
Waiting for connection...
Enter command: mine
Mining for Bitcoins...
-
Mined and found Bitcoin address: 1kfRSGOKX8t2jPviL1DwQEu3Kd17l
Enter command: mine
Mining for Bitcoins...
-
Mined and found Bitcoin address: 34PvZLVfodFkw0ipkCcbAl95HPcz40BKdD2
Enter command: upload secrets
Saved valuables to pastebot.net/secrets for the botnet master
Enter command: exit
smerity@pegasus:~/usyd/elec5616_proj/framework_part2$ python3.2 master_view.py
Which file in pastebot.net does the botnet master want to view? secrets
Bitcoin: 1kfRSGOKX8t2jPviL1DwQEu3Kd17l
Bitcoin: 34PvZLVfodFkw0ipkCcbAl95HPcz40BKdD2

Usage -- signing updates and downloading updates
================================================
merity@pegasus:~/usyd/elec5616_proj/framework_part2$ python3.2 master_sign.py
Which file in pastebot.net should be signed? hello.fbi
Signed file written to pastebot.net/hello.fbi.signed
smerity@pegasus:~/usyd/elec5616_proj/framework_part2$ python3.2 bot.py
Listening on port 1337
Waiting for connection...
Enter command: download hello.fbi
The file has not been signed by the botnet master
Enter command: download hello.fbi.signed
Stored the received file as hello.fbi.signed
Enter command: list
Files stored by this bot: hello.fbi.signed
Valuables stored by this bot: []
Enter command: exit
