import win32evtlog
import win32evtlogutil

from collector.base_collector import BaseCollector
from utils.time_utils import TimeUtils


class EventLogCollector(BaseCollector):

    """
    Collects meaningful USB forensic events
    from Windows System Event Log.
    """


    LOG_TYPE = "System"


    # Providers that generate noise
    IGNORE_SOURCES = [

        "storahci",

        "Microsoft-Windows-HAL",

        "Microsoft-Windows-Kernel-Boot",

        "Disk",

        "Ntfs"

    ]


    # Useful USB related providers

    USB_SOURCES = [

        "Microsoft-Windows-UserPnp",

        "Microsoft-Windows-Kernel-PnP",

        "DriverFrameworks-UserMode",

        "USBSTOR"

    ]


    # Important USB event IDs

    USB_EVENT_IDS = [

        2003,   # USB device started

        2001,   # USB device installed

        2100,

        2102,

        10000,

        10001

    ]


    def collect(self):

        events = []


        try:

            print("[+] Opening Windows Event Log...")


            handle = win32evtlog.OpenEventLog(

                None,

                self.LOG_TYPE

            )


            flags = (

                win32evtlog.EVENTLOG_BACKWARDS_READ |

                win32evtlog.EVENTLOG_SEQUENTIAL_READ

            )


            print("[+] Event Log Opened Successfully")


            while True:


                records = win32evtlog.ReadEventLog(

                    handle,

                    flags,

                    0

                )


                if not records:

                    break



                for record in records:


                    event_id = record.EventID & 0xFFFF


                    source = record.SourceName or ""


                    source_lower = source.lower()



                    # Remove noisy providers

                    if any(

                        noise.lower() in source_lower

                        for noise in self.IGNORE_SOURCES

                    ):

                        continue



                    description = self.get_description(record)



                    source_match = any(

                        usb.lower() in source_lower

                        for usb in self.USB_SOURCES

                    )


                    id_match = event_id in self.USB_EVENT_IDS



                    if not (source_match or id_match):

                        continue



                    timestamp = TimeUtils.format_timestamp(

                        record.TimeGenerated.timestamp()

                    )


                    classification = self.classify_event(

                        event_id

                    )



                    events.append({


                        "event_id": event_id,


                        "source": source,


                        "time": timestamp,


                        "activity": classification["activity"],


                        "category": classification["category"],


                        "description": classification["description"],


                        "raw_description": description

                    })

                    print("\nUSB EVENT DEBUG")
                    print("Event ID:", event_id)
                    print("Source:", source)
                    print("Raw:", description[:300])



            win32evtlog.CloseEventLog(handle)



            print(

                f"[+] USB Events Collected: {len(events)}"

            )


        except Exception as error:


            print(

                "[Event Log Collector Error]",

                error

            )


        return events




    def classify_event(self, event_id):


        if event_id in [2001, 2003]:


            return {


                "activity":

                "USB_DEVICE_CONNECTED",


                "category":

                "USB Connection",


                "description":

                "USB storage device connection detected"

            }



        if event_id in [2100,2102]:


            return {


                "activity":

                "USB_DRIVER_INSTALLATION",


                "category":

                "Driver Installation",


                "description":

                "USB device driver installation detected"

            }



        if event_id in [10000,10001]:


            return {


                "activity":

                "USB_DEVICE_OPERATION",


                "category":

                "USB Activity",


                "description":

                "USB device operational event detected"

            }



        return {


            "activity":

            "USB_EVENT",


            "category":

            "USB Activity",


            "description":

            "USB related Windows event detected"

        }





    def get_description(self, record):


        try:


            message = win32evtlogutil.SafeFormatMessage(

                record,

                self.LOG_TYPE

            )


            if message:


                return message.strip()



        except Exception:

            pass



        if record.StringInserts:


            return " | ".join(

                str(x)

                for x in record.StringInserts

            )



        return (

            f"Provider: {record.SourceName} "

            f"Event ID: {record.EventID & 0xFFFF}"

        )