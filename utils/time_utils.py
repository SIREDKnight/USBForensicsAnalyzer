from datetime import datetime, timedelta



class TimeUtils:
    """
    Utility class for forensic timestamp handling.

    Supports:
    - Windows FILETIME timestamps
    - Unix timestamps
    - Python datetime objects
    - Timestamp strings
    """



    @staticmethod
    def format_timestamp(value):
        """
        Convert different timestamp formats into
        consistent forensic display format.
        """

        if value is None:

            return "UNKNOWN"



        # Already a datetime object

        if isinstance(value, datetime):

            return value.strftime(

                "%Y-%m-%d %H:%M:%S"

            )



        try:

            value = int(value)



            # ==================================================
            # Windows FILETIME
            #
            # 100-nanosecond intervals since:
            # 1601-01-01 UTC
            #
            # Example:
            # 134274737089563330
            # ==================================================

            if value > 100000000000000:


                epoch = datetime(

                    1601,

                    1,

                    1

                )


                converted = epoch + timedelta(

                    microseconds=value / 10

                )


                return converted.strftime(

                    "%Y-%m-%d %H:%M:%S"

                )



            # ==================================================
            # Unix timestamp
            #
            # Seconds since:
            # 1970-01-01
            # ==================================================

            return datetime.fromtimestamp(

                value

            ).strftime(

                "%Y-%m-%d %H:%M:%S"

            )



        except Exception:


            return str(value)



    @staticmethod
    def current_timestamp():

        """
        Generate current system timestamp
        for case creation and reports.
        """

        return datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )



    @staticmethod
    def parse_timestamp(value):

        """
        Convert timestamp string into datetime object
        for sorting and comparisons.
        """

        if not value:

            return None



        try:

            return datetime.strptime(

                value,

                "%Y-%m-%d %H:%M:%S"

            )



        except Exception:


            return None