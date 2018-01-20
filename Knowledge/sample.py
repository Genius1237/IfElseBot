import aiml
import os
import random
import time
import pyttsx3
from weather import Weather
from news import News
from google import Search
from DBconnect import *
import signal
import datetime
import sys
import string

def evaulateExpression(fexp):
    expstr = fexp.replace(' ','')
    return eval(expstr)


# Create the kernel and learn AIML files
kernel = aiml.Kernel()
engine = pyttsx3.init()
obj = DBconnect()
obj.getConnection('./connection.db')
obj.putQuery("CREATE TABLE IF NOT EXISTS chat_history ( qid integer PRIMARY KEY AUTOINCREMENT,question text NOT NULL, response text);")
obj.putQuery("CREATE TABLE IF NOT EXISTS  unknown ( qid integer PRIMARY KEY AUTOINCREMENT, question text NOT NULL, response text);")
dblistQuery = "SELECT NAME FROM sqlite_master WHERE TYPE=\"table\";"
insertQuery1b = "INSERT INTO chat_history ( question, response ) VALUES ("
insertQuery2b = "INSERT INTO unknown (question, response ) VALUES ("


if os.path.isfile("bot_brain.brn"): 
    #kernel.bootstrap(brainFile = "bot_brain.brn")
    pass
if 1==1:
    kernel.bootstrap(learnFiles = "sample.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

querystring=""


# Handles CTRL+C
def sigint_handler(signum,frame):
	obj.closeConnection()
	exit()

def speakOut(output,param=""):
    if(param=="enable-voice"):
    	engine.say(output)
    	engine.runAndWait()

while True:
    signal.signal(signal.SIGINT, sigint_handler)
    message = input("Enter your message to the bot: ")
    if(len(sys.argv)<=1):
    	sys.argv.append("enable-voice")
    if(len(message)<1):
    	continue
    if message == "quit":
        obj.closeConnection()
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response=""
        kernel.setPredicate('ctype',0)
        bot_response = kernel.respond(message)
        if len(bot_response)<2:
            # bot_response="i did not understand, what is that?"            
            # querystring=insertQuery1b+"\""+message+"\""+",\""+bot_response+"\");"
            # obj.putQuery(querystring)
            # speakOut(bot_response,sys.argv[1])
            # print(bot_response)
            # kernel.setPredicate('topic',"eagertoknow")
            # bot_response = input("Enter your message to the bot: ")
            # print("Okay, thank you for telling me about it")
            
            # querystring=insertQuery2b+"\""+message+"\""+",\""+bot_response+"\");"
            # obj.putQuery(querystring)
            # speakOut("Okay, thank you for telling me about it",sys.argv[1])
            bot_response="i did not understand, want to search google for it?"
            
            querystring=insertQuery1b+"\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            speakOut(bot_response,sys.argv[1])
            print(bot_response)
            kernel.setPredicate('topic',"eagertoknow")
            bot_response = input("Enter your message to the bot: ")
            if(bot_response.lower()=="YES".lower()):
            	bot_response="Okay let me see..."
            	print(bot_response)
            	querystring=insertQuery1b+"\"Yes\", \""+bot_response+"\");"
            	obj.putQuery(querystring)
            	speakOut(bot_response,sys.argv[1])
            	s=Search.make_request(message)
            	if s['success']:
            		print("Got something.. Answer is "+s['d'])
            		bot_response="Got something.. Answer is "+s['d']
            		querystring=insertQuery2b+"\""+message+"\""+",\""+s['d']+"\");"
            		obj.putQuery(querystring)
            		speakOut(bot_response,sys.argv[1])

            	else:
            		print("Search Failed")
            		bot_response=bot_response+"Search Failed"
            		speakOut(bot_response,sys.argv[1])

         
            querystring=insertQuery1b+"\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            continue

        print(bot_response)        
        querystring=insertQuery1b+"\""+message+"\""+",\""+bot_response+"\");"
        obj.putQuery(querystring)
        speakOut(bot_response,sys.argv[1])
        inp = kernel.getPredicate('ctype')
        if inp=="1" :
            time.sleep(1)
            kernel.setPredicate('expression',str(evaulateExpression(kernel.getPredicate('expression'))))
            bot_response = kernel.respond('results')
            bot_speech=bot_response

        elif inp=="2":
            time.sleep(1)
            num = random.randint(0,1)
            if num==1:
                kernel.setPredicate('expression',"Heads")
            else:
                kernel.setPredicate('expression',"Tails")

            bot_response = kernel.respond('toss outcome')
            bot_speech=bot_response

        elif inp=='3' or inp=='4':
            time.sleep(1)
            uval = 6
            num = random.randint(1,6)
            if inp=="4":
                uval = int(kernel.getPredicate('expression'))
                num = random.randint(1,uval)
            kernel.setPredicate('expression',str(num))
            bot_response = kernel.respond('die outcome')
            bot_speech=bot_response

        elif inp=='5' or inp=='6':
            if inp=='5':
                city=kernel.getPredicate('home_city')
                if city is "":
                    city="Secunderabad"
            else:
                city=kernel.getPredicate('city')

            w=Weather.get_current_weather(city)
            if w['success']:
                bot_response = "The weather in {} is {}. The temperature is {} with a minimum of {} and a maximum of {} celcius. The humidity is {}%.".format(
                    w['place'],w['desc'],w['temp'],w['temp_min'],w['temp_max'],w['humidity'])
            
            else:
                bot_response="Sorry, couldn't get the weather"

            bot_speech=bot_response

        elif inp=='7' or inp=='8' :
            if inp=='7':
                city=kernel.getPredicate('home_city')
                if city is "":
                    city="Secunderabad"
            else:
                city=kernel.getPredicate('city')

            w=Weather.get_5_day_forecast(city)
            if w['success']:
                bot_response="The forecast for {} is as follows\n".format(w['place'])
                for a in w['w']:
                    d=datetime.datetime.strptime(a['date'],"%Y-%m-%d %H:%M:%S").date()
                    bot_response+=("{} {} {}, {} with a temperature of {} celcius and humidity of {}%\n".format(d.day,d.month,d.year,a['desc'],a['temp'],a['humidity']))

            else:
                bot_response="Sorry, couldn't get the forecast"

            bot_speech=bot_response

        elif inp=='9' or inp=='10':
            news=kernel.getPredicate('news')
            if news!="":
                if inp=='9':
                    n=News.get_india_top_headlines(news)
                else:
                    n=News.get_world_top_headlines(news)
            else:
                if inp=='9':
                    n=News.get_india_top_headlines()
                else:
                    n=News.get_world_top_headlines()
            if n['success']:
                bot_response=""
                bot_speech=""
                for a in n['a']:
                    bot_response+="{}\n{}\n\n".format(a['title'],a['url'])
                    bot_speech+="{}\n".format(a['title'])
                
            else:
                bot_response="Sorry, couldn't get the news"
                bot_speech=bot_response

        elif len(bot_response)<2:
            '''
            s=Search.make_request(q)
            if s['success']:
                #got something. Answer is s['d']
            else:
                #search fail
            '''

            bot_response="i did not understand, want to search google for it?"
            
            querystring=insertQuery1b+"\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            speakOut(bot_response,sys.argv[1])
            print(bot_response)
            kernel.setPredicate('topic',"eagertoknow")
            bot_response = input("Enter your message to the bot: ")
            if(bot_response.lower()=="YES".lower()):
            	bot_response="Ok, let me see..."
            	print(bot_response)
            	querystring=insertQuery1b+"\"Yes\","+bot_response+"\");"
            	obj.putQuery(querystring)
            	speakOut(bot_response,sys.argv[1])
            	s=Search.make_request(message)
            	if s['success']:
            		print("Got something.. Answer is "+s['d'])
            		bot_response=bot_response+"Got something.. Answer is "+s['d']
            		for c in string.punctuation:
            			s['d'].replace(c,'')
            		querystring=insertQuery2b+"\""+message+"\""+",\""+s['d']+"\");"
            		speakOut(bot_response,sys.argv[1])

            	else:
            		print("Search Failed")
            		bot_response="Search Failed"
            		speakOut(bot_response,sys.argv[1])

         
            querystring=insertQuery1b+"\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            speakOut("Okay, thank you for telling me about it",sys.argv[1])
            continue