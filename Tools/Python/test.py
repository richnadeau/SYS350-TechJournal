import json

with open('vm-utils.json') as f:
    distros_dict = json.load(f)

for vcenterhost in distros_dict['vcenter']:
        print(vcenterhost['vcenterhost'])