import xml.etree.ElementTree as ET
import struct
import argparse

class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file

    def assemble(self):
        with open(self.input_file, 'r') as infile, open(self.output_file, 'wb') as outfile:
            log = ET.Element("log")

            for line in infile:
                if line.startswith("#"):
                    continue
                if not line.strip():
                    continue

                parts = line.strip().split()
                parsed_parts = list(map(int, parts))
                if len(parts) < 6:
                    parsed_parts += [0] * (6 - len(parts))
                
                command = struct.pack("BBBBBB", *parsed_parts)
                outfile.write(command)
                
                cmd_log = ET.SubElement(log, "command")
                cmd_log.set("A", str(parts[0]))
                for i, operand in enumerate(parts[1:]):
                    cmd_log.set(chr(66 + i), str(operand))

            ET.indent(log, space="  ", level=0)
            tree = ET.ElementTree(log)
            tree.write(self.log_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="путь к входному файлу")
    parser.add_argument("output_file", help="путь к выходному файлу")
    parser.add_argument("--log_file", help="путь к файлу-логу")

    args = parser.parse_args()

    assembler = Assembler(args.input_file, args.output_file, args.log_file)
    assembler.assemble()