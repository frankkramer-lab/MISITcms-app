import os, sys, json

confpath = os.path.abspath(os.path.join(os.path.dirname(__file__),"cms.conf"))

with open(confpath,"r",encoding="utf-8") as f:
    conf_data = json.load(f)

if len(sys.argv) == 2:
    print(conf_data[sys.argv[1]])
else:
    # Unknown parameter
    pass
