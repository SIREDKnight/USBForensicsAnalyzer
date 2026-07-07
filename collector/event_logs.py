import win32evtlog

from collector.base_collector import BaseCollector


class EventLogCollector(BaseCollector):

    """
    Collects USB related Windows Event Logs.

    Primary source:
    Windows System Event Log

    Important USB-related sources:
    - Microsoft-Windows-UserPnp
    - Microsoft-Windows-Kernel-PnP
    - Microsoft-Windows-DriverFrameworks-UserMode
    """


    LOG_TYPE = "System"


    USB_SOURCES = [

        "Microsoft-Windows-UserPnp",

        "Microsoft-Windows-Kernel-PnP",

        "Microsoft-Windows-DriverFrameworks-UserMode"

    ]



    def collect(self):

        events = []


        try:

            handle = win32evtlog.OpenEventLog(
                "localhost",
                self.LOG_TYPE
            )


            flags = (

                win32evtlog.EVENTLOG_BACKWARDS_READ |

                win32evtlog.EVENTLOG_SEQUENTIAL_READ

            )


            while True:


                records = win32evtlog.ReadEventLog(
                    handle,
                    flags,
                    0
                )


                if not records:

                    break



                for event in records:


                    source = str(
                        event.SourceName
                    )


                    if not self.is_usb_event(source):

                        continue



                    events.append(

                        {

                            "event_id":
                            event.EventID,


                            "source":
                            source,


                            "time":
                            str(
                                event.TimeGenerated
                            ),


                            "description":
                            self.classify_event(
                                source,
                                event.EventID,
                                event.StringInserts
                            )

                        }

                    )



        except Exception as e:


            print(
                "[EventLogCollector Error]",
                e
            )



        return events




    def is_usb_event(self, source):

        for usb_source in self.USB_SOURCES:

            if usb_source.lower() in source.lower():

                return True


        return False




    def classify_event(
            self,
            source,
            event_id,
            data):


        source = source.lower()



        if "userpnp" in source:


            return (

                "USB device installation "
                "or connection detected"

            )



        elif "driverframeworks" in source:


            return (

                "USB driver activity detected"

            )



        elif "kernel-pnp" in source:


            return (

                "Plug and Play device event"

            )



        return (

            "USB related Windows event"

        )