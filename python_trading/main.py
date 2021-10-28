import tkinter as tk # helps us to create the window
import logging # is used for receiving messages about errors, bugs etc.
from binance_future import *
logger = logging.getLogger()

#stream_handler = logging.StreamHandler()

#stream_handler.setFormatter(formatter)
#stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter(# формат сообщений, которые будут выводится при запуске.
    "%(asctime)s %(levelname)s :: %(message)s"
    )

file_handler = logging.FileHandler('info.log') #создает файл в котором выводятся сообщения(file handler = файл оброботчик# )
file_handler.setFormatter(formatter) #внутри файла ставит формат
file_handler.setLevel(logging.DEBUG) # ставит уровень читаемости сообщений(какие сообщения читать)

#logger.addHandler(stream_handler)
logger.addHandler(file_handler) #добавляет в Логгер наш файл
logger.setLevel(logging.INFO) # в логгере ставит уровень читаемоси сообщений
logger.info("This message shows when that code was executed.") # само сообщение

if __name__ == '__main__':
    root = tk.Tk()
    root.title("My_First_Window_made_for_Binance")
    root.mainloop() # mainloop prevent closing the window

    print(get_contracts())
# Изучить!

