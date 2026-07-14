class TimestampEvaluator:



    @staticmethod
    def evaluate(artifact):


        if artifact == "EVENT_LOG":

            return (

                "EVENT_GENERATED",

                "HIGH"

            )



        if artifact == "USB_REGISTRY":

            return (

                "REGISTRY_LAST_WRITE",

                "MEDIUM"

            )



        if artifact == "MOUNTED_DEVICE":

            return (

                "REGISTRY_LAST_WRITE",

                "LOW"

            )



        return (

            "UNKNOWN",

            "LOW"

        )