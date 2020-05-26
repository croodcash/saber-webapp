import datetime
import hashlib
import json
import os

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

from .models import UploadFileForm

EMAIL_KEY = "email"
TITLE_KEY = "title"


def get_map_data():
    pwd = os.path.dirname(__file__)
    path_to_map_file = os.path.join(pwd, "../media/map.json")

    with open(path_to_map_file, "r") as json_file:
        data = json.load(json_file)
        return data


def write_map_data(data):
    pwd = os.path.dirname(__file__)
    path_to_map_file = os.path.join(pwd, "../media/map.json")

    with open(path_to_map_file, "w") as json_file:
        json.dump(data, json_file)


def get_hashed_filename(form):
    salted_filename = form["email"] + "#" + form["file"].name + "#" + str(datetime.datetime.now().timestamp())
    return hashlib.md5(salted_filename.encode('utf-8')).hexdigest()


def update_map_data(form, hashed_filename):
    pwd = os.path.dirname(__file__)
    path_to_map_file = os.path.join(pwd, "../media/map.json")
    print(path_to_map_file)

    json_payload = {EMAIL_KEY: form["email"], TITLE_KEY: form["file"].name}

    data = get_map_data()
    data[hashed_filename] = json_payload

    write_map_data(data)


def save_uploaded_file(form):
    print("Going to save form file")
    fs = FileSystemStorage()
    file = form["file"]

    hashed_filename = get_hashed_filename(form)
    fs.save("./input/" + form["model"] + "/" + hashed_filename + ".wav", file)

    update_map_data(form, hashed_filename)


def index(request):
    print("accepted")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("cleaned data!")
            save_uploaded_file(form.cleaned_data)
            return render(request, 'transcribe/index.html', {'file_url': "filename"})
        else:
            print("error data")
            print(form.errors)
    else:
        form = UploadFileForm()

    return HttpResponse(render(request, 'transcribe/index.html', {'form': form}))
