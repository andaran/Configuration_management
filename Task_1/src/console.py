import tkinter as tk
from tkinter import scrolledtext

class Console:
    bg_color = "#2e2e2e"
    text_color = "#ffffff"
    prompt_color = "#00ff00"
    prompt_user_color = "#00ff00"
    prompt_path_color = "#00bfff"

    def __init__(self, cmd_callback):
        self.cmd_callback = cmd_callback
        self.path = "/"

        self.root = tk.Tk()
        self.root.title("Not Bash")

        self.console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, width=70, 
                                                 bg=self.bg_color, fg=self.text_color,
                                                 insertbackground=self.text_color)
        self.console.grid(row=0, column=0, padx=0, pady=0)
        self.console.bind('<Return>', self.execute_command)
        self.console.config(font=("Courier New", 12))

        self.console.tag_configure("user", foreground=self.prompt_user_color)
        self.console.tag_configure("path", foreground=self.prompt_path_color)

    def execute_command(self, event):
        input_text = self.console.get("1.0", tk.END)

        command = input_text.split("\n")[-2].strip()
        command = command.split("$")[1].strip()

        if command == "exit":
            self.root.quit()
            return

        self.console.insert(tk.END, "\n")
        self.cmd_callback(command)

        return "break"
    
    def print(self, text=""):
        self.console.insert(tk.END, f"{text}\n")

    def insert_prompt(self):
        self.console.insert(tk.END, "user@computer", "user")
        self.console.insert(tk.END, f":{self.path}", "path")
        self.console.insert(tk.END, "$ ")
        self.console.mark_set("insert", tk.END)

    def set_path(self, path):
        self.path = path
    
    def run(self):
        self.root.mainloop()
