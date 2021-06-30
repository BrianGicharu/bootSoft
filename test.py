import time
from tkinter import simpledialog
from tkinter import *
import mainClass as m

ip = "192.168.43.1:x"

root = Tk()


def counter():
    maxi = simpledialog.askinteger("Input Dialog", "Enter the integer")
    for c in range(maxi):
        time.sleep(0.1)
        c = +1
        print(ip.replace("x", str(c)))


counter()

