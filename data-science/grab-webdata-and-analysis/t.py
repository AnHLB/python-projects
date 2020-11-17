import os
import subprocess


def readHTMLData(sIndex):
    sbd = sIndex
    cmd = ""
    # while sbd <= endIndex:
    val_sbd = '0' + str(sbd)
    cmd = 'curl https://freecoursesite.us'
    outputData = subprocess.check_output(cmd, shell=True)
    return outputData


startSBD = 2034898
OutputHTMLData = readHTMLData(startSBD)
print(OutputHTMLData)
