# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from library.config.loader import load_config

class MainApp:
    def __init__(self, root):
        self.root = root
        load_config("../config/app_config.json")
        self.root.title("Financial Analyzer")
        self.root.geometry("1024x768")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.current_data = None
        self.create_home()
        self.create_data()
        self.create_ref()
        self.create_analysis()
        self.create_reports()
        self.create_config()
        self.create_help()
        self.status = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_home(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Home")
        tk.Label(tab, text="Financial Analysis Platform", font=("Arial", 18)).pack(pady=20)
        tk.Label(tab, text="Select a tab to start working").pack()

    def create_data(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Data")
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Load CSV", command=self.load_csv).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Save CSV", command=self.save_csv).pack(side=tk.LEFT)
        self.tree = ttk.Treeview(tab)
        self.tree.pack(fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            self.current_data = pd.read_csv(path)
            for row in self.tree.get_children(): self.tree.delete(row)
            columns = list(self.current_data.columns)
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            for col in columns: self.tree.heading(col, text=col)
            for _, row in self.current_data.head(100).iterrows(): self.tree.insert("", tk.END, values=list(row))
            self.status.set(f"Loaded {os.path.basename(path)}")
        except Exception as e: messagebox.showerror("Error", f"Failed to load file: {e}")

    def save_csv(self):
        if self.current_data is None: messagebox.showerror("Error", "No data to save")
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            try:
                self.current_data.to_csv(path, index=False)
                self.status.set(f"Saved {os.path.basename(path)}")
            except Exception as e: messagebox.showerror("Error", f"Failed to save: {e}")

    def create_ref(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="References")
        tk.Label(tab, text="Tickers").pack()
        self.listbox = tk.Listbox(tab)
        self.listbox.pack()
        for t in ["AAPL", "MSFT", "GOOG"]: self.listbox.insert(tk.END, t)

    def create_analysis(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Analysis")
        ctrl = ttk.Frame(tab)
        ctrl.pack(fill=tk.X)
        self.fig = plt.Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_reports(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reports")
        ttk.Button(tab, text="Generate CSV Report", command=self.make_report).pack()
        self.report = tk.Text(tab, height=15)
        self.report.pack(fill=tk.BOTH, expand=True)

    def make_report(self):
        if self.current_data is None: self.report.insert(tk.END, "No data loaded. Please load a CSV first.\n")
        else:
            os.makedirs("output", exist_ok=True)
            path = "output/report.csv"
            try:
                self.current_data.to_csv(path, index=False)
                self.report.insert(tk.END, f"Report saved to {path}\n")
                self.status.set("Report created")
            except Exception as e: self.report.insert(tk.END, f"Error saving report: {e}\n")

    def create_config(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Config")
        self.config_text = tk.Text(tab, height=20)
        self.config_text.pack(fill=tk.BOTH, expand=True)
        try:
            with open("config/app_config.json", "r", encoding="utf-8") as f: self.config_text.insert(tk.END, f.read())
        except: pass

    def create_help(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Help")
        tk.Label(tab, text="Financial Analysis System\nVersion 1.0\nUse tabs for data management, analysis and reporting.", justify=tk.LEFT).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
