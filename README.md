# OXE_LogFileFixer
Simple program to ingest OXE engine Log Files, and create new log files with only the data selected by the user.

Still working on getting the package to work as a standalone, but currently, running the program opens a dialog box where you can select
the log file, and it will open a listbox in Tkinter where you can select the headers that you want to keep. Clicking the button exports
a new CSV file with only the headers selected.
