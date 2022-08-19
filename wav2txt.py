import os, sys
from glob import glob
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Iz https://chromedriver.chromium.org/downloads prenesi ustrezen 
# gonilnik in ga razširi v direktorij v katerem se nahaja python.exe.

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
ch = webdriver.Chrome(options=options)
ch.get('https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/#features')
ln = Select(ch.find_element('id','langselect'))

if os.path.isdir(sys.argv[1]):  
  wav_dir = os.path.abspath(sys.argv[1])
  wav_files = sorted(glob(os.path.join(wav_dir, "*.wav")))
elif os.path.isfile(sys.argv[1]):  
  wav_files = [os.path.abspath(sys.argv[1])]

for wc, wf in enumerate(wav_files):
  ln = Select(ch.find_element('id','langselect'))
  ln.select_by_value('sl-SI')
  s = ch.find_element('xpath', "//input[@type='file']")
  s.send_keys(wf)
  txt = ''
  max_retries = 30
  retries = 0
  while ' ---' not in txt and retries < max_retries: 
    time.sleep(random.uniform(0.5, 1))
    txt = ch.find_element('xpath', "//textarea[@id='speechout']").text
    retries += 1
  ch.refresh()
  txt = txt.split('\n',2)[-1].split('---',1)[0].rstrip()
  print('%s (%i/%i):'%(os.path.basename(wf), wc+1, len(wav_files)))
  print(txt)
