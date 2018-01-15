import aiml
import os
import random
import time

def evaulateExpression(fexp):
    expstr = fexp.replace(' ','')
    return eval(expstr)


# Create the kernel and learn AIML files
kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"): 
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "sample.xml", commands = "load aiml b")
    kernel.bootstrap(learnFiles = "sample.xml", commands = "load math")
    kernel.saveBrain("bot_brain.brn")

# Press CTRL-C to break this loop
while True:
    message = input("Enter your message to the bot: ")
    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response = kernel.respond(message)
        if(len(bot_response)<2):
            bot_response="i don't know what you are talking about"
            print(bot_response)
            continue
        print(bot_response)
        time.sleep(1)
        inp = kernel.getPredicate('ctype')
        if(inp=="1"):
            kernel.setPredicate('expression',str(evaulateExpression(kernel.getPredicate('expression'))))
            bot_response = kernel.respond('results')

        elif(inp=="2"):
            num = random.randint(0,1)
            if(num==1):
                kernel.setPredicate('expression',"Heads")
            else:
                kernel.setPredicate('expression',"Tails")

            bot_response = kernel.respond('toss outcome')


        elif(inp=='3' or inp=='4'):
            uval = 6
            num = random.randint(1,6)
            if(inp=="4"):
                uval = int(kernel.getPredicate('expression'))
                num = random.randint(1,uval)
            kernel.setPredicate('expression',str(num))
            bot_response = kernel.respond('die outcome')

        else:
            bot_response=""

            #print(bot_response)
        if(len(bot_response)<2):
            bot_response="i don't know what you are talking about"
       
        print(bot_response)