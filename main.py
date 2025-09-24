import shlex
import os
import tkinter as tk
from tkinter import scrolledtext

def handle(a):
    l = shlex.split(a)

    cmd = ""
    if l:
        cmd = l[0]

    if cmd == "ls" or cmd == "cd":
        return " ".join(l)
    if cmd == "exit":
        root.quit()
        return ""

    return f"unknown command: {cmd}"

def start_script(start_path):
    with open(start_path, 'r') as file:
        commands = file.readlines()
        for cmd in commands:
            print_to_console(handle(cmd))


def print_to_console(string):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"{string}\n")
    output_text.config(state=tk.DISABLED)


def on_submit():
    user_input = entry.get()
    if not user_input.strip():
        return

    result = handle(user_input)

    print_to_console(f"> {user_input}")
    print_to_console(f"{result}")

    entry.delete(0, tk.END)
    output_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    current_dir = os.getcwd()
    root.title(f"Эмулятор — {current_dir}")


    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED)
    output_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    entry = tk.Entry(root, width=60)
    entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    submit_button = tk.Button(root, text="Отправить", command=on_submit)
    submit_button.grid(row=1, column=1, padx=5, pady=5)
    entry.bind("<Return>", lambda event: on_submit())
    root.grid_columnconfigure(0, weight=1)
    entry.focus_set()
    root.mainloop()