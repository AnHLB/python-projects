import sys
import re
from io import StringIO
import pandas as pd
import numpy as np
import subprocess
import html


tHeader = "sbd,tên,dd,mm,yyyy,toán,ngữ văn,khxh,khtn,lịch sử,địa lí,gdcd,sinh học,vật lí, hoá học,tiếng anh\n"
subjectsList = ['toán', 'ngữ văn', 'khxh', 'khtn', 'lịch sử',
                'địa lí', 'gdcd', 'sinh học', 'vật lí', 'hóa học', 'tiếng anh']


def writeToCSV(data, writeOptions):
    if writeOptions == "":
        writeOptions = 'w'
    s = StringIO(data)
    with open('fileName.csv', writeOptions, encoding="utf-8") as f:  # 'w' new file, 'a' append more
        for line in s:
            f.write(line)


def readHTMLData(sIndex):
    sbd = sIndex
    cmd = ""
    # while sbd <= endIndex:
    val_sbd = '0' + str(sbd)
    cmd = u'curl -F  "SoBaoDanh="' + val_sbd + ' diemthi.hcm.edu.vn/Home/Show'
    outputData = subprocess.check_output(cmd, shell=True, encoding="UTF-8")
    return outputData


def stripHTML(dataHTML):
    # remove empty lines
    ret = re.sub(r"\s", " ", dataHTML, flags=re.MULTILINE)
    # remove content between <>
    ret = re.sub('<.*?>', ' ', ret, flags=re.DOTALL)
    # remove whitespace more than 1
    ret = re.sub(r"  +", " ", ret)
    # Check student index available or NOT
    check = ret[len(
        u'Sở Giáo dục và Đào tạo TP HCM TRA CỨU ĐIỂM KỲ THI TỐT NGHIỆP TRUNG HỌC PHỔ THÔNG 2020 ') + 8::].strip()
    if check == "Không tìm thấy số báo danh này !":
        ret = ""
    else:
        # remove header
        ret = ret[len(
            u'Sở Giáo dục và Đào tạo TP HCM TRA CỨU ĐIỂM KỲ THI TỐT NGHIỆP TRUNG HỌC PHỔ THÔNG 2020 Họ và Tên Ngày sinh Điểm thi ')+8::].strip()
    return ret


def getDataOfStudentFromHTML(OutputHTMLData):
    # clean HTML data to get raw data remove whitespaces pattern (r'^[\s]*|[\s]$',"",data)
    rawOutputData = stripHTML(OutputHTMLData)
    rawOutputData = "".join(rawOutputData)
    # escape HTML entities to unicode characters
    rawOutputData = html.unescape(rawOutputData)

    if rawOutputData != "":
        # initialise lists
        fullName, dobOfStudent, gradesOfStudent, subjectNames = ([], ) * 4
        # get fullname and remove it from rawOutputData
        fullName = re.findall(r'^[^a-z\/:.]+\s', rawOutputData)
        fullName = "".join(fullName)
        fullName = fullName.strip()
        fullName = fullName.title()

        removeFullName = re.sub(r'^[^a-z\/:.]+\s', "", rawOutputData)

        # get date of birth and remove it from rawOutputData
        dobOfStudent = re.findall(r'\d+[\/|-].*.[\/|-]\d+', removeFullName)
        dobOfStudent = "".join(dobOfStudent)
        dobOfStudent = dobOfStudent.strip()
        dobOfStudent = re.sub(r'\/', ",", dobOfStudent)
        dobOfStudent = "".join(dobOfStudent)

        removeDOB = re.sub(r'\d+[\/|-].*.[\/|-]\d+', "", removeFullName)
        removeDOB = removeDOB.strip()
        # get grades and remove them from rawOutputData
        gradesOfStudent = re.findall(
            r':[^\S\r\n]+(\d+(?:\.\d+)?)', removeDOB)
        removeGradesOfStudent = re.sub(
            r':[^\S\r\n]+(\d+(?:\.\d+)?)', ": ", removeDOB)
        subjectNames = re.split(r':\s+', removeGradesOfStudent)
        subjectNames.pop()
        newListGradesOfStudent = [np.nan, np.nan,
                                  np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        for i in range(0, len(subjectNames)):
            for k in range(0, len(subjectsList)):
                if subjectNames[i].lower() == subjectsList[k]:
                    newListGradesOfStudent[k] = gradesOfStudent[i]

        newListGradesOfStudent1 = [str(int) for int in newListGradesOfStudent]
        newListGradesOfStudent1 = ",".join(newListGradesOfStudent1)
        newListStudent = fullName + "," + dobOfStudent + "," + newListGradesOfStudent1
    else:
        newListStudent = ""
     #   print(newListStudent)
    return newListStudent


# get all data
newListGradesOfStudent = ""
tempListGradesOfStudent = ""
noDataSBD = ""
startSBD = 2000001
endSBD = 2074718  # 2074718
#writeToCSV(tHeader, 'w')
while startSBD <= endSBD:
    OutputHTMLData = readHTMLData(startSBD)
    tempListGradesOfStudent = getDataOfStudentFromHTML(OutputHTMLData)
    if tempListGradesOfStudent != "":
        newListGradesOfStudent = "0" + str(startSBD) + "," + \
            tempListGradesOfStudent + "\n"
        writeToCSV(newListGradesOfStudent, 'a')
    else:
        noDataSBD = noDataSBD + "," + "0" + str(startSBD)

    startSBD = startSBD + 1
writeToCSV(noDataSBD, 'a')
'''
studentsData = {}
df = pd.DataFrame(studentsData)
arraySBD = ['2000149', '2000201']
df['sbd'] = arraySBD
print(df)
'''
