from src.console import Console
import csv
import threading

class NotBash:
    path = "/"
    config = {
        "file_system": "",
        "start_script": "",
    }

    def __init__(self):
        self.console = Console(self.cmd_processing)

        # Load config
        with open('config.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                self.config[row[0]] = row[1]

    # Commands processing

    def _ls(self):
        pass
    
    # Class methods

    def cmd_processing(self, command):
        print(command)
        return f"test"
    
    def run_start_script(self):
        if self.config["start_script"]:
            script = open(self.config["start_script"], "r")
            for line in script:
                self.console.print("$ " + line)
                self.console.print(self.cmd_processing(line))
            script.close()
        self.console.insert_prompt()
    
    def run(self):
        start_cmds = threading.Thread(target=self.run_start_script)
        start_cmds.start()  

        self.console.run()

if __name__ == "__main__":
    not_bash = NotBash()
    not_bash.run()
