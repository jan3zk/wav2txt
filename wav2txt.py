print('procesiranje ...')
import os
from glob import glob
import time
import random
#from selenium import webdriver
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.firefox.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
import argparse


def argparser():
  ap = argparse.ArgumentParser()
  ap.add_argument('-w',
    type=str,
    help='Path to WAV file or directory containig WAV files.',
    required=True,
  )
  ap.add_argument('-l',
    type=str,
    default='Slovenian (Slovenia)',
    help='Language selection.'
  )
  ap.add_argument('-p',
    action='store_true',
    help='Punctuation switch.'
  )
  ap.add_argument('-s',
    action='store_true',
    help='Storage switch.'
  )
  return ap.parse_args()

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def wav2txt(wav,br,
            lang='Slovenian (Slovenia)',
            punct=True,
            save=False):
  if os.path.isdir(wav):  
    wav_dir = os.path.abspath(wav)
    wav_files = sorted(glob(os.path.join(wav_dir, "*.wav")))
  elif os.path.isfile(wav):  
    wav_files = [os.path.abspath(wav)]

  for wc, wf in enumerate(wav_files):
    ln = Select(br.find_element('id','langselect'))
    ln.select_by_visible_text(lang)
    pn = br.find_element('id','punctuation')
    if punct != str2bool(pn.get_attribute('checked')):
      pn.click()
    s = br.find_element('xpath', "//input[@type='file']")
    s.send_keys(wf)
    txt = ''
    max_retries = 30
    retries = 0
    while ' ---' not in txt and retries < max_retries: 
      time.sleep(random.uniform(0.5, 1))
      txt = br.find_element('xpath', "//textarea[@id='speechout']").text
      retries += 1
    br.refresh()
    txt = txt.split('\n',2)[-1].split('---',1)[0].rstrip()

    print('%s : %s'%(os.path.basename(wf), txt))
    if save:
      with open(os.path.splitext(wf)[0]+'.txt', 'w') as text_file:
        text_file.write(txt)
    if os.path.isfile(wav):
      return txt


if __name__ == '__main__':
  args = argparser()
  wav2txt(args.w, args.l, args.b, args.p, args.s)
