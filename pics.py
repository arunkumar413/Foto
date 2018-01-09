import os
import pandas as pd
import exifread  # library to read the meta data of jpg pictures
import glob
import numpy as np
from datetime import datetime

path = '/home/arun/Pictures/2017/12/27/'  # Directory where all the pictures are located.
file_name = 'DSC_0436.JPG'  # Sample file to get the metadata
f = open(path + file_name, 'rb')  # read the file
tags = exifread.process_file(f)  # extract the metadata

s = pd.Series(tags)  # convert the metadata into a series object
df = pd.DataFrame(s)  # convert the series into dataframe
df.drop(['JPEGThumbnail'], inplace=True)  # drop the column. Not required
df.reset_index(inplace=True)
df.columns = ['parameter', 'value']  # Rename the columns

# metadata may contain lot of information. Most of the times only exif, image, thumbnail and gps are enough.

exif = df[df['parameter'].str.startswith("EXIF")]
image = df[df['parameter'].str.startswith("Image")]
thumbnail = df[df['parameter'].str.startswith("Thumbnail")]
gps = df[df['parameter'].str.startswith("GPS")]

# NOTE:  These are not the values of the metadata.These are just the metadata keys

exif = exif['parameter'].values
image = image['parameter'].values
thumbnail = thumbnail['parameter'].values
gps = gps['parameter'].values

# metadata keys info as list

exif = list(exif)
image = list(image)
thumbnail = list(thumbnail)
gps = list(gps)
cols = exif + image + thumbnail + gps  # cols will be our dataframe columns

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
    path = '/home/arun/Pictures/2017/12/27/'  # chance this as per your convenience
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
