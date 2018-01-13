import aiml

kernel = aiml.Kernel()
kernel.learn("sample.xml")
kernel.respond("load aiml b")

while True:
	print(kernel.respond(input("Enter your message >> ")))