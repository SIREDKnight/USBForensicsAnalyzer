import tkinter as tk
from tkinter import ttk



class TimelineView:



    def __init__(self, parent):


        self.frame = ttk.Frame(

            parent

        )


        self.create_widgets()



    def create_widgets(self):


        title = ttk.Label(

            self.frame,

            text="FORENSIC TIMELINE",

            font=(

                "Arial",

                14,

                "bold"

            )

        )


        title.pack(

            pady=10

        )



        columns = (

            "time",

            "artifact",

            "event_id",

            "source",

            "description"

        )



        self.table = ttk.Treeview(

            self.frame,

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

            "event_id",

            text="Event ID"

        )


        self.table.heading(

            "source",

            text="Source"

        )


        self.table.heading(

            "description",

            text="Description"

        )



        self.table.column(

            "time",

            width=150

        )


        self.table.column(

            "artifact",

            width=130

        )


        self.table.column(

            "event_id",

            width=80

        )


        self.table.column(

            "source",

            width=150

        )


        self.table.column(

            "description",

            width=400

        )



        scrollbar = ttk.Scrollbar(

            self.frame,

            orient="vertical",

            command=self.table.yview

        )


        self.table.configure(

            yscrollcommand=scrollbar.set

        )



        self.table.pack(

            side="left",

            fill="both",

            expand=True

        )


        scrollbar.pack(

            side="right",

            fill="y"

        )



    def show_timeline(self, timeline):


        # Clear old data

        for item in self.table.get_children():

            self.table.delete(

                item

            )



        if not timeline:


            self.table.insert(

                "",

                "end",

                values=(

                    "NO DATA",

                    "",

                    "",

                    "",

                    "No timeline available"

                )

            )

            return



        for event in timeline:



            if hasattr(

                event,

                "to_dict"

            ):


                event = event.to_dict()



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

                        "event_id",

                        ""

                    ),


                    event.get(

                        "source",

                        ""

                    ),


                    event.get(

                        "description",

                        "UNKNOWN"

                    )

                )

            )



    def get_frame(self):


        return self.frame