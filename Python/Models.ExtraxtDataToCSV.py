#Made by Jonathan ATGER, 2019


import clr
#clr.AddReference('ProtoGeometry')
#from Autodesk.DesignScript.Geometry import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import System

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
#from RevitServices.Transactions import TransactionManager

#doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

import csv
import time

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *



#inputs
if isinstance(IN[0], list) : filepaths = IN[0]
else : filepaths = [IN[0]]

directorypath = IN[1] 

if isinstance(IN[2], list) : categories = IN[2]
else : categories = [IN[2]]

if isinstance(IN[3], list) :params = IN[3]
else : params = [IN[3]]

modelname = IN[4]
getid = IN[5]


paths = []
for p in filepaths :
	modelpath = ModelPathUtils.ConvertUserVisiblePathToModelPath(p)
	paths.append(modelpath)
	
#Setup list for the output of the node
out = []
headers = []


#create headers for csv file
if modelname == True :
	headers.append("File Name")
if getid == True :
	headers.append("Id")	
for c in params :
	headers.append(c)
	
out.append(headers)

# det document opening option 
options = OpenOptions()
options.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
	

	
try :
	for i in paths :
		#open revit document
		opendoc = app.OpenDocumentFile(i, options)
		
		if IN[4] == True :
			#add document name
			pathname = opendoc.PathName
			name = pathname.split("\\")[-1]
		
		for c in categories :
			
			#filter
			filter = ElementCategoryFilter(System.Enum.ToObject(BuiltInCategory, c.Id))
				
			#Collector filtering out types
			col = FilteredElementCollector(opendoc).WherePasses(filter).WhereElementIsNotElementType().ToElements()
			
			for e in col :
				elementdata = []
				
				if modelname == True :
					elementdata.append(name)
				
				if getid == True :
					elementdata.append(e.Id)
				
				for p in params :
					try :
						#append properties
						param = e.LookupParameter(p).AsValueString()
						if param == None :
							param2 = e.LookupParameter(p).AsString()
							elementdata.append(param2)
						else :
							elementdata.append(param)
					
					
					except :
						elementdata.append("No parameter with the given name")
						
				#append the elementdata to the right category		
				out.append(elementdata)
			
			
		#Close document
		opendoc.Close(False)
	
	filename = directorypath + '\\modeldata_' + time.strftime("%Y%m%d_%H%M%S") + '.csv'
	
	OUT = out[1:], filename
	
	#get the directory for extraction
	#os.chdir(IN[5])
	
	with open(filename, mode='wb') as csv_file :
		csv_filewriter = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for line in out :
			csv_filewriter.writerow(line)

	
except:
    # if error accurs anywhere in the process catch it
    import traceback
    errorReport = traceback.format_exc()
    OUT = errorReport 

