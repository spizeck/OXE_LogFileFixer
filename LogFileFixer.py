import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

import pandas as pd
import ttkbootstrap as ttkb

# Presets filepath
PRESETS_FILE_PATH = 'presets.json'


class PresetManager:
    @staticmethod
    def load_presets():
        if not os.path.exists(PRESETS_FILE_PATH):
            return {}

        with open(PRESETS_FILE_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_presets(presets):
        with open(PRESETS_FILE_PATH, 'w') as f:
            json.dump(presets, f)

    @staticmethod
    def save_preset(name, headers):
        presets = PresetManager.load_presets()
        presets[name] = headers
        PresetManager.save_presets(presets)

    @staticmethod
    def get_preset(name):
        presets = PresetManager.load_presets()
        return presets.get(name, [])


class CSVHandler:
    @staticmethod
    def load_file(file_path):
        try:
            return pd.read_csv(file_path, dtype=str)
        except Exception as e:
            messagebox.showerror(
                'Error', f'Failed to load CSV file. Error: {str(e)}')
            return None

    @staticmethod
    def save_file(df, headers, file_path):
        try:
            new_df = df[headers]
            new_df.to_csv(file_path, index=False)
        except Exception as e:
            messagebox.showerror(
                'Error', f'Failed to save CSV file. Error: {str(e)}')
            return False

        return True


class App:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.style = ttkb.Style(theme='lumen')
        self.root.title('OXE Log File Fixer by Chad')
        self.root.geometry('500x500')

        frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10)

        button = ttkb.Button(
            root, text='Create New CSV with Selected Columns', command=self.on_button_click)
        button.pack(pady=15)

        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=80)
        self.listbox.pack(fill='both', side=tk.LEFT)

        scrollbar = ttk.Scrollbar(
            root, orient='vertical', command=self.listbox.yview)
        scrollbar.pack(fill='y', side=tk.RIGHT)

        for column in self.df.columns:
            self.listbox.insert(tk.END, column)

        self.preset_var = tk.StringVar(root)
        self.preset_var.set(None)
        presets = PresetManager.load_presets()
        self.preset_menu = ttk.OptionMenu(
            root, self.preset_var, None, *presets.keys(), command=self.on_preset_select)
        self.preset_menu.pack()

        self.save_preset_button = ttkb.Button(
            root, text='Save current selection as preset', command=self.on_save_preset)
        self.save_preset_button.pack()

    def on_button_click(self):
        selected_indices = self.listbox.curselection()
        selected_headers = [self.listbox.get(i) for i in selected_indices]

        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", initialfile=f'new_file_{datetime.now().strftime("%Y%m%d%H%M%S")}')
        if not output_file_path:
            return

        if CSVHandler.save_file(self.df, selected_headers, output_file_path):
            messagebox.showinfo(
                'Success', 'New CSV file has been created with selected headers.')
            self.root.destroy()

    def on_preset_select(self, preset_name):
        preset = PresetManager.get_preset(preset_name)
        self.listbox.select_clear(0, tk.END)
        for i, item in enumerate(self.listbox.get(0, tk.END)):
            if item in preset:
                self.listbox.select_set(i)

    def on_save_preset(self):
        if preset_name := tk.simpledialog.askstring(
            'Preset Name', 'Enter a name for the preset:'
        ):
            selected_indices = self.listbox.curselection()
            selected_headers = [self.listbox.get(i) for i in selected_indices]
            PresetManager.save_preset(preset_name, selected_headers)
            self.preset_menu['menu'].add_command(
                label=preset_name, command=tk._setit(self.preset_var, preset_name))


def main():
    file_path = filedialog.askopenfilename()
    df = CSVHandler.load_file(file_path)
    if df is not None:
        root = tk.Tk()
        app = App(root, df)
        root.mainloop()


if __name__ == "__main__":
    main()
