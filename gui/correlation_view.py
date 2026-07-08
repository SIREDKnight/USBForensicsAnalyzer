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

            "1000x600"

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

            "device",

            "manufacturer",

            "drive",

            "confidence"

        )



        self.table = ttk.Treeview(

            frame,

            columns=columns,

            show="headings"

        )



        self.table.heading(

            "device",

            text="USB Device"

        )


        self.table.heading(

            "manufacturer",

            text="Manufacturer"

        )


        self.table.heading(

            "drive",

            text="Drive"

        )


        self.table.heading(

            "confidence",

            text="Confidence"

        )



        self.table.column(

            "device",

            width=250

        )


        self.table.column(

            "manufacturer",

            width=200

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



        self.create_reason_box()



    # ==================================================
    # LOAD CORRELATIONS
    # ==================================================

    def load_results(self):


        for item in self.correlations:


            self.table.insert(

                "",

                "end",

                values=(

                    item.get(

                        "product",

                        "Unknown"

                    ),


                    item.get(

                        "manufacturer",

                        "Unknown"

                    ),


                    item.get(

                        "drive_letter",

                        "Unknown"

                    ),


                    f"{item.get('confidence',0)}%"

                )

            )



    # ==================================================
    # DETAILS BOX
    # ==================================================

    def create_reason_box(self):


        label = tk.Label(

            self.window,

            text="Correlation Evidence / Reasons",

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                12,

                "bold"

            )

        )


        label.pack(

            pady=10

        )



        self.reason_text = tk.Text(

            self.window,

            height=8,

            width=100,

            bg="#252526",

            fg="white"

        )


        self.reason_text.pack(

            padx=20,

            pady=10

        )



        self.table.bind(

            "<<TreeviewSelect>>",

            self.show_details

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



        result = self.correlations[index]



        self.reason_text.delete(

            "1.0",

            "end"

        )



        self.reason_text.insert(

            "end",

            f"Device: {result.get('product')}\n"

        )


        self.reason_text.insert(

            "end",

            f"Drive: {result.get('drive_letter')}\n"

        )


        self.reason_text.insert(

            "end",

            f"Confidence: {result.get('confidence')}%\n\n"

        )


        self.reason_text.insert(

            "end",

            "Supporting Evidence:\n"

        )



        for reason in result.get(

            "reasons",

            []

        ):


            self.reason_text.insert(

                "end",

                f"- {reason}\n"

            )