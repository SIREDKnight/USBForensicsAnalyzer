import tkinter as tk
from tkinter import messagebox

from gui.styles import GUIStyles
from gui.case_window import CaseWindow



class USBForensicsApp:


    def __init__(self):

        self.root = tk.Tk()

        GUIStyles.configure_window(

            self.root

        )

        GUIStyles.apply(

            self.root

        )


        self.create_interface()



    # ==================================================
    # MAIN WINDOW
    # ==================================================

    def create_interface(self):


        # ==============================
        # HEADER
        # ==============================

        header = tk.Frame(

            self.root,

            bg="#1e1e1e"

        )

        header.pack(

            fill="x",

            pady=20

        )



        title = tk.Label(

            header,

            text="USB FORENSICS ANALYZER",

            bg="#1e1e1e",

            fg="#00d9ff",

            font=(

                "Segoe UI",

                24,

                "bold"

            )

        )


        title.pack()



        subtitle = tk.Label(

            header,

            text="Digital Forensics & Incident Response Platform",

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                12

            )

        )


        subtitle.pack()



        # ==============================
        # CENTER PANEL
        # ==============================

        panel = tk.Frame(

            self.root,

            bg="#1e1e1e"

        )

        panel.pack(

            expand=True

        )



        description = tk.Label(

            panel,

            text=(

                "Automated Windows USB Artifact Collection\n"

                "Registry Analysis | Event Correlation | Evidence Reporting"

            ),

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                12

            )

        )


        description.pack(

            pady=40

        )



        create_button = tk.Button(

            panel,

            text="CREATE NEW FORENSIC CASE",

            width=35,

            height=2,

            font=(

                "Segoe UI",

                12,

                "bold"

            ),

            command=self.open_case_window

        )


        create_button.pack(

            pady=20

        )



        exit_button = tk.Button(

            panel,

            text="EXIT",

            width=20,

            command=self.root.destroy

        )


        exit_button.pack()



        # ==============================
        # FOOTER
        # ==============================

        footer = tk.Label(

            self.root,

            text=(

                "USB Forensics Analyzer - DFIR Edition"

            ),

            bg="#1e1e1e",

            fg="#aaaaaa",

            font=(

                "Segoe UI",

                9

            )

        )


        footer.pack(

            side="bottom",

            pady=15

        )



    # ==================================================
    # CASE WINDOW
    # ==================================================

    def open_case_window(self):


        CaseWindow(

            self.root

        )



    # ==================================================
    # START APPLICATION
    # ==================================================

    def run(self):


        self.root.mainloop()



if __name__ == "__main__":


    app = USBForensicsApp()

    app.run()