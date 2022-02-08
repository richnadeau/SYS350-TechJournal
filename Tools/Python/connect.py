import getpass
import json

with open('vm-utils.json') as f:
    distros_dict = json.load(f)

for vcenterhost in distros_dict['vcenter']:
        vcenterh = vcenterhost['vcenterhost']
        vcentera = vcenterhost['vcenteradmin']

passwd = getpass.getpass()
from pyVim.connect import SmartConnect
import ssl
s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode=ssl.CERT_NONE
si= SmartConnect(host=vcenterh, user=vcentera, pwd=passwd, sslContext=s)
#aboutInfo=si.content.about
#print(aboutInfo)
#print(aboutInfo.fullName)