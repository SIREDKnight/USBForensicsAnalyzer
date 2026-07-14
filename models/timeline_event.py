from dataclasses import dataclass, asdict
from datetime import datetime



@dataclass
class TimelineEvent:
    """
    Represents a forensic timeline event.

    Sources:
    - USB Registry artifacts
    - Mounted Device artifacts
    - Windows Event Logs

    Every artifact entering the forensic timeline
    must use this structure.
    """



    time: str

    artifact: str

    description: str

    event_id: int = None

    source: str = None

    evidence_type: str = None

    confidence: int = 0



    # ==================================================
    # TIMESTAMP NORMALIZATION
    # ==================================================

    def normalize_time(self):

        """
        Converts different Windows timestamp formats
        into a common forensic format.
        """



        if not self.time:

            self.time = "UNKNOWN"

            return self.time



        if str(self.time).upper() == "UNKNOWN":

            return "UNKNOWN"



        formats = [

            "%Y-%m-%d %H:%M:%S",

            "%Y-%m-%d %H:%M:%S.%f",

            "%m/%d/%Y %H:%M:%S",

            "%d/%m/%Y %H:%M:%S",

            "%a %b %d %H:%M:%S %Y"

        ]



        for fmt in formats:


            try:


                parsed = datetime.strptime(

                    str(self.time),

                    fmt

                )



                self.time = parsed.strftime(

                    "%Y-%m-%d %H:%M:%S"

                )



                return self.time



            except ValueError:


                continue



        return self.time





    # ==================================================
    # VALIDATION
    # ==================================================

    def is_valid(self):

        """
        Determines whether the event contains
        enough forensic information.
        """



        if not self.artifact:

            return False



        if not self.description:

            return False



        return True





    # ==================================================
    # DICTIONARY EXPORT
    # ==================================================

    def to_dict(self):

        """
        Convert timeline event into dictionary
        for database storage, reports, and hashing.
        """

        return asdict(self)





    # ==================================================
    # DISPLAY
    # ==================================================

    def __str__(self):


        return (

            "\nTIMELINE EVENT\n"

            "-------------------------\n"

            f"Time          : {self.time}\n"

            f"Artifact      : {self.artifact}\n"

            f"Evidence Type : {self.evidence_type}\n"

            f"Event ID      : {self.event_id}\n"

            f"Source        : {self.source}\n"

            f"Confidence    : {self.confidence}%\n"

            f"Description   : {self.description}\n"

        )