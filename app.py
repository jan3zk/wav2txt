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

# Iz https://github.com/mozilla/geckodriver/releases/ prenesi ustrezen 
# gonilnik in ga razširi v direktorij v katerem se nahaja python.exe.

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def wav2txt(wav, lang='Slovenian (Slovenia)', punct=False):
  options = Options()
  options.headless = True
  ff = webdriver.Firefox(options=options)
  ff.get('https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/#features')
  ln = Select(ff.find_element('id','langselect'))
  ln.select_by_visible_text(lang)
  pn = ff.find_element('id','punctuation')
  if punct != str2bool(pn.get_attribute('checked')):
    pn.click()
  s = ff.find_element('xpath', "//input[@type='file']")
  s.send_keys(os.path.abspath(wav))
  txt = ''
  max_retries = 15
  retries = 0
  while ' ---' not in txt and retries < max_retries: 
    time.sleep(random.uniform(0.5, 1))
    txt = ff.find_element('xpath', "//textarea[@id='speechout']").text
    retries += 1
  ff.refresh()
  return txt.split('\n',2)[-1].split('---',1)[0].rstrip()


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
  decorators=[]
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
