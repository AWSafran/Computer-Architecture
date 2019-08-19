#!/usr/bin/env python3

"""Main."""

import sys
import os
from cpu import *


if __name__ == "__main__":
    cpu = CPU()

    if len(sys.argv) != 2 or not os.path.exists(f"examples/{sys.argv[1]}"):
        print("Please try again with a valid command argument")
    else:
        cpu.load(sys.argv[1])
        cpu.run()