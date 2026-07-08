import tkinter as tk
from tkinter import ttk



class TimelineView:


    def __init__(self, timeline):


        self.timeline = timeline



        self.window = tk.Toplevel()


        self.window.title(

            "Forensic Timeline Viewer"

        )


        self.window.geometry(

            "900x500"

        )


        self.window.configure(

            bg="#1e1e1e"

        )



        self.create_interface()



    # ==================================================
    # INTERFACE
    # ==================================================

    def create_interface(self):


        title = tk.Label(

            self.window,

            text="FORENSIC TIMELINE",

            bg="#1e1e1e",

            fg="#00d9ff",

            font=(

                "Segoe UI",

                18,

                "bold"

            )

        )


        title.pack(

            pady=20

        )



        # ===============================
        # TABLE
        # ===============================

        frame = tk.Frame(

            self.window

        )


        frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=10

        )



        columns = (

            "time",

            "artifact",

            "description"

        )



        self.table = ttk.Treeview(

            frame,

            columns=columns,

            show="headings"

        )



        self.table.heading(

            "time",

            text="Time"

        )


        self.table.heading(

            "artifact",

            text="Artifact"

        )


        self.table.heading(

            "description",

            text="Description"

        )



        self.table.column(

            "time",

            width=200

        )


        self.table.column(

            "artifact",

            width=150

        )


        self.table.column(

            "description",

            width=450

        )



        scrollbar = ttk.Scrollbar(

            frame,

            orient="vertical",

            command=self.table.yview

        )


        self.table.configure(

            yscrollcommand=scrollbar.set

        )



        scrollbar.pack(

            side="right",

            fill="y"

        )


        self.table.pack(

            fill="both",

            expand=True

        )



        self.load_events()



    # ==================================================
    # LOAD TIMELINE
    # ==================================================

    def load_events(self):


        for event in self.timeline:


            self.table.insert(

                "",

                "end",

                values=(

                    event.get(

                        "time",

                        "UNKNOWN"

                    ),


                    event.get(

                        "artifact",

                        "UNKNOWN"

                    ),


                    event.get(

                        "description",

                        "UNKNOWN"

                    )

                )

            )