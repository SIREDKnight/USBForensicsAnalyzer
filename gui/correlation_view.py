import tkinter as tk
from tkinter import ttk



class CorrelationView:


    def __init__(self, correlations):


        self.correlations = correlations


        self.window = tk.Toplevel()


        self.window.title(

            "USB Evidence Correlation Analysis"

        )


        self.window.geometry(

            "1100x650"

        )


        self.window.configure(

            bg="#1e1e1e"

        )


        self.create_interface()



    # ==================================================
    # CREATE INTERFACE
    # ==================================================

    def create_interface(self):


        title = tk.Label(

            self.window,

            text="FORENSIC CORRELATION ANALYSIS",

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



        subtitle = tk.Label(

            self.window,

            text=(

                "Relationship analysis between USB devices "

                "and mounted storage volumes"

            ),

            bg="#1e1e1e",

            fg="white"

        )


        subtitle.pack()



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

            pady=20

        )



        columns = (

            "device",

            "manufacturer",

            "serial",

            "drive",

            "confidence"

        )



        self.table = ttk.Treeview(

            frame,

            columns=columns,

            show="headings"

        )



        headings = {

            "device":

            "USB Device",


            "manufacturer":

            "Manufacturer",


            "serial":

            "Serial Number",


            "drive":

            "Drive",


            "confidence":

            "Confidence"

        }



        for column, text in headings.items():


            self.table.heading(

                column,

                text=text

            )



        self.table.column(

            "device",

            width=200

        )


        self.table.column(

            "manufacturer",

            width=160

        )


        self.table.column(

            "serial",

            width=260

        )


        self.table.column(

            "drive",

            width=100

        )


        self.table.column(

            "confidence",

            width=120

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



        self.load_results()



        # ===============================
        # DETAILS PANEL
        # ===============================

        details_title = tk.Label(

            self.window,

            text="Supporting Evidence",

            bg="#1e1e1e",

            fg="#00d9ff",

            font=(

                "Segoe UI",

                12,

                "bold"

            )

        )


        details_title.pack()



        self.details = tk.Text(

            self.window,

            height=8,

            width=120,

            bg="#252526",

            fg="white"

        )


        self.details.pack(

            padx=20,

            pady=10

        )



        self.table.bind(

            "<<TreeviewSelect>>",

            self.show_details

        )



    # ==================================================
    # LOAD RESULTS
    # ==================================================

    def load_results(self):


        if not self.correlations:


            self.table.insert(

                "",

                "end",

                values=(

                    "No matches",

                    "",

                    "",

                    "",

                    "0%"

                )

            )


            return



        for item in self.correlations:


            self.table.insert(

                "",

                "end",

                values=(

                    item.get(

                        "product",

                        "UNKNOWN"

                    ),


                    item.get(

                        "manufacturer",

                        "UNKNOWN"

                    ),


                    item.get(

                        "serial_number",

                        "UNKNOWN"

                    ),


                    item.get(

                        "drive_letter",

                        "UNKNOWN"

                    ),


                    f"{item.get('confidence',0)}%"

                )

            )



    # ==================================================
    # SHOW DETAILS
    # ==================================================

    def show_details(self, event):


        selected = self.table.selection()



        if not selected:


            return



        index = self.table.index(

            selected[0]

        )



        if index >= len(self.correlations):


            return



        result = self.correlations[index]



        self.details.delete(

            "1.0",

            "end"

        )



        self.details.insert(

            "end",

            f"Device: {result.get('product')}\n"

        )


        self.details.insert(

            "end",

            f"Manufacturer: {result.get('manufacturer')}\n"

        )


        self.details.insert(

            "end",

            f"Drive: {result.get('drive_letter')}\n"

        )


        self.details.insert(

            "end",

            f"Confidence Score: {result.get('confidence')}%\n\n"

        )


        self.details.insert(

            "end",

            "Correlation Reasons:\n"

        )



        for reason in result.get(

                "reasons",

                []):


            self.details.insert(

                "end",

                f"- {reason}\n"

            )