# -*- coding: utf-8 -*-
import os
import time
import random
import uuid
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import werkzeug
from flask import Flask
from flask_restful import Resource, Api, reqparse
from selenium.webdriver.firefox.service import Service as FirefoxService
from wav2txt import wav2txt


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

app = Flask(__name__)
api = Api(app)
api.app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}

parser = reqparse.RequestParser()
parser.add_argument(
  'file',
  type=werkzeug.datastructures.FileStorage,
  location='files'
)

class About(Resource):
  def get(self):
    return {'WAV2TXT': 'app'}

class Recognise(Resource):
  def post(self):
    data = parser.parse_args()
    if data['file'] == "":
      return {
            'data':'',
            'message':'No file found',
            'status':'error'
              }
    wavfile = data['file']
    if wavfile:
      tmp_name = str(uuid.uuid4())+'.wav'
      wavfile.save(tmp_name)
      # ~ import ipdb; ipdb.set_trace()
      txt_str = wav2txt(tmp_name)
      os.remove(tmp_name) 
      return {
              'data':txt_str,
              'message':'speech recognised',
              'status':'success'
              }
    return {
            'data':'',
            'message':'Something when wrong',
            'status':'error'
            }

api.add_resource(About, '/')
api.add_resource(Recognise,'/recognise')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
