import os
import pandas as pd
import exifread  # library to read the meta data of jpg pictures
import glob
import numpy as np
from datetime import datetime

exif = pd.read_csv('/home/arun/PycharmProjects/Foto/exif.csv', header=None)
img = pd.read_csv('/home/arun/PycharmProjects/Foto/img.csv', header=None)
maker = pd.read_csv('/home/arun/PycharmProjects/Foto/maker.csv', header=None)
thumbnail = pd.read_csv('/home/arun/PycharmProjects/Foto/thumbnail.csv', header=None)
all_tags = pd.read_csv('/home/arun/PycharmProjects/Foto/all_tags.csv', header=None)

exif = list(exif[0].values)
img = list(img[0].values)
maker = list(maker[0].values)
thumbnail = list(thumbnail[0].values)

cols = exif + img + thumbnail  # cols will be our dataframe columns

# Read the pictures and create a dataframe

files = os.listdir('/home/arun/Pictures/2017/12/27/')
file_name = pd.Series(files)
pics = pd.DataFrame(file_name)
pics.columns = ['file_name']

# create new columns using the cols list
for col in cols:
    pics[col] = 0

## for each picture get the metadata info and append it to the dataframe

def getparams(f):
    path = '/home/arun/Pictures/2017/12/27/'  # change this depending on you environment
    fr = open(path + f, 'rb')  # Read the file
    tags = exifread.process_file(fr)  # extract tags
    for col in cols:
        pics.loc[pics['file_name'] == f, col] = tags[col]  # update the values in the dataframe


pics['file_name'].apply(getparams, f)

# Add new columns
pics['rating'] = 0  # default rating is zero
pics['location'] = ''
pics['tag2'] = ''
pics['tag3'] = ''
pics['album'] = ''

pics['EXIF DateTimeDigitized'] = pd.to_datetime(pics['EXIF DateTimeDigitized'], format='%Y:%m:%d %H:%M:%S')
pics['EXIF DateTimeOriginal'] = pd.to_datetime(pics['EXIF DateTimeOriginal'], format='%Y:%m:%d %H:%M:%S')

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
lastYear = datetime.now().year - 1

if currentMonth == 1:
    lastMonth = 12
else:
    lastMonth = currentMonth - 1


# Connect the frontend click events to the below functions/handlers to filter the pics

def thismonth():
    pics_this_month = pics[pics['EXIF DateTimeOriginal'].dt.month == currentMonth]


def thisyear():
    pics_this_year = pics[pics['EXIF DateTimeOriginal'].dt.year == currentYear]

def today():
    pics_today = pics[pics['EXIF DateTimeOriginal'].dt.date == currentDay]

def lastmonth():
    return pics[pics['EXIF DateTimeOriginal'].dt.month == lastMonth]


def rating(score):
    rated = pics[pics['rating'] == score]
