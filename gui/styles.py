import tkinter as tk
from tkinter import ttk



class GUIStyles:


    @staticmethod
    def apply(root):


        style = ttk.Style(root)


        # Use modern built-in theme

        try:

            style.theme_use(
                "clam"
            )

        except:

            pass



        # ==================================================
        # GENERAL
        # ==================================================

        style.configure(

            "TFrame",

            background="#1e1e1e"

        )


        style.configure(

            "TLabel",

            background="#1e1e1e",

            foreground="white",

            font=(

                "Segoe UI",

                10

            )

        )



        style.configure(

            "Title.TLabel",

            background="#1e1e1e",

            foreground="#00d9ff",

            font=(

                "Segoe UI",

                18,

                "bold"

            )

        )



        style.configure(

            "Header.TLabel",

            background="#1e1e1e",

            foreground="white",

            font=(

                "Segoe UI",

                12,

                "bold"

            )

        )



        # ==================================================
        # BUTTONS
        # ==================================================

        style.configure(

            "TButton",

            font=(

                "Segoe UI",

                10,

                "bold"

            ),

            padding=8

        )



        # ==================================================
        # TREEVIEW TABLES
        # ==================================================

        style.configure(

            "Treeview",

            background="#252526",

            foreground="white",

            fieldbackground="#252526",

            rowheight=28,

            font=(

                "Segoe UI",

                10

            )

        )



        style.configure(

            "Treeview.Heading",

            font=(

                "Segoe UI",

                10,

                "bold"

            )

        )



        # ==================================================
        # LABEL FRAMES
        # ==================================================

        style.configure(

            "TLabelframe",

            background="#1e1e1e",

            foreground="white"

        )


        style.configure(

            "TLabelframe.Label",

            background="#1e1e1e",

            foreground="#00d9ff",

            font=(

                "Segoe UI",

                11,

                "bold"

            )

        )



    @staticmethod
    def configure_window(root):


        root.configure(

            background="#1e1e1e"

        )


        root.geometry(

            "1200x750"

        )


        root.minsize(

            1000,

            650

        )


        root.title(

            "USB Forensics Analyzer - DFIR Edition"

        )