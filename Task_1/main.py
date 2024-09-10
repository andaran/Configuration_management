from src.console import Console

def cmd_callback(command):
    print(command)
    return f"test"

if __name__ == "__main__":
    console = Console(cmd_callback)
    console.run()
