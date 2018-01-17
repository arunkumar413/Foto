import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import pymysql
from sqlalchemy import create_engine

UPLOAD_FOLDER = '/home/Pictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def accept_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['POST'])
def file_upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file in accept_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FDER"], filename))
            filenames.append(filename)
    return render_template('home.html')
    create_df(filenames)


def create_df(fnames):
    file_series = pd.Series(fnames)
    session_df = pd.DataFrame(file_series)
    session_df.columns = ["file_name"]
    session_df['album'] = 'None'
    session_df['rating'] = ''
    write_to_db(session_df)


def write_to_db(session_df):
    eng = create_engine('mysql+pymysql://[user]:[pass]@[host]:[port]/[schema]', echo=False)
    session_df.to_sql(name='pics_db', con=eng, if_exists='append', index=False)
