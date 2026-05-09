"""
Application entry point.

This module initializes the configuration manager, creates the GUI
application instance, and starts the Tkinter event loop.
"""


from work.library.config import ConfigManager
from work.scripts.gui import App


def main() -> None:
    """
    Start the application.

    The function creates the configuration manager, initializes
    the GUI application, and launches the main event loop.
    """

    config_manager = ConfigManager()
    app = App(config_manager)
    app.run()


if __name__ == "__main__":
    main()
