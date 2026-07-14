import tkinter as tk
from tkinter import ttk



class GUIStyles:
    """
    Central location for application GUI styling.
    """



    @staticmethod
    def apply(root):

        style = ttk.Style(

            root

        )


        try:

            style.theme_use(

                "clam"

            )

        except Exception:

            pass



        style.configure(

            "TButton",

            font=(

                "Arial",

                10

            ),

            padding=6

        )



        style.configure(

            "TLabel",

            font=(

                "Arial",

                10

            )

        )



        style.configure(

            "Treeview.Heading",

            font=(

                "Arial",

                10,

                "bold"

            )

        )



        style.configure(

            "Treeview",

            rowheight=25

        )



    @staticmethod
    def center_window(window, width, height):

        """
        Center a tkinter window on screen.
        """

        screen_width = window.winfo_screenwidth()

        screen_height = window.winfo_screenheight()



        x = int(

            (screen_width - width) / 2

        )


        y = int(

            (screen_height - height) / 2

        )



        window.geometry(

            f"{width}x{height}+{x}+{y}"

        )