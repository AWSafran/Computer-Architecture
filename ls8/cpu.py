"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [None] * 256
        self.register = [None] * 8
        self.pc = 0

    def ram_read(self, mem_address_register):
        mem_data_register = self.ram[mem_address_register]
        return mem_data_register

    def ram_write(self, mem_address_register, mem_data_register):
        self.ram[mem_address_register] = mem_data_register

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # Register 0
            0b00001000, # numeric value 8
            0b01000111, # PRN R0
            0b00000000, # register 0
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        instruction_register = self.pc

        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010

        running = True

        print("Running")

        while running:

            instruction = self.ram_read(instruction_register)

            if instruction == HLT:
                running = False
            elif instruction == PRN:
                operand_a = self.ram_read(instruction_register + 1)
                print(self.register[operand_a])
                instruction_register += 1
            elif instruction == LDI:
                operand_a = self.ram_read(instruction_register + 1)
                operand_b = self.ram_read(instruction_register + 2)
                self.register[operand_a] = operand_b
                instruction_register += 2
            
            instruction_register += 1
