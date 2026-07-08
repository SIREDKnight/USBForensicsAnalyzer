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

            "1000x600"

        )


        self.window.configure(

            bg="#1e1e1e"

        )


        self.create_interface()



    # ==================================================
    # CREATE WINDOW
    # ==================================================

    def create_interface(self):


        title = tk.Label(

            self.window,

            text="FORENSIC TIMELINE ANALYSIS",

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



        info = tk.Label(

            self.window,

            text=(

                "Collected Windows forensic events "

                "ordered by timestamp"

            ),

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                10

            )

        )


        info.pack()



        # ===============================
        # TABLE FRAME
        # ===============================

        frame = tk.Frame(

            self.window

        )


        frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

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

            text="Timestamp"

        )


        self.table.heading(

            "artifact",

            text="Artifact Source"

        )


        self.table.heading(

            "description",

            text="Description"

        )



        self.table.column(

            "time",

            width=220

        )


        self.table.column(

            "artifact",

            width=180

        )


        self.table.column(

            "description",

            width=500

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



        self.load_timeline()



    # ==================================================
    # LOAD EVENTS
    # ==================================================

    def load_timeline(self):


        if not self.timeline:


            self.table.insert(

                "",

                "end",

                values=(

                    "N/A",

                    "NONE",

                    "No timeline events available"

                )

            )


            return



        for event in self.timeline:


            self.table.insert(

                "",

                "end",

                values=(

                    self.safe_value(

                        event,

                        "time"

                    ),


                    self.safe_value(

                        event,

                        "artifact"

                    ),


                    self.safe_value(

                        event,

                        "description"

                    )

                )

            )



    # ==================================================
    # SAFE DATA HANDLING
    # ==================================================

    def safe_value(

            self,

            event,

            key):


        value = event.get(

            key,

            "UNKNOWN"

        )


        if value is None:


            return "UNKNOWN"


        return str(value)