#!/usr/bin/python3
import os, sys, base64
from datetime import datetime, timedelta, timezone
from pyjsparser import parse

os.chdir(sys.path[0])

with open("./pac.js", "r+") as pac_js:
    pac = parse(pac_js.read())
pac_js.close

for js_var in pac['body']:
    if js_var['type'] == 'VariableDeclaration' and js_var['declarations'][0]['id']['name'] == 'rules':
        gen_list = f"[AutoProxy 0.2.9]\n!build on {datetime.now(timezone(timedelta(hours=8))).strftime('%y%m%d %H:%M:%S %Z')}\n"
        gen_list += "\n\n!------direct rules from gfwList\n\n"
        for rule in js_var['declarations'][0]['init']['elements'][1]['elements'][0]['elements']:
            gen_list += f"@@{rule['value']}\n"
        gen_list += "\n\n!------proxy rules from gfwList\n\n"
        for rule in js_var['declarations'][0]['init']['elements'][1]['elements'][1]['elements']:
            gen_list += f"||{rule['value']}\n"
        gen_list += "\n\n!------direct rules from user list\n\n"
        for rule in js_var['declarations'][0]['init']['elements'][0]['elements'][0]['elements']:
            gen_list += f"@@{rule['value']}\n"
        gen_list += "\n\n!------proxy rules from user list\n\n"
        for rule in js_var['declarations'][0]['init']['elements'][0]['elements'][1]['elements']:
            gen_list += f"||{rule['value']}\n"

with open("./merge.list", "wb+") as merge_list:
    merge_list.write(base64.b64encode(gen_list.encode(encoding="UTF-8")))
merge_list.close

pass