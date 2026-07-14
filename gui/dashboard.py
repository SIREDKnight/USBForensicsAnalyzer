import tkinter as tk
from tkinter import ttk, messagebox
import datetime


from manager.evidence_manager import EvidenceManager

from gui.timeline_view import TimelineView
from gui.correlation_view import CorrelationView



class Dashboard:


    def __init__(self, root, manager=None):


        self.root = root


        self.root.title(
            "USB Forensics Analyzer"
        )


        self.root.geometry(
            "1100x700"
        )


        if manager:

            self.manager = manager

        else:

            self.manager = EvidenceManager()


        self.case_created = False


        self.create_interface()


    # ==================================================
    # GUI
    # ==================================================

    def create_interface(self):


        title = ttk.Label(

            self.root,

            text="USB FORENSICS ANALYZER",

            font=(
                "Arial",
                18,
                "bold"
            )

        )


        title.pack(

            pady=10

        )



        # ===============================
        # CASE FRAME
        # ===============================

        case_frame = ttk.LabelFrame(

            self.root,

            text="Case Information"

        )


        case_frame.pack(

            fill="x",

            padx=10,

            pady=10

        )



        ttk.Label(

            case_frame,

            text="Case Name"

        ).grid(

            row=0,

            column=0,

            padx=5,

            pady=5

        )


        self.case_name_entry = ttk.Entry(

            case_frame,

            width=30

        )


        self.case_name_entry.grid(

            row=0,

            column=1,

            padx=5

        )



        ttk.Label(

            case_frame,

            text="Investigator"

        ).grid(

            row=1,

            column=0,

            padx=5,

            pady=5

        )


        self.investigator_entry = ttk.Entry(

            case_frame,

            width=30

        )


        self.investigator_entry.grid(

            row=1,

            column=1,

            padx=5

        )



        ttk.Button(

            case_frame,

            text="Create Case",

            command=self.create_case

        ).grid(

            row=0,

            column=2,

            rowspan=2,

            padx=20

        )



        self.case_status = ttk.Label(

            case_frame,

            text="No active case"

        )


        self.case_status.grid(

            row=2,

            column=0,

            columnspan=3,

            pady=5

        )



        # ===============================
        # CONTROL BUTTONS
        # ===============================


        control_frame = ttk.Frame(

            self.root

        )


        control_frame.pack(

            pady=5

        )



        ttk.Button(

            control_frame,

            text="Run Acquisition",

            command=self.run_acquisition

        ).grid(

            row=0,

            column=0,

            padx=10

        )



        ttk.Button(

            control_frame,

            text="Export Case",

            command=self.export_case

        ).grid(

            row=0,

            column=1,

            padx=10

        )



        ttk.Button(

            control_frame,

            text="Exit",

            command=self.root.destroy

        ).grid(

            row=0,

            column=2,

            padx=10

        )



        # ===============================
        # VIEWS
        # ===============================


        self.notebook = ttk.Notebook(

            self.root

        )


        self.notebook.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )



        self.timeline_view = TimelineView(

            self.notebook

        )


        self.correlation_view = CorrelationView(

            self.notebook

        )



        self.notebook.add(

            self.timeline_view.get_frame(),

            text="Timeline"

        )


        self.notebook.add(

            self.correlation_view.get_frame(),

            text="Correlation"

        )



    # ==================================================
    # CREATE CASE
    # ==================================================

    def create_case(self):


        try:


            case_name = self.case_name_entry.get()


            investigator = self.investigator_entry.get()



            if not case_name or not investigator:


                messagebox.showwarning(

                    "Missing Data",

                    "Enter case name and investigator"

                )


                return



            generated_case_id = (

                "CASE-"

                +

                datetime.datetime.now()

                .strftime("%Y%m%d%H%M%S")

            )



            database_id = self.manager.create_case(

                case_name,

                investigator,

                generated_case_id

            )



            self.case_created = True



            self.case_status.config(

                text=(

                    f"Active Case: {generated_case_id}"

                )

            )


            messagebox.showinfo(

                "Case Created",

                f"Case created successfully\nID: {generated_case_id}"

            )



        except Exception as error:


            messagebox.showerror(

                "Case Error",

                str(error)

            )



    # ==================================================
    # ACQUISITION
    # ==================================================

    def run_acquisition(self):


        try:


            if not self.case_created:


                messagebox.showwarning(

                    "No Case",

                    "Create a case first"

                )


                return



            (

                devices,

                mounted,

                correlations,

                timeline

            ) = self.manager.collect()



            self.timeline_view.show_timeline(

                timeline

            )


            self.correlation_view.show_correlations(

                correlations

            )



            messagebox.showinfo(

                "Complete",

                "Acquisition completed"

            )



        except Exception as error:


            messagebox.showerror(

                "Acquisition Error",

                str(error)

            )



    # ==================================================
    # EXPORT
    # ==================================================

    def export_case(self):


        try:


            self.manager.export_case()



            messagebox.showinfo(

                "Export",

                "Case exported successfully"

            )



        except Exception as error:


            messagebox.showerror(

                "Export Error",

                str(error)

            )