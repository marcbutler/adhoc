#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from sys import argv

content = bytearray(open(argv[1], 'rb').read())

freq, bins, patches = plt.hist(content, 256)
plt.xlabel("Byte Value"); plt.ylabel("Frequency"); plt.title(argv[1])
plt.grid(True)
plt.show()

