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

    def _tail(self, path):
        with tarfile.open(self.config["file_system"], "r") as tar:
            for member in tar.getmembers():
                if member.name == self.path + path and member.isfile():
                    break
            else:
                self.console.print("No such file")
                return

            with tar.extractfile(member) as f:
                lines = f.readlines()
                lines = [line.decode("utf-8") for line in lines]
                self.console.print("".join(lines[-min(len(lines), 10):]))

    def _du(self, path):
        with tarfile.open(self.config["file_system"], "r") as tar:
            for member in tar.getmembers():
                if member.name == self.path + path and member.isdir():
                    break
            else:
                self.console.print("No such directory")
                return
            
            total_size = 0
            for member in tar.getmembers():
                if member.name.startswith(self.path + path):
                    if not member.isfile():
                        continue

                    size = member.size
                    name = "/" + "/".join(member.name.split("/")[2:])

                    total_size += size
                    self.console.print(f"{size}\t{name}")

            self.console.print(f"Total size: {total_size} bytes")


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
            case "tail":
                self._tail(command[1])
            case "du":
                self._du(command[1])
            case _:
                self.console.print("Unknown command")

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
