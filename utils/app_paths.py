from pathlib import Path


class AppPaths:
    """
    Stores all writable application folders.

    Windows:
    C:\\Users\\<User>\\Desktop\\USB Forensics Analyzer
    """

    DESKTOP = Path.home() / "Desktop"

    APP_DIR = DESKTOP / "USB Forensics Analyzer"

    DATABASE_DIR = APP_DIR / "Database"

    OUTPUT_DIR = APP_DIR / "Reports"

    EXPORTS_DIR = APP_DIR / "Exports"

    LOGS_DIR = APP_DIR / "Logs"

    @staticmethod
    def initialize():
        """
        Create required folders.
        """

        AppPaths.APP_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        AppPaths.DATABASE_DIR.mkdir(
            exist_ok=True
        )

        AppPaths.OUTPUT_DIR.mkdir(
            exist_ok=True
        )

        AppPaths.EXPORTS_DIR.mkdir(
            exist_ok=True
        )

        AppPaths.LOGS_DIR.mkdir(
            exist_ok=True
        )