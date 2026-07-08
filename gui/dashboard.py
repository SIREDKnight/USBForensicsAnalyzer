import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import os


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
    # INTERFACE
    # ==================================================

    def create_interface(self):


        # ===============================
        # HEADER
        # ===============================

        header = tk.Label(

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


        header.pack(

            pady=20

        )



        # ===============================
        # CASE INFORMATION
        # ===============================

        case_frame = tk.LabelFrame(

            self.window,

            text="Current Case",

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



        case_text = (

            f"Case ID: {case['case_id']}     "

            f"Case Name: {case['case_name']}     "

            f"Investigator: {case['investigator']}"

        )



        tk.Label(

            case_frame,

            text=case_text,

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



        self.usb_count = self.create_stat_box(

            stats,

            "USB Devices",

            0

        )


        self.mount_count = self.create_stat_box(

            stats,

            "Mounted Drives",

            1

        )


        self.timeline_count = self.create_stat_box(

            stats,

            "Timeline Events",

            2

        )


        self.correlation_count = self.create_stat_box(

            stats,

            "Correlations",

            3

        )



        # ===============================
        # BUTTONS
        # ===============================

        buttons = tk.Frame(

            self.window,

            bg="#1e1e1e"

        )


        buttons.pack(

            pady=20

        )



        tk.Button(

            buttons,

            text="START ACQUISITION",

            width=25,

            height=2,

            command=self.run_acquisition

        ).grid(

            row=0,

            column=0,

            padx=10

        )



        tk.Button(

            buttons,

            text="OPEN PDF REPORT",

            width=25,

            height=2,

            command=self.open_pdf

        ).grid(

            row=0,

            column=1,

            padx=10

        )



        tk.Button(

            buttons,

            text="EXPORT CASE",

            width=25,

            height=2,

            command=self.export_case

        ).grid(

            row=0,

            column=2,

            padx=10

        )



        tk.Button(

            buttons,

            text="EXIT",

            width=20,

            command=self.window.destroy

        ).grid(

            row=0,

            column=3,

            padx=10

        )



        # ===============================
        # STATUS AREA
        # ===============================

        self.status = tk.Label(

            self.window,

            text="Ready for acquisition",

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

    def create_stat_box(

            self,

            parent,

            title,

            column):


        frame = tk.Frame(

            parent,

            bg="#252526",

            width=200,

            height=100

        )


        frame.grid(

            row=0,

            column=column,

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

            padx=30,

            pady=25

        )


        return label





    # ==================================================
    # ACQUISITION
    # ==================================================

    def run_acquisition(self):


        try:


            self.status.config(

                text="Collecting forensic artifacts..."

            )


            self.window.update()



            (

                self.devices,

                self.mounted,

                self.correlations,

                self.timeline

            ) = self.manager.collect()



            self.usb_count.config(

                text=f"USB Devices\n{len(self.devices)}"

            )


            self.mount_count.config(

                text=f"Mounted Drives\n{len(self.mounted)}"

            )


            self.timeline_count.config(

                text=f"Timeline Events\n{len(self.timeline)}"

            )


            self.correlation_count.config(

                text=f"Correlations\n{len(self.correlations)}"

            )



            self.status.config(

                text="Acquisition completed successfully"

            )



            messagebox.showinfo(

                "Complete",

                "Forensic acquisition completed."

            )



        except Exception as error:


            messagebox.showerror(

                "Acquisition Error",

                str(error)

            )





    # ==================================================
    # PDF
    # ==================================================

    def open_pdf(self):


        pdf = Path(

            "output/case_report.pdf"

        )


        if pdf.exists():


            os.startfile(

                pdf

            )


        else:


            messagebox.showwarning(

                "Missing Report",

                "Run acquisition first."

            )





    # ==================================================
    # EXPORT
    # ==================================================

    def export_case(self):


        try:


            self.manager.export_case()



            messagebox.showinfo(

                "Export Complete",

                "Case bundle exported."

            )


        except Exception as error:


            messagebox.showerror(

                "Export Error",

                str(error)

            )