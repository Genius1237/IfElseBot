import aiml
import os
import random
import time
import pyttsx3
from weather import Weather

def evaulateExpression(fexp):
    expstr = fexp.replace(' ','')
    return eval(expstr)


# Create the kernel and learn AIML files
kernel = aiml.Kernel()
engine = pyttsx3.init()

if os.path.isfile("bot_brain.brn"): 
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "sample.xml", commands = "load aiml b")
    #kernel.bootstrap(learnFiles = "sample.xml", commands = "load math")
    kernel.saveBrain("bot_brain.brn")

# Press CTRL-C to break this loop
while True:
    message = input("Enter your message to the bot: ")
    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response=""
        kernel.setPredicate('ctype',0)
        bot_response = kernel.respond(message)
        if len(bot_response)<2:
            bot_response="i don't know what you are talking about"
            print(bot_response)
            continue
        print(bot_response)
        engine.say(bot_response)
        engine.runAndWait()
        inp = kernel.getPredicate('ctype')
        if inp=="1" :
            time.sleep(1)
            kernel.setPredicate('expression',str(evaulateExpression(kernel.getPredicate('expression'))))
            bot_response = kernel.respond('results')
            print(bot_response)
            engine.say(bot_response)
            engine.runAndWait()

        elif inp=="2":
            time.sleep(1)
            num = random.randint(0,1)
            if num==1:
                kernel.setPredicate('expression',"Heads")
            else:
                kernel.setPredicate('expression',"Tails")

            bot_response = kernel.respond('toss outcome')
            print(bot_response)
            engine.say(bot_response)
            engine.runAndWait() 	


        elif inp=='3' or inp=='4':
            time.sleep(1)
            uval = 6
            num = random.randint(1,6)
            if inp=="4":
                uval = int(kernel.getPredicate('expression'))
                num = random.randint(1,uval)
            kernel.setPredicate('expression',str(num))
            bot_response = kernel.respond('die outcome')
            print(bot_response)
            engine.say(bot_response)
            engine.runAndWait()

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
            print(bot_response)
            engine.say(bot_response)
            engine.runAndWait()

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

            print(bot_response)
            engine.say(bot_response)
            engine.runAndWait()


        elif len(bot_response)<2:
            bot_response="i don't know what you are talking about"
            print(bot_response)
            engine.say(bot_response)
            engine.runAndWait()