# Chatbot - CS F407 Assignment 1

### To install dependencies
```
pip install python-aiml pyttsx3
```

### To run the chatbot:
python3 Knowledge/sample.py

### Content of Project Files
Inside the Knowledge folder

1. **sample.py**: Uses python-aiml library to learn and use the aiml Knowledge files. Imports and uses the other modules like weather.py, news.py etc.

2. **DBconnect.py**: Contains class DBconnect to establish connection with, and Query the Sqlite Database.

3. **weather.py**: Retrieves the latest weather related information from openweathermap.org API, for a given place.

4. **news.py**:	Retrieves the latest news for a given place from newsapi.org.

5. **sample.xml**: Is the main XML file, that is called from sample.py, it loads and learns all aiml files in the ./aiml_files directory

6. **./aiml_files**: Contains an AIML file for each domain.
	- **greetings.aiml**: *Initiating and Terminating the conversation, like Hi, Hello, I am great, Bye .. etc.*
	- **personal.aiml**: *To know and store details about the user like name, location, tastes etc.*
	- **about_bits.aiml**: *Basic information about BITS Pilani, Hyderabad, Goa, Pilani Campuses.*
	- **Reachablilty.aiml**: *Information about Reaching BITS Pilani Hyderabad Campus.*
	- **fests.aiml**: *Information about Atmos, Pearl, and Arena, BITS Pilani, Hyderabad Campus.*
	- **eateries.aiml**: *To Suggest eateries at BITS Pilani, Hyderabad Campus based on food preferences. Tells about prices, ambience and *avaerage time for order.
	- **offeredcourses.aiml**: *Information about departments, degree programs and key courses in computer-science department BITS Pilani, *Hyderabad Campus
	- **math.aiml**: *To calculate an expression, toss a coin, roll a 'x' sided die*
	- **control.aiml**: *To handle questions, to which the bot does not know an answer to*
	- **online.aiml**: *To get the latest weather and news updates*
