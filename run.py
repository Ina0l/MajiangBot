from tkinter import *
from tkinter import ttk

import MajiangBot


def launch() -> None:
    global launching_root
    launching_root.destroy()
    MajiangBot.launch_bot()

def destroy() -> None:
    global launching_root
    print("Launch aborted")
    launching_root.destroy()

print()

launching_root = Tk()
launching_root.title("bot launching")

launching_frame: Frame = ttk.Frame(launching_root, padding="50 50 50 50")
launching_frame.grid(column=0, row=0, sticky=(N, W, E, S))
launching_root.columnconfigure(0, weight=1)
launching_root.rowconfigure(0, weight=1)

ttk.Button(launching_frame, text="Launch", padding="5 5 5 5", command=launch).grid(column=1, row=3, sticky=W)
ttk.Button(launching_frame, text="Cancel", padding="5 5 5 5", command=destroy).grid(column=3, row=3, sticky=E)

ttk.Label(launching_frame, text=" ").grid(column=2, row=2, sticky=N)
ttk.Label(launching_frame, text="Launch the Bot ?", font=("Arial", 20)).grid(column=2, row=1, sticky=N)

launching_root.mainloop()
