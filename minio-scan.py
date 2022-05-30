from flask import request
from flask import current_app
from minio import Minio
from flask import jsonify
import os.path
import os
import json
import urllib.parse

def main():
    #READ-WHAT-WAS-RECEIVED
    current_app.logger.info("Received request")
    msg = "---HEADERS---\n%s\n--BODY--\n%s\n-----\n" % (request.headers, request.get_data())
    y = json.loads(request.get_data())

    #CONNECT-TO-MINIO
    client = Minio(
    "MINIO_IP:MINIO_PORT",
    access_key="ACCESS_KEY",
    secret_key="SECRET_KEY",
    secure=False
    ) 

    #EXTRACT INFO FROM MINIO
    bucket = y['Records'][0]['s3']['bucket']['name']
    key = y['Key']
    object_key = y['Records'][0]['s3']['object']['key']
    file_name = key.split("/")
    file_name = file_name[-1]
    full_file_name = urllib.parse.unquote_plus(object_key)

    #COPY OBJECT
    client.fget_object(bucket, full_file_name, file_name)
    os.system("mkdir -p /tmp/infected-files/")

    #SCAN OBJECT
    cmd="clamdscan " +file_name+ " --move /tmp/infected-files/" 
    os.system(cmd)
    file_path = "/tmp/infected-files/" +file_name

    #CHECK IF INFECTED
    msg = os.path.exists(file_path)
    
    if msg:    
      client.fput_object("infected-objects", file_name, file_path) 
      return jsonify("File scannedd: " +key+ '/' +file_name+ ".This file is infected")
    else:
      return jsonify("File scannedd: " +key+ ". This file is OK.") 

