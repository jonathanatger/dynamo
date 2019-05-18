
path = IN[0]

import sys
sys.path.append(r"C:\Program Files (x86)\IronPython 2.7\Lib")

try:
	import os
	os.startfile(path)
	OUT = "Folder opened"

except:
	OUT = "Link the path of the folder you want to open !"

