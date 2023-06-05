import pandas as pd
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import filedialog, messagebox, ttk


def load_file():
    file_path = filedialog.askopenfilename()
    df = pd.read_csv(file_path, dtype=str)
    return df


def select_headers(df):
    style = ttkb.Style(theme='lumen')
    root = style.master
    root.title('OXE Log File Fixer by Chad')
    root.geometry('500x500')

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10)

    def on_button_click():
        selected_indices = listbox.curselection()
        selected_headers = [listbox.get(i) for i in selected_indices]
        new_df = df[selected_headers]
        new_df.to_csv('new_file.csv', index=False)
        messagebox.showinfo('Success', 'New CSV file has been created with selected headers.')
        root.destroy()

    button = ttkb.Button(root, text='Create New CSV with Selected Columns', command=on_button_click)
    button.pack(pady=15)

    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=80)
    listbox.pack(fill='both', side=tk.LEFT)

    scrollbar = ttk.Scrollbar(root, orient='vertical', command=listbox.yview)
    scrollbar.pack(fill='y', side=tk.RIGHT)

    for column in df.columns:
        listbox.insert(tk.END, column)

    root.mainloop()


def main():
    df = load_file()
    select_headers(df)


if __name__ == "__main__":
    main()
