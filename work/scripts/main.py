import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library.config.loader import load_config
from scripts.gui.main_window import MainApp
import tkinter as tk

if __name__ == "__main__":
    load_config("../config/app_config.json")
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
