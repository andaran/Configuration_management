import tkinter as tk
from tkinter import scrolledtext

class Console:
    bg_color = "#2e2e2e"
    text_color = "#ffffff"
    prompt_color = "#00ff00"

    def __init__(self, cmd_callback):
        self.cmd_callback = cmd_callback

        self.root = tk.Tk()
        self.root.title("Not Bash")

        self.console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, width=70, 
                                                 bg=self.bg_color, fg=self.text_color,
                                                 insertbackground=self.text_color)
        self.console.grid(row=0, column=0, padx=0, pady=0)
        self.console.bind('<Return>', self.execute_command)
        self.console.config(font=("Courier New", 12))

    def execute_command(self, event):
        input_text = self.console.get("1.0", tk.END)

        command = input_text.split("\n")[-2].strip()
        command = command.replace("$ ", "")

        if command == "exit":
            self.root.quit()
            return

        output = self.cmd_callback(command)
        self.console.insert(tk.END, "\n")
        self.print(output)
        self.insert_prompt()

        return "break"
    
    def print(self, text):
        self.console.insert(tk.END, f"{text}\n")
        self.console.mark_set("insert", tk.END)

    def insert_prompt(self):
        self.console.insert(tk.END, "$ ")
        self.console.mark_set("insert", tk.END)
    
    def run(self):
        self.root.mainloop()
