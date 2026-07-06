import win32evtlog
from collector.base_collector import BaseCollector


class EventLogCollector(BaseCollector):

    LOG_TYPE = "System"

    def collect(self):

        events = []

        server = "localhost"
        logtype = self.LOG_TYPE

        hand = win32evtlog.OpenEventLog(server, logtype)

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

        total = win32evtlog.GetNumberOfEventLogRecords(hand)

        while True:

            records = win32evtlog.ReadEventLog(hand, flags, 0)

            if not records:
                break

            for event in records:

                # USB-related event filtering
                if event.EventID in [2003, 2001, 2100, 2102]:

                    events.append({
                        "event_id": event.EventID,
                        "source": str(event.SourceName),
                        "time": str(event.TimeGenerated),
                        "description": str(event.StringInserts)
                    })

        return events