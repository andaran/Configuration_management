import xml.etree.ElementTree as ET
import struct
import argparse

class Interpreter:
    def __init__(self, binary_file, result_file, memory_range):
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory = [0] * 256
        self.memory_range = memory_range

    def run(self):
        with open(self.binary_file, 'rb') as file:
            while command := file.read(6):
                args = struct.unpack("BBBBBB", command)
                self.execute_command(args)
        
        result = ET.Element("result")
        for i in range(*self.memory_range):
            mem_elem = ET.SubElement(result, "memory")
            mem_elem.set("address", str(i))
            mem_elem.text = str(self.memory[i])
        
        ET.indent(result, space="  ", level=0)
        tree = ET.ElementTree(result)
        tree.write(self.result_file)

    def execute_command(self, args):
        opcode, op1, op2, op3, op4, op5 = args

        match opcode:
            case 212:
                self.memory[op1] = op2
            case 211:
                address = self.memory[op2] + op3
                self.memory[op1] = self.memory[address]
            case 196:
                address = self.memory[op1]
                self.memory[address] = self.memory[op2]
            case 217:
                self.memory[op1] = int(self.memory[op1] < self.memory[op2])
            case _:
                raise ValueError(f"Unknown opcode: {opcode}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="путь к входному файлу")
    parser.add_argument("output_file", help="путь к выходному файлу")
    parser.add_argument("--memory_range", nargs=2, type=int, help="диапазон памяти для вывода результата")

    args = parser.parse_args()

    interpreter = Interpreter(args.input_file, args.output_file, tuple(args.memory_range))
    interpreter.run()
