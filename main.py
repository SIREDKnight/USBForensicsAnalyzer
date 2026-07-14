import tkinter as tk

from gui.dashboard import Dashboard



def main():

    root = tk.Tk()

    root.title(
        "USB Forensics Analyzer"
    )

    root.geometry(
        "1100x700"
    )


    Dashboard(

        root

    )


    root.mainloop()



if __name__ == "__main__":

    main()