import win32evtlog
from collector.base_collector import BaseCollector


class EventLogCollector(BaseCollector):

    LOG_TYPE = "System"


    USB_KEYWORDS = [
        "USB",
        "Kernel-PnP",
        "DriverFrameworks",
        "UserPnp"
    ]


    def collect(self):

        events = []

        server = "localhost"


        try:

            hand = win32evtlog.OpenEventLog(
                server,
                self.LOG_TYPE
            )


            flags = (
                win32evtlog.EVENTLOG_BACKWARDS_READ |
                win32evtlog.EVENTLOG_SEQUENTIAL_READ
            )


            while True:

                records = win32evtlog.ReadEventLog(
                    hand,
                    flags,
                    0
                )


                if not records:
                    break


                for event in records:


                    source = str(event.SourceName)


                    # Check if event relates to USB activity

                    if not any(
                        keyword.lower() in source.lower()
                        for keyword in self.USB_KEYWORDS
                    ):
                        continue


                    description = self.classify_event(
                        source,
                        event.EventID,
                        event.StringInserts
                    )


                    events.append({

                        "event_id": event.EventID,

                        "source": source,

                        "time": str(event.TimeGenerated),

                        "description": description

                    })


        except Exception as e:

            print(
                "[EventLogCollector Error]",
                e
            )


        return events



    # -----------------------------
    # EVENT CLASSIFICATION
    # -----------------------------
    def classify_event(
        self,
        source,
        event_id,
        data
    ):


        source = source.lower()


        if "userpnp" in source:

            return (
                "USB device installation "
                "or connection detected"
            )


        if "driverframeworks" in source:

            return (
                "USB driver activity detected"
            )


        if "kernel-pnp" in source:

            return (
                "Plug and Play device event"
            )


        return (
            "USB related system event"
        )