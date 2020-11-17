import os
import csv
import pandas as pd
import re
import subprocess


def readHTMLData(sIndex):
    sbd = sIndex
    cmd = ""
    # while sbd <= endIndex:
    val_sbd = '0' + str(sbd)
    cmd = u'curl -F  "SoBaoDanh="' + val_sbd + ' diemthi.hcm.edu.vn/Home/Show'
    outputData = subprocess.check_output(cmd, shell=True, encoding="UTF-8")
    return outputData


startSBD = 2034898
OutputHTMLData = readHTMLData(startSBD)

# 1: Using read_csv() method: read_csv() is an important pandas function to read csv files and do operations on it.
# creating a data frame
df = pd.read_csv("fileName.csv")
print(df.head())

# 2: Using read_table() method: read_table() is another important pandas function to read csv files and create data frame from it.
# creating a data frame
df = pd.read_table("fileName.csv", delimiter=",")
print(df.head(10))

# 3: Using csv module: One can directly import the csv files using csv module and then create a data frame using that csv file.

with open("fileName.csv") as csv_file:
    # read the csv file
    csv_reader = csv.reader(csv_file)

    # now we can use this csv files into the pandas
    df = pd.DataFrame([csv_reader], index=None)

# iterating values of first column
for val in list(df[1]):
    print(val)

 # Find out your current working directory
print(os.getcwd())
# Out: /Users/shane/Documents/blog
# Display all of the files found in your current working directory
print(os.listdir(os.getcwd()))
