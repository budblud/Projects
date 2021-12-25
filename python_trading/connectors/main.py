import tkinter as tk  # helps us to create the window
import logging
from connectors.binance_future import BinanceSamples



logger = logging.getLogger()

# stream_handler = logging.StreamHandler()

# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter(  # формат сообщений, которые будут выводится при запуске.
    "%(asctime)s %(levelname)s :: %(message)s"
)

file_handler = logging.FileHandler(
    'info.log')  # создает файл в котором выводятся сообщения(file handler = файл оброботчик# )
file_handler.setFormatter(formatter)  # внутри файла ставит формат
file_handler.setLevel(logging.DEBUG)  # ставит уровень читаемости сообщений(какие сообщения читать)

# logger.addHandler(stream_handler)
logger.addHandler(file_handler)  # добавляет в Логгер наш файл
logger.setLevel(logging.INFO)  # в логгере ставит уровень читаемоси сообщений
logger.info("This message shows when that code was executed.")  # само сообщение

if __name__ == '__main__':

    binance = BinanceSamples(ans = True)
    print(binance.get_balance())


    root = tk.Tk()
    #root.cofig(bg = grey12) это background всего окна

    root.title("My_First_Window_made_for_Binance")
    '''binance_contracts = get_contracts()

    i = 0
    j = 0
    for contract in binance_contracts:
        label_widget = tk.Label(root, text=contract, borderwidth=1, relief=tk.SOLID, width= 13, fg="white")  # так мы создаем виджет,
        # давая текст который будет в нем(text=) и в каком окне его писать(root)
        # borderwidth(ширина границ), width(ширина виджета), relief (показывает сами графицф?)
        # так же может быть bg(background = виджета), fg(foreground = цвет текста)


        # раставить текст в виджете мы можем двумя способами:
        # 1) виджет . pack(берет один аргумент: где в окне его ставить относительно других элементов(вверх , низ...(tk.TOP)))
        # 2) виджет . grid(берет два аргумента(colomn and row начинаещиеся с 0))
        label_widget.grid(column=i, row=j, sticky='ew')# sticky разширяет виджет аргумент = "SNWE"(south, north...)
        # label_widget.pack(side=tk.TOP)
        if j == 8:
            i += 1
            j = 0
        else:
            j += 1'''

    root.mainloop()  # mainloop prevent closing the window

# Изучить!

