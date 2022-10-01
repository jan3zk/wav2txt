import os, sys
import time
import random
import uuid
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from flask import Flask, request
from werkzeug.utils import secure_filename

# Iz https://github.com/mozilla/geckodriver/releases/ prenesi ustrezen 
# gonilnik in ga razširi v direktorij v katerem se nahaja python.exe.

def wav2txt(wav, lang='Slovenian (Slovenia)'):
  options = Options()
  options.headless = True
  ff = webdriver.Firefox(options=options)
  ff.get('https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/#features')
  ln = Select(ff.find_element('id','langselect'))
  ln = Select(ff.find_element('id','langselect'))
  ln.select_by_visible_text(lang)
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
  return txt.split('\n',2)[-1].split('---',1)[0].rstrip()+'\n'


app = Flask(__name__)

@app.route("/")
def about():
  return "WAV2TXT app."

@app.route('/recognise', methods=['POST','PUT'])
def recognise():
  f = request.files['file']
  if f.filename != '':
    tmp_file = str(uuid.uuid4())+'.wav'
    f.save(tmp_file)
    #filename = secure_filename(f.filename)
    #import ipdb; ipdb.set_trace()
    txt_str = wav2txt(tmp_file)
    os.remove(tmp_file) 
    return txt_str
    


if __name__ == '__main__':
  app.run(port=5000,debug=True)
