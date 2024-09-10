from src.console import Console
import csv
import threading
import tarfile

class NotBash:
    path = "/"
    config = {
        "file_system": "",
        "start_script": "",
    }

    def __init__(self):
        self.console = Console(self.cmd_processing)

        # Load config
        with open('./config.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                self.config[row[0]] = row[1]

        # Set current path
        self.path = self.config["file_system"].replace(".tar", "") + "/"

    # --- Commands processing ---

    def _ls(self):
        elems = set()
        with tarfile.open(self.config["file_system"], "r") as tar:
            for member in tar.getmembers():
                if not member.name.startswith(self.path):
                    continue
                elems.add(member.name.split("/")[self.path.count("/")])     

        self.console.print("\n".join(elems))

    def _cd(self, path):
        self.path = self.path.replace("//", "/")
        if type(path) != list:
            path = path.split("/")
        if path[0] == "":
            return

        if path[0] == "..":
            if self.path == "./file_system/":
                return self._cd(path[1:])
            self.path = "/".join(self.path.split("/")[:-2]) + "/"
            return self._cd(path[1:])
        elif path[0] == ".":
            return self._cd(path[1:])
        else:
            with tarfile.open(self.config["file_system"], "r") as tar:
                for member in tar.getmembers():
                    if member.name == self.path + "/".join(path) and \
                       member.isdir():
                        break
                else:
                    self.console.print("No such directory")
                    return

            self.path += "/".join(path) + "/"
            self.path = self.path.replace("//", "/")

    # --- Class methods ---

    def cmd_processing(self, command):
        command = command.split(" ")
        match command[0]:
            case "ls":
                self._ls()
            case "cd":
                self._cd(command[1])
                new_path = self.path.replace(
                    self.config["file_system"].replace(".tar", ""), "")
                self.console.set_path(new_path)
                
        self.console.insert_prompt()
    
    def run_start_script(self):
        if self.config["start_script"]:
            script = open(self.config["start_script"], "r")
            self.console.insert_prompt()
            for line in script:
                line = line.strip()
                self.console.print(line)
                self.cmd_processing(line)
            script.close()
    
    def run(self):
        start_cmds = threading.Thread(target=self.run_start_script)
        start_cmds.start()  

        self.console.run()

if __name__ == "__main__":
    not_bash = NotBash()
    not_bash.run()
