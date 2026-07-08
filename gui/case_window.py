import tkinter as tk
from tkinter import messagebox

import getpass
from datetime import datetime

from manager.evidence_manager import EvidenceManager
from gui.dashboard import Dashboard



class CaseWindow:


    def __init__(self, parent):


        self.parent = parent


        self.window = tk.Toplevel(parent)


        self.window.title(

            "Create Forensic Case"

        )


        self.window.geometry(

            "550x500"

        )


        self.window.configure(

            bg="#1e1e1e"

        )


        # Single EvidenceManager instance

        self.manager = EvidenceManager()


        self.create_interface()



    # ==================================================
    # CREATE INTERFACE
    # ==================================================

    def create_interface(self):


        title = tk.Label(

            self.window,

            text="NEW FORENSIC INVESTIGATION",

            bg="#1e1e1e",

            fg="#00d9ff",

            font=(

                "Segoe UI",

                18,

                "bold"

            )

        )


        title.pack(

            pady=25

        )



        # -------------------------------
        # CASE NAME
        # -------------------------------

        tk.Label(

            self.window,

            text="Case Name",

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                11

            )

        ).pack()



        self.case_entry = tk.Entry(

            self.window,

            width=45,

            font=(

                "Segoe UI",

                11

            )

        )


        self.case_entry.pack(

            pady=10

        )



        # -------------------------------
        # INVESTIGATOR
        # -------------------------------

        investigator = getpass.getuser()



        tk.Label(

            self.window,

            text=(

                f"Investigator: {investigator}"

            ),

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                11

            )

        ).pack(

            pady=10

        )



        # -------------------------------
        # CASE ID GENERATION
        # -------------------------------

        timestamp = datetime.now().strftime(

            "%Y%m%d-%H%M%S"

        )


        self.case_id = (

            f"CASE-{timestamp}"

        )



        tk.Label(

            self.window,

            text=(

                "Generated Case ID\n"

                f"{self.case_id}"

            ),

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                11,

                "bold"

            )

        ).pack(

            pady=20

        )



        # -------------------------------
        # START BUTTON
        # -------------------------------

        tk.Button(

            self.window,

            text="START INVESTIGATION",

            width=30,

            height=2,

            font=(

                "Segoe UI",

                11,

                "bold"

            ),

            command=self.create_case

        ).pack(

            pady=20

        )



    # ==================================================
    # CREATE CASE
    # ==================================================

    def create_case(self):


        case_name = self.case_entry.get().strip()



        if not case_name:


            messagebox.showwarning(

                "Missing Information",

                "Please enter a case name."

            )


            return



        investigator = getpass.getuser()



        try:


            self.manager.create_case(

                case_name,

                investigator,

                self.case_id

            )



            messagebox.showinfo(

                "Case Created",

                (

                    "Investigation created successfully.\n\n"

                    f"Case ID: {self.case_id}\n"

                    f"Investigator: {investigator}"

                )

            )



            self.window.destroy()



            Dashboard(

                self.manager

            )



        except Exception as error:


            messagebox.showerror(

                "Case Creation Error",

                str(error)

            )