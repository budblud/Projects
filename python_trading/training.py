import logging

#create a logger, think about it as container where our logs handlers are saved
#set the level of messages
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#create an instance of the format of output message
format = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

#create file where we want to receive logs to
#then set a format of it + set level of messages(INFO, ERROR, etc)
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(format)
file_handler.setLevel(logging.INFO)

#add the file handler into the logger
logger.addHandler(file_handler)

#write the message we want to produce in case of execution the program
logger.info("Message displays in case of some actions occur")