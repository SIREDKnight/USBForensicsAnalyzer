from pathlib import Path
import os
import shutil

import tkinter as tk
from tkinter import messagebox, filedialog

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
    # INTERFACE
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



        case_frame = tk.LabelFrame(

            self.window,

            text="Active Investigation",

            bg="#1e1e1e",

            fg="white"

        )


        case_frame.pack(

            fill="x",

            padx=20

        )



        case = self.manager.database.get_latest_case()



        if case:


            case_text = (

                f"Case ID: {case[0]}     "

                f"Case Name: {case[1]}     "

                f"Investigator: {case[3]}"

            )


        else:


            case_text = "No active case"



        tk.Label(

            case_frame,

            text=case_text,

            bg="#1e1e1e",

            fg="white"

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



        self.usb_label = self.create_stat(

            stats,

            "USB DEVICES"

        )


        self.mount_label = self.create_stat(

            stats,

            "MOUNTED DRIVES"

        )


        self.timeline_label = self.create_stat(

            stats,

            "TIMELINE EVENTS"

        )


        self.correlation_label = self.create_stat(

            stats,

            "CORRELATIONS"

        )



        # ===============================
        # BUTTONS
        # ===============================

        buttons = tk.Frame(

            self.window,

            bg="#1e1e1e"

        )


        buttons.pack()



        options = [

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

                "OPEN / DOWNLOAD PDF",

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



        for i, item in enumerate(options):


            tk.Button(

                buttons,

                text=item[0],

                width=25,

                height=2,

                command=item[1]

            ).grid(

                row=i // 3,

                column=i % 3,

                padx=10,

                pady=10

            )



        self.status = tk.Label(

            self.window,

            text="Ready",

            bg="#1e1e1e",

            fg="#00ff99"

        )


        self.status.pack(

            pady=20

        )



    # ==================================================
    # STAT BOX
    # ==================================================

    def create_stat(self, parent, title):


        label = tk.Label(

            parent,

            text=f"{title}\n0",

            bg="#252526",

            fg="white",

            width=20,

            height=4,

            font=(

                "Segoe UI",

                11,

                "bold"

            )

        )


        label.pack(

            side="left",

            padx=10

        )


        return label



    # ==================================================
    # ACQUISITION
    # ==================================================

    def acquire(self):


        try:


            self.status.config(

                text="Collecting evidence..."

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

                text="Acquisition completed"

            )


            messagebox.showinfo(

                "Completed",

                "Forensic acquisition completed successfully."

            )


        except Exception as error:


            messagebox.showerror(

                "Error",

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


        TimelineView(

            self.timeline

        )



    # ==================================================
    # CORRELATIONS
    # ==================================================

    def open_correlations(self):

        print(self.correlations)

        CorrelationView(

            self.correlations

        )



    # ==================================================
    # PDF OPEN / DOWNLOAD
    # ==================================================

    def open_pdf(self):


        report = Path(

            "output/case_report.pdf"

        )



        if not report.exists():


            messagebox.showwarning(

                "Missing Report",

                "Generate the report first."

            )


            return



        choice = messagebox.askyesno(

            "PDF Report",

            "Open PDF report?\n\nChoose NO to save a copy."

        )



        if choice:


            os.startfile(

                report

            )


        else:


            destination = filedialog.asksaveasfilename(

                title="Save PDF Report",

                defaultextension=".pdf",

                filetypes=[

                    (

                        "PDF Files",

                        "*.pdf"

                    )

                ]

            )


            if destination:


                shutil.copy(

                    report,

                    destination

                )


                messagebox.showinfo(

                    "Saved",

                    "PDF report saved successfully."

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