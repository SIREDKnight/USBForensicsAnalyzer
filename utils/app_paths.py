from pathlib import Path
import os


class AppPaths:
    """
    Stores all writable application folders.

    Windows:
    C:\\Users\\<User>\\AppData\\Local\\USBForensicsAnalyzer
    """

    APP_DIR = (
        Path(os.getenv("LOCALAPPDATA"))
        / "USBForensicsAnalyzer"
    )

    DATABASE_DIR = APP_DIR / "database"

    OUTPUT_DIR = APP_DIR / "output"

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