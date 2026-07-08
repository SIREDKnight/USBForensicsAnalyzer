import tkinter as tk
from tkinter import messagebox

import getpass
from datetime import datetime

from manager.evidence_manager import EvidenceManager
from gui.dashboard import Dashboard



class CaseWindow:


    def __init__(self, parent):


        self.window = tk.Toplevel(parent)


        self.window.title(

            "Create Forensic Case"

        )


        self.window.geometry(

            "500x450"

        )


        self.window.configure(

            bg="#1e1e1e"

        )


        self.manager = EvidenceManager()


        self.create_interface()



    def create_interface(self):


        tk.Label(

            self.window,

            text="NEW FORENSIC INVESTIGATION",

            bg="#1e1e1e",

            fg="#00d9ff",

            font=(

                "Segoe UI",

                16,

                "bold"

            )

        ).pack(

            pady=25

        )



        tk.Label(

            self.window,

            text="Case Name",

            bg="#1e1e1e",

            fg="white"

        ).pack()



        self.case_name = tk.Entry(

            self.window,

            width=40

        )

        self.case_name.pack(

            pady=10

        )



        investigator = getpass.getuser()



        tk.Label(

            self.window,

            text=f"Investigator: {investigator}",

            bg="#1e1e1e",

            fg="white"

        ).pack(

            pady=10

        )



        timestamp = datetime.now().strftime(

            "%Y%m%d-%H%M%S"

        )


        self.case_id = f"CASE-{timestamp}"



        tk.Label(

            self.window,

            text=(

                f"Generated Case ID:\n{self.case_id}"

            ),

            bg="#1e1e1e",

            fg="white"

        ).pack(

            pady=20

        )



        tk.Button(

            self.window,

            text="START INVESTIGATION",

            width=25,

            height=2,

            command=self.start_case

        ).pack(

            pady=20

        )



    def start_case(self):


        name = self.case_name.get().strip()



        if not name:


            messagebox.showwarning(

                "Missing Case Name",

                "Enter a case name."

            )

            return



        investigator = getpass.getuser()



        self.manager.create_case(

            name,

            investigator,

            self.case_id

        )



        messagebox.showinfo(

            "Case Created",

            (

                f"Case ID: {self.case_id}\n"

                f"Investigator: {investigator}"

            )

        )



        self.window.destroy()



        Dashboard(

            self.manager

        )