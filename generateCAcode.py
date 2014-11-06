#!/usr/bin/env python
#-*-encoding:utf-8-*-

# generateCAcode.py generates one of the 32 GPS satellite C/A codes.
# CAcode = generateCAcode(PRN)

import sys
import pickle


def generateCAcode(PRN):
    """usage:
    inputs: PRN         - PRN number of the sequence.
    outputs: CA/code    - a vector containing the desired C/A code sequence.
    """
# The g2s vector holds the appropriate shift of the g2 code to generate
# the C/A code
    g2s = [5, 6, 7, 8, 17, 18, 139, 140, 141, 251,
            252, 254, 256, 257, 258, 469, 470, 471, 472,
            473, 474, 509, 512, 513, 514, 515, 516, 859,
            860, 861, 862, 145, 175, 52, 21, 237, 235, 886,
            657, 634, 762, 355, 1012, 176, 603, 130, 359, 595,
            68, 386]
    g2shift = g2s[PRN]    # Pick right shift for the given PRN number

# Generate G1 code
    g1 = [0 for i in range(0, 1023)]    # Initialize g1 output to speed up the function
    reg = [-1 for i in range(0, 10)]    # Load shift register
    for i in range(0, 1023):            # Generate all G1 signal chips based on G1 feedback polynominal
        g1[i] = reg[9]
        saveBit = reg[2] * reg[9]
        reg[1:10] = reg[0:9]
        reg[0] = saveBit

# Generate G2 code
    g2 = [0 for i in range(0, 1023)]
    reg = [-1 for i in range(0, 10)]
    for i in range(0, 1023):
        g2[i] = reg[9]
        savebit = reg[1]*reg[2]*reg[5]*reg[7]*reg[8]*reg[9]
        reg[1:10] = reg[0:9]
        reg[0] = savebit

# Shift G2 code
# The idea: g2 = concatenate[ g2_right_part, g2_left_part ]
    temp = g2[(1023-g2shift) : 1023]
    temp2 = g2[0 : (1023 - g2shift)]
    g2 =  temp + temp2
    caCode = [0 for i in range(0, 1023)]


    for i in range(0, 1023):
        caCode[i] = -1*g1[i] * g2[i]
    out = open('cacode.txt', 'w')
    pickle.dump(caCode, out)
    out.close()

generateCAcode(5)
