import tkinter as tk # helps us to create the window
import logging # is used for receiving messages about errors, bugs etc.

logger = logging.getLogger()

#stream_handler = logging.StreamHandler()

#stream_handler.setFormatter(formatter)
#stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter(# формат сообщений, которые будут выводится при запуске.
    "%(asctime)s %(levelname)s :: %(message)s"
    )

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

#logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
logger.info("This message shows when that code was executed.")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("My_First_Window_made_for_Binance")
    root.mainloop() # mainloop prevent closing the window

# Изучить!

