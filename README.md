The copyright of this product belongs to M Fazle Taher, Graduate Student 2011, GWU.
This project is done under Professor A. Bellacchia, CS Faculty, GWU.
The code of this project is free to use and can be modified for your research.


Database settings:
First Download mongodb from http://www.mongodb.org/ in this project I have used
mongodb 1.6.5+ 64bit.

You can download twitter stream to your mongo database directly with following command.

"curl -d @tracking.txt http://stream.twitter.com/1/statuses/filter.json -u [username]:[password] | mongoimport -d [database] -c [collection]"

If you are using windows you can download cygwin to run the command. Create tracking.txt in your cygwin home with tracking words.
Once you download the tweets you can use tweetdb.py file process them from the database and create file. But remember to turn off
your database storing option by setting its value to False.

To start mongo database go to mongo home\bin dir and type mongod in your command prompt.
By default mongo try to store database in your root path /data/db/. It is advisable
to create the directories before starting the database for the first time. You can also run:
"mongod --dbpath [path to your db]" if you are running database in different path.

Python Packages:
You will need the following packages for this software to work:

1. PyMongo - mongodb driver for python
2. PyCurl - For Twitter stream connection over curl
3. lxml Parser
4. NLTK for language detection

To start the software, run tweetstream.py.

You can change settings for the software in stream.ini configuration file.


