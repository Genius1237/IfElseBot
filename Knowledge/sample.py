import aiml
import os
import random
import time
import pyttsx3
from weather import Weather
from DBconnect import *
import signal
import sys

def evaulateExpression(fexp):
    expstr = fexp.replace(' ','')
    return eval(expstr)


# Create the kernel and learn AIML files
kernel = aiml.Kernel()
engine = pyttsx3.init()
obj = DBconnect()
obj.getConnection('./connection.db')
obj.putQuery("CREATE TABLE IF NOT EXISTS chat_history ( qid integer PRIMARY KEY,question text NOT NULL, response text);")
obj.putQuery("CREATE TABLE IF NOT EXISTS  unknown ( qid integer PRIMARY KEY AUTOINCREMENT, question text NOT NULL, reponse text);")
dblistQuery = "SELECT NAME FROM sqlite_master WHERE TYPE=\"table\";"
getuquid = "SELECT * FROM qidvals;"
insertQuery1b = "INSERT INTO chat_history values ("
insertQuery2b = "INSERT INTO unknown values ("
updateQueryQid = "UPDATE qidvals SET "
updateQueryQidend = " WHERE qid=0;"
tlist_names = obj.getQuery(dblistQuery)
flag = False
for name in tlist_names:
    if(name[0]=="qidvals"):
        flag = True
        break

if(flag==False):
    obj.putQuery("CREATE TABLE IF NOT EXISTS qidvals (qid integer PRIMARY KEY default 0, kqid integer default 0, ukqid integer default 0);")
    obj.putQuery("INSERT INTO qidvals VALUES (0,0,0);")
#obj.putQuery("CREATE TABLE IF NOT EXISTS qidvals (qid integer PRIMARY KEY default 0, kqid integer default 0, ukqid integer default 0);")

if os.path.isfile("bot_brain.brn"): 
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "sample.xml", commands = "load aiml b")
    #kernel.bootstrap(learnFiles = "sample.xml", commands = "load math")
    kernel.saveBrain("bot_brain.brn")

# Press CTRL-C to break this loop
defvals= obj.getQuery(getuquid)[0]
#print(defvals)
qid=int(defvals[1])
unknown_qid=int(defvals[2])
querystring=""


# Handles CTRL+C
def sigint_handler(signum,frame):
	querystring=updateQueryQid+"kqid = "+str(qid)+","+"ukqid = "+str(unknown_qid)+updateQueryQidend
	obj.putQuery(querystring)
	obj.closeConnection()
	exit()

def speakOut(output,param="enable-voice"):
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
        querystring=updateQueryQid+"kqid = "+str(qid)+","+"ukqid = "+str(unknown_qid)+updateQueryQidend
        obj.putQuery(querystring)
        obj.closeConnection()
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response=""
        kernel.setPredicate('ctype',0)
        bot_response = kernel.respond(message)
        if len(bot_response)<2:
            bot_response="i did not understand, what is that?"
            qid=qid+1
            querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            speakOut(bot_response,sys.argv[1])
            print(bot_response)
            kernel.setPredicate('topic',"eagertoknow")
            #print(kernel.getPredicate('topic'))
            #print("here")
            bot_response = input("Enter your message to the bot: ")
            print("Okay, thank you for telling me about it")
            unknown_qid=unknown_qid+1
            querystring=insertQuery2b+str(unknown_qid)+",\""+message+"\""+",\""+bot_response+"\");"
            #print(querystring)
            obj.putQuery(querystring)
            speakOut("Okay, thank you for telling me about it",sys.argv[1])
            continue

        print(bot_response)
        qid=qid+1
        querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
        obj.putQuery(querystring)
        speakOut(bot_response,sys.argv[1])
        inp = kernel.getPredicate('ctype')
        if inp=="1" :
            time.sleep(1)
            kernel.setPredicate('expression',str(evaulateExpression(kernel.getPredicate('expression'))))
            bot_response = kernel.respond('results')
            qid=qid+1
            querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            print(bot_response)
            speakOut(bot_response,sys.argv[1])

        elif inp=="2":
            time.sleep(1)
            num = random.randint(0,1)
            if num==1:
                kernel.setPredicate('expression',"Heads")
            else:
                kernel.setPredicate('expression',"Tails")

            bot_response = kernel.respond('toss outcome')
            qid=qid+1
            querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            print(bot_response)
            speakOut(bot_response,sys.argv[1]) 	


        elif inp=='3' or inp=='4':
            time.sleep(1)
            uval = 6
            num = random.randint(1,6)
            if inp=="4":
                uval = int(kernel.getPredicate('expression'))
                num = random.randint(1,uval)
            kernel.setPredicate('expression',str(num))
            bot_response = kernel.respond('die outcome')
            qid=qid+1
            querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            print(bot_response)
            speakOut(bot_response,sys.argv[1])

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
            qid=qid+1
            querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            print(bot_response)
            speakOut(bot_response,sys.argv[1])

        elif inp=='7' or inp=='8' :
            if inp=='5':
                city=kernel.getPredicate('home_city')
                if city is "":
                    city="Secunderabad"
            else:
                city=kernel.getPredicate('city')

            w=Weather.get_5_day_forecast(city)
            if w['success']:
                bot_response="The forecast for {} is as follows\n".format(city)
                for a in w['w']:
                    bot_response=""
                    #bot_response+=("{} {} {}, {} with a temperature of {} and humidity of {}%\n".format(a['desc'],a['temp'],a['humidity']))

            else:
                bot_response="Sorry, couldn't get the forecast"

            qid=qid+1
            querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            print(bot_response)
            speakOut(bot_response,sys.argv[1])


        elif len(bot_response)<2:
            bot_response="i did not understand, what is that?"
            qid=qid+1
            querystring=insertQuery1b+str(qid)+",\""+message+"\""+",\""+bot_response+"\");"
            obj.putQuery(querystring)
            speakOut(bot_response,sys.argv[1])
            print(bot_response)
            kernel.setPredicate('topic',"eagertoknow")
            #print(kernel.getPredicate('topic'))
            #print("here")
            bot_response = input("Enter your message to the bot: ")
            print("Okay, thank you for telling me about it")
            unknown_qid=unknown_qid+1
            querystring=insertQuery2b+str(unknown_qid)+",\""+message+"\""+",\""+bot_response+"\");"
            #print(querystring)
            obj.putQuery(querystring)
            speakOut("Okay, thank you for telling me about it",sys.argv[1])
            continue