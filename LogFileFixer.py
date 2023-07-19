import pandas as pd
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import filedialog, messagebox, ttk
from datetime import datetime


class CSVHandler:
    @staticmethod
    def load_file(file_path):
        try:
            return pd.read_csv(file_path, dtype=str)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load CSV file. Error: {str(e)}')
            return None

    @staticmethod
    def save_file(df, headers, file_path):
        try:
            new_df = df[headers]
            new_df.to_csv(file_path, index=False)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save CSV file. Error: {str(e)}')
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

        button = ttkb.Button(root, text='Create New CSV with Selected Columns', command=self.on_button_click)
        button.pack(pady=15)

        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=80)
        self.listbox.pack(fill='both', side=tk.LEFT)

        scrollbar = ttk.Scrollbar(root, orient='vertical', command=self.listbox.yview)
        scrollbar.pack(fill='y', side=tk.RIGHT)

        for column in self.df.columns:
            self.listbox.insert(tk.END, column)

    def on_button_click(self):
        selected_indices = self.listbox.curselection()
        selected_headers = [self.listbox.get(i) for i in selected_indices]

        output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=f'new_file_{datetime.now().strftime("%Y%m%d%H%M%S")}')
        if not output_file_path:
            return

        if CSVHandler.save_file(self.df, selected_headers, output_file_path):
            messagebox.showinfo('Success', 'New CSV file has been created with selected headers.')
            self.root.destroy()


def main():
    file_path = filedialog.askopenfilename()
    df = CSVHandler.load_file(file_path)
    if df is not None:
        root = tk.Tk()
        app = App(root, df)
        root.mainloop()


if __name__ == "__main__":
    main()

