import tkinter as tk

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


        # ===============================
        # HEADER
        # ===============================

        header = tk.Frame(

            self.root,

            bg="#1e1e1e"

        )


        header.pack(

            pady=40

        )



        title = tk.Label(

            header,

            text="USB FORENSICS ANALYZER",

            bg="#1e1e1e",

            fg="#00d9ff",

            font=(

                "Segoe UI",

                26,

                "bold"

            )

        )


        title.pack()



        subtitle = tk.Label(

            header,

            text=(

                "Digital Forensics & Incident Response Platform"

            ),

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                12

            )

        )


        subtitle.pack(

            pady=10

        )



        # ===============================
        # DESCRIPTION
        # ===============================

        body = tk.Frame(

            self.root,

            bg="#1e1e1e"

        )


        body.pack(

            expand=True

        )



        description = tk.Label(

            body,

            text=(

                "Automated Windows USB Artifact Collection\n\n"

                "• Registry Artifact Analysis\n"

                "• Event Log Investigation\n"

                "• Device Correlation\n"

                "• Evidence Reporting\n"

                "• Case Export Management"

            ),

            bg="#1e1e1e",

            fg="white",

            font=(

                "Segoe UI",

                12

            ),

            justify="center"

        )


        description.pack(

            pady=30

        )



        # ===============================
        # BUTTONS
        # ===============================

        tk.Button(

            body,

            text="CREATE NEW FORENSIC CASE",

            width=35,

            height=2,

            font=(

                "Segoe UI",

                12,

                "bold"

            ),

            command=self.open_case

        ).pack(

            pady=20

        )



        tk.Button(

            body,

            text="EXIT",

            width=20,

            command=self.root.destroy

        ).pack()



        # ===============================
        # FOOTER
        # ===============================

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
    # OPEN CASE WINDOW
    # ==================================================

    def open_case(self):


        CaseWindow(

            self.root

        )



    # ==================================================
    # START APPLICATION
    # ==================================================

    def run(self):


        self.root.mainloop()