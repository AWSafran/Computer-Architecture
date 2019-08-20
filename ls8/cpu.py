"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [None] * 256
        self.register = [None] * 8
        self.pc = 0
        self.running = True

    def ram_read(self, mem_address_register):
        mem_data_register = self.ram[mem_address_register]
        return mem_data_register

    def ram_write(self, mem_address_register, mem_data_register):
        self.ram[mem_address_register] = mem_data_register

    def load(self, argfile):
        """Load a program into memory."""

        address = 0
        program = []

        f = open(f'examples/{argfile}', 'r')
        commands = f.read().split('\n')
        f.close()

        # Pull the binary and convert it from string
        for command in commands:
            if len(command) >= 8:
                binary = command[:8]
                program.append(int(binary, base=2))


        for instruction in program:
            self.ram_write(address, instruction)
            address += 1


        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def prn(self, instruction_register):
        operand_a = self.ram_read(instruction_register + 1)
        print(self.register[operand_a])
        return instruction_register + 1

    def ldi(self, instruction_register):
        operand_a = self.ram_read(instruction_register + 1)
        operand_b = self.ram_read(instruction_register + 2)
        self.register[operand_a] = operand_b
        return instruction_register + 2

    def mul(self, instruction_register):
        operand_a = self.ram_read(instruction_register + 1)
        operand_b = self.ram_read(instruction_register + 2)
        self.alu("MUL", operand_a, operand_b)
        return instruction_register + 2

    def invalid(self, instruction_register):
        print("Invalid Function")
        return instruction_register

    def hlt(self, instruction_register):
        self.running = False
        return instruction_register


    def run(self):
        """Run the CPU."""

        instruction_register = self.pc
        instruction_dictionary ={
            0b01000111: self.prn,
            0b10000010: self.ldi,
            0b10100010: self.mul,
            0b00000001: self.hlt
        }

        while self.running:
            instruction = self.ram_read(instruction_register)
            #print(f"Pulled instruction: {instruction}")
            
            function = instruction_dictionary.get(instruction, self.invalid)
            instruction_register = function(instruction_register)
            instruction_register += 1
