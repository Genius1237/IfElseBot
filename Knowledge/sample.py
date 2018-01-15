import aiml
import os

# Create the kernel and learn AIML files
kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"): 
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "sample.xml", commands = "load aiml b")
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