import shlex
import os
import tkinter as tk
from tkinter import scrolledtext

import vfs
import cmds

root = None
entry = None
output_text = None
submit_button = None
input_var = None

vfs_path = None
cur_vfs = None
cur_path = None

ERR_MSG = "unknown command:"

def handle(a):
    l = shlex.split(a)

    cmd = ""
    if l:
        cmd = l[0]

    if cmd == "ls":
        return cmds.ls(cur_vfs, cur_path)
    if cmd == "cd":
        return [" ".join(l), 0]
    if cmd == "exit":
        root.quit()
        return ["", 0]
    if cmd == "vfs-save":
        if len(l) < 2:
            return ["Saving path is not specified", 1]
        res = cmds.vfs_save(cur_vfs, l[1])
        if res == 0:
            return ["Current VFS was successfully saved", 0]
        else:
            return ["VFS is not loaded", 1]

    return [f"{ERR_MSG} {cmd}", 1]


def print_to_console(string):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"{string}\n")
    output_text.config(state=tk.DISABLED)
    output_text.yview(tk.END)


def get_from_console():
    global input_var

    input_var = tk.StringVar()

    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.focus_set()

    root.wait_variable(input_var)

    user_input = input_var.get()
    input_var = None
    return user_input


def on_submit():
    global input_var
    user_input = entry.get()
    if not user_input.strip():
        return

    if input_var is not None:
        input_var.set(user_input)
        entry.delete(0, tk.END)
        return

    result = handle(user_input)
    print_to_console(f"> {user_input}")
    print_to_console(result[0])
    print(result)
    entry.delete(0, tk.END)


def start_procedure():
    # VFS
    print_to_console("Please, enter VFS path (or \"q\")")
    while True:
        global vfs_path
        vfs_path = get_from_console()
        print_to_console(f"> {vfs_path}")

        if (vfs_path == "q"):
            print_to_console("VFS skipped")
            vfs_path = None
            break
        if not (vfs_path.endswith(".csv")):
            print_to_console("VFS extension is not .csv")
            continue
        try:
            global cur_vfs
            cur_vfs = vfs.load_vfs(vfs_path)
            # print(cur_vfs)
        except FileNotFoundError:
            print_to_console("File not found")
            continue
        except BaseException:
            print_to_console("Wrong VFS format")

        if "/" not in cur_vfs.keys():
            print_to_console("Root dir is not found")
            continue

        print_to_console("VFS loaded")
        global cur_path
        cur_path = "/"
        break


    # End of VFS

    # Startup script
    print_to_console("Please, enter path for startup script (or \"q\")")
    while True:
        path = get_from_console()
        print_to_console(f"> {path}")

        if (path == "q"):
            print_to_console("Startup script skipped")
            break
        try:
            with open(path, 'r') as file:
                commands = file.readlines()
                for cmd in commands:
                    to_print = cmd.replace('\n', '')
                    print_to_console(f"> {to_print}")
                    res = handle(cmd)
                    if res[1] != 0:
                        print_to_console(f"Error occurred in startup script - {res[0]}")
                        break
                    print_to_console(res[0])
                break
        except BaseException:
            print_to_console("File not found")
            continue


if __name__ == "__main__":
    # global root, entry, output_text, submit_button

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

    root.after(100, start_procedure)

    root.mainloop()