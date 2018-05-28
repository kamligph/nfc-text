import sys
import unicodedata2
import subprocess
import threading, webbrowser
import diff_match_patch as dmp_module
from bs4 import BeautifulSoup

def main():

  try:
    malformed_string = sys.argv[1]
  except IndexError:
    malformed_string = 'Please put something...'

  try:
    form = sys.argv[2]
  except IndexError:
    form = 'NFC'

  formed_string = unicodedata2.normalize(form, malformed_string)
  dmp = dmp_module.diff_match_patch()
  diffs = dmp.diff_main(malformed_string, formed_string)

  with open('templates/index.html') as inf:
    html = inf.read()
    soup = BeautifulSoup(html, 'html.parser')

  div_output = soup.find('div', {'id': 'output'})
  div_output.clear()
  new_pre = "<pre class='diff_data'>\n----------------------------------------\nForm: " + form + \
    "\nMalformed string: " + malformed_string + \
    "\n========================================\n " + form + \
    " string: " + formed_string + "\n========================================\n" + \
    "\nDiff: " + ''.join(map(str, diffs)) + "</pre>"
  extra_soup = BeautifulSoup(new_pre, 'html.parser')
  div_output.append(extra_soup)

  pretty_diff = dmp.diff_prettyHtml(diffs)
  extra_soup = BeautifulSoup(("<div class='diff_wrapper'>" + pretty_diff + "</div>"), 'html.parser')
  
  div_output.append(extra_soup)

  with open('templates/index.html', 'w') as outf:
    outf.write(str(soup))

  threading.Timer(1.25, lambda: webbrowser.open("http://127.0.0.1:5000/") ).start()
  subprocess.call("FLASK_APP=routes.py flask run", shell=True)
  
if __name__ == '__main__':
  main()