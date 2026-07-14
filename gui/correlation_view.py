import tkinter as tk
from tkinter import ttk



class CorrelationView:



    def __init__(self, parent):


        self.frame = ttk.Frame(

            parent

        )


        self.create_widgets()



    def create_widgets(self):


        title = ttk.Label(

            self.frame,

            text="CORRELATION ANALYSIS",

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

            "product",

            "serial",

            "drive",

            "confidence",

            "reasons"

        )



        self.table = ttk.Treeview(

            self.frame,

            columns=columns,

            show="headings"

        )



        self.table.heading(

            "product",

            text="USB Product"

        )


        self.table.heading(

            "serial",

            text="Serial Number"

        )


        self.table.heading(

            "drive",

            text="Mounted Drive"

        )


        self.table.heading(

            "confidence",

            text="Confidence"

        )


        self.table.heading(

            "reasons",

            text="Correlation Reasons"

        )



        self.table.column(

            "product",

            width=150

        )


        self.table.column(

            "serial",

            width=180

        )


        self.table.column(

            "drive",

            width=100

        )


        self.table.column(

            "confidence",

            width=100

        )


        self.table.column(

            "reasons",

            width=350

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



    def show_correlations(self, correlations):


        for item in self.table.get_children():

            self.table.delete(

                item

            )



        if not correlations:


            self.table.insert(

                "",

                "end",

                values=(

                    "",

                    "",

                    "",

                    "0%",

                    "No correlation results available"

                )

            )


            return



        for correlation in correlations:



            reasons = correlation.get(

                "reasons",

                []

            )



            self.table.insert(

                "",

                "end",

                values=(


                    correlation.get(

                        "product",

                        "UNKNOWN"

                    ),


                    correlation.get(

                        "serial_number",

                        "UNKNOWN"

                    ),


                    correlation.get(

                        "drive_letter",

                        "UNKNOWN"

                    ),


                    f"{correlation.get('confidence',0)}%",


                    ", ".join(

                        reasons

                    )

                )

            )



    def get_frame(self):


        return self.frame