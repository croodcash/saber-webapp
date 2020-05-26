import datetime
import json
import os
import re
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

abs_input_path = "/home/meong/webapp/saber/media/"
abs_model_path = "/home/meong/saber-project/"

input_path = abs_input_path + "input/"
model_path = abs_model_path + "model/"

email_key = "email"
title_key = "title"

gmail_user = 'saber.email.service@gmail.com'
gmail_password = 'superConfidential'


def transcribe(model, title):
    file = input_path + model + title
    print("tarnscribing: " + file)

    type = model.split("_")[0]

    command = 'python /home/meong/saber-project/saber/skripsi/transcribe/' + type + '_transcribe.py --model_dir="' + \
              model_path + model + '"  ' + file
    os.system(command)


def get_song_map(title_without_extension):
    with open("/home/meong/webapp/saber/media/map.json") as json_file:
        return json.load(json_file)[title_without_extension]


def zip_file(model, title):
    os.system("cp " + input_path + model + title + ".midi ./")

    title_without_extension = title[:-5]

    song_map = get_song_map(title_without_extension)

    original_title = re.escape(song_map[title_key])
    original_title = original_title[:-4]

    os.system("mv " + title + ".midi " + original_title + ".midi")
    os.system("zip " + original_title + ".zip " + original_title + ".midi")


def create_email_body(title):
    title_without_extension = title[:-5]
    song_map = get_song_map(title_without_extension)

    msg = MIMEMultipart()
    msg['Subject'] = "Music Transcription is done!"
    msg['From'] = gmail_user
    msg['To'] = song_map[email_key]

    body = "Hey, here is your music transcription! Thank you for using our service!\n\n-- SABER Team"
    msg.attach(MIMEText(body, 'plain'))

    original_title = song_map[title_key]
    original_title = original_title[:-4]

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(original_title + ".zip", "rb").read())
    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="' + original_title + ".zip" + '"')

    msg.attach(part)

    return msg.as_string()


def send_email(title):
    title_without_extension = title[:-5]
    song_map = get_song_map(title_without_extension)

    receiver = song_map[email_key]

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, receiver, create_email_body(title))
    print("SUCCESSFULLY SENDING EMAIL TO: " + receiver)


def cleanup(model, file):
    title_without_extension = file[:-5]
    song_map = get_song_map(title_without_extension)

    original_filename = song_map[title_key][:-4]

    os.system("rm " + input_path + model + file)
    os.system("rm " + input_path + model + file + ".midi")
    os.system("rm " + re.escape(original_filename + ".midi"))
    os.system("rm " + re.escape(original_filename + ".zip"))


def main():
    models = os.listdir(input_path)
    for model in models:
        inputs = os.listdir(input_path + model)
        model = model + "/"
        for file in inputs:
            print(datetime.datetime.utcnow().strftime("%c"))
            print("Start transcribing....")
            print("WE ARE ON DIR: " + model)
            file = re.escape(file)
            transcribe(model, file)
            zip_file(model, file)
            send_email(file)
            cleanup(model, file)
            print("DONE!")


main()
