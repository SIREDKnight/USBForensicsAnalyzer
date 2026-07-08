import tkinter as tk
from tkinter import ttk



class CorrelationView:


    def __init__(self, correlations):


        self.correlations = correlations


        self.window = tk.Toplevel()


        self.window.title(

            "Forensic Correlation Results"

        )


        self.window.geometry(

            "1100x700"

        )


        self.create_interface()



    # ==================================================
    # INTERFACE
    # ==================================================

    def create_interface(self):


        title = tk.Label(

            self.window,

            text="DEVICE CORRELATION ANALYSIS",

            font=(

                "Segoe UI",

                16,

                "bold"

            )

        )


        title.pack(

            pady=10

        )



        columns = (

            "product",

            "drive",

            "confidence"

        )



        self.table = ttk.Treeview(

            self.window,

            columns=columns,

            show="headings"

        )



        self.table.heading(

            "product",

            text="USB Device"

        )


        self.table.heading(

            "drive",

            text="Drive"

        )


        self.table.heading(

            "confidence",

            text="Confidence"

        )



        self.table.pack(

            fill="x",

            padx=20

        )



        for index, item in enumerate(self.correlations):


            self.table.insert(

                "",

                "end",

                iid=index,

                values=(

                    item.get(

                        "product",

                        "UNKNOWN"

                    ),

                    item.get(

                        "drive_letter",

                        "UNKNOWN"

                    ),

                    f"{item.get('confidence',0)}%"

                )

            )



        self.table.bind(

            "<<TreeviewSelect>>",

            self.show_details

        )



        self.details = tk.Text(

            self.window,

            height=20,

            width=120

        )


        self.details.pack(

            padx=20,

            pady=20

        )



    # ==================================================
    # DETAILS
    # ==================================================

    def show_details(self, event):


        selected = self.table.selection()



        if not selected:

            return



        index = int(

            selected[0]

        )


        result = self.correlations[index]

        print("VIEWER DATA:")
        print(result)



        self.details.delete(

            "1.0",

            tk.END

        )



        self.details.insert(

            tk.END,

            "CORRELATION DETAILS\n"

        )


        self.details.insert(

            tk.END,

            "=" * 60 + "\n\n"

        )



        self.details.insert(

            tk.END,

            f"Manufacturer: {result.get('manufacturer')}\n"

        )


        self.details.insert(

            tk.END,

            f"Product: {result.get('product')}\n"

        )


        self.details.insert(

            tk.END,

            f"Serial Number: {result.get('serial_number')}\n"

        )


        self.details.insert(

            tk.END,

            f"Drive: {result.get('drive_letter')}\n"

        )


        self.details.insert(

            tk.END,

            f"Confidence: {result.get('confidence')}%\n\n"

        )



        self.details.insert(

            tk.END,

            "SUPPORTING REASONS\n"

        )


        self.details.insert(

            tk.END,

            "-" * 60 + "\n"

        )



        for reason in result.get(

            "reasons",

            []

        ):


            self.details.insert(

                tk.END,

                f"- {reason}\n"

            )



        self.details.insert(

            tk.END,

            "\nSUPPORTING EVIDENCE\n"

        )


        self.details.insert(

            tk.END,

            "-" * 60 + "\n"

        )



        evidence = result.get(

            "evidence",

            {}

        )



        for key, value in evidence.items():


            self.details.insert(

                tk.END,

                f"{key}: {value}\n"

            )
