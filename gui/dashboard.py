import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import os

from gui.timeline_view import TimelineView
from gui.correlation_view import CorrelationView



class Dashboard:


    def __init__(self, manager):

        self.manager = manager


        self.devices = []

        self.mounted = []

        self.correlations = []

        self.timeline = []



        self.window = tk.Toplevel()


        self.window.title(

            "USB Forensics Analyzer - Dashboard"

        )


        self.window.geometry(

            "1200x750"

        )


        self.window.configure(

            bg="#1e1e1e"

        )


        self.create_interface()



    # ==================================================
    # MAIN INTERFACE
    # ==================================================

    def create_interface(self):


        title = tk.Label(

            self.window,

            text="FORENSIC INVESTIGATION DASHBOARD",

            bg="#1e1e1e",

            fg="#00d9ff",

            font=(

                "Segoe UI",

                20,

                "bold"

            )

        )


        title.pack(

            pady=20

        )



        # ===============================
        # CASE INFORMATION
        # ===============================

        case_frame = tk.LabelFrame(

            self.window,

            text="Active Investigation",

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                11,

                "bold"

            )

        )


        case_frame.pack(

            fill="x",

            padx=20

        )



        case = self.manager.database.get_latest_case()



        if case:

            case_info = (

                f"Case ID: {case['case_id']}    "

                f"Case Name: {case['case_name']}    "

                f"Investigator: {case['investigator']}"

            )

        else:

            case_info = "No active case"



        tk.Label(

            case_frame,

            text=case_info,

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                11

            )

        ).pack(

            pady=10

        )



        # ===============================
        # STATISTICS
        # ===============================

        stats = tk.Frame(

            self.window,

            bg="#1e1e1e"

        )


        stats.pack(

            pady=20

        )



        self.usb_label = self.stat_box(

            stats,

            "USB DEVICES"

        )


        self.mount_label = self.stat_box(

            stats,

            "MOUNTED DRIVES"

        )


        self.timeline_label = self.stat_box(

            stats,

            "TIMELINE EVENTS"

        )


        self.correlation_label = self.stat_box(

            stats,

            "CORRELATIONS"

        )



        # ===============================
        # CONTROL BUTTONS
        # ===============================

        controls = tk.Frame(

            self.window,

            bg="#1e1e1e"

        )


        controls.pack(

            pady=20

        )



        buttons = [

            (

                "START ACQUISITION",

                self.acquire

            ),

            (

                "VIEW TIMELINE",

                self.open_timeline

            ),

            (

                "VIEW CORRELATIONS",

                self.open_correlations

            ),

            (

                "OPEN PDF REPORT",

                self.open_pdf

            ),

            (

                "EXPORT CASE",

                self.export_case

            ),

            (

                "EXIT",

                self.window.destroy

            )

        ]



        for index, item in enumerate(buttons):


            tk.Button(

                controls,

                text=item[0],

                width=22,

                height=2,

                command=item[1]

            ).grid(

                row=index // 3,

                column=index % 3,

                padx=10,

                pady=10

            )



        # ===============================
        # STATUS
        # ===============================

        self.status = tk.Label(

            self.window,

            text="Ready",

            bg="#1e1e1e",

            fg="#00ff99",

            font=(

                "Segoe UI",

                11

            )

        )


        self.status.pack(

            pady=20

        )



    # ==================================================
    # STAT BOX
    # ==================================================

    def stat_box(self, parent, title):


        frame = tk.Frame(

            parent,

            bg="#252526",

            width=220,

            height=100

        )


        frame.pack(

            side="left",

            padx=15

        )


        label = tk.Label(

            frame,

            text=f"{title}\n0",

            bg="#252526",

            fg="white",

            font=(

                "Segoe UI",

                12,

                "bold"

            )

        )


        label.pack(

            padx=25,

            pady=25

        )


        return label



    # ==================================================
    # ACQUISITION
    # ==================================================

    def acquire(self):


        try:


            self.status.config(

                text="Collecting forensic evidence..."

            )


            self.window.update()



            (

                self.devices,

                self.mounted,

                self.correlations,

                self.timeline

            ) = self.manager.collect()



            self.update_statistics()



            self.status.config(

                text="Acquisition completed successfully"

            )


            messagebox.showinfo(

                "Completed",

                "Forensic acquisition completed successfully."

            )



        except Exception as error:


            messagebox.showerror(

                "Acquisition Error",

                str(error)

            )



    # ==================================================
    # UPDATE COUNTERS
    # ==================================================

    def update_statistics(self):


        self.usb_label.config(

            text=f"USB DEVICES\n{len(self.devices)}"

        )


        self.mount_label.config(

            text=f"MOUNTED DRIVES\n{len(self.mounted)}"

        )


        self.timeline_label.config(

            text=f"TIMELINE EVENTS\n{len(self.timeline)}"

        )


        self.correlation_label.config(

            text=f"CORRELATIONS\n{len(self.correlations)}"

        )



    # ==================================================
    # TIMELINE
    # ==================================================

    def open_timeline(self):


        if not self.timeline:


            messagebox.showwarning(

                "No Data",

                "Run acquisition first."

            )


            return



        TimelineView(

            self.timeline

        )



    # ==================================================
    # CORRELATIONS
    # ==================================================

    def open_correlations(self):


        if not self.correlations:


            messagebox.showwarning(

                "No Data",

                "Run acquisition first."

            )


            return



        CorrelationView(

            self.correlations

        )



    # ==================================================
    # PDF
    # ==================================================

    def open_pdf(self):


        report = Path(

            "output/case_report.pdf"

        )



        if report.exists():


            os.startfile(

                report

            )


        else:


            messagebox.showwarning(

                "Missing Report",

                "Generate report first."

            )



    # ==================================================
    # EXPORT
    # ==================================================

    def export_case(self):


        try:


            self.manager.export_case()



            messagebox.showinfo(

                "Export Complete",

                "Case bundle exported successfully."

            )


        except Exception as error:


            messagebox.showerror(

                "Export Error",

                str(error)

            )