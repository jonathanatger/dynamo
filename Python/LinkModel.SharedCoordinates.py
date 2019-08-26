
# part of the code originally created by Nicklas Østertgaard  nvo@bimshark.com / nvo@shl.fk  and/or Augusto Goncalves (AEC Devblog)
# Workset management, loop, pin and site location settings by Jonathan ATGER (jonathan.atger@yahoo.fr)

import clr

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import System

doc = DocumentManager.Instance.CurrentDBDocument

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

if isinstance(IN[0], list) : in_links = IN[0] 
else : in_links = [IN[0]]

if isinstance(IN[1], list) : in_ws = IN[1] 
else : in_ws = [IN[1]]

# number of elements
try : numlinks = len(in_links)
except : OUT = 'append link'
	
try : numworksets = len(in_ws)
except : numworksets = 0

#check list lengths
if numlinks == numworksets : listlength = True
else : listlength = False

def linkmodel (fpath, options, doc, pin) :
	# Create the Revit Link Type
	mp = ModelPathUtils.ConvertUserVisiblePathToModelPath(fpath)
	lnkOp = RevitLinkOptions(options)
	loadedLnkType = RevitLinkType.Create(doc, mp, lnkOp)
	
	# Create the Revit Link Instance 
	lnkInstance = RevitLinkInstance.Create(doc, loadedLnkType.ElementId, ImportPlacement.Shared)
	
	#Pin link
	lnkInstance.Pinned = pin
	return lnkInstance

try:
	# Number of worksets input and filepaths input are different
	if IN[1] and listlength == False :
		OUT = "The number of worksets doesn't match the number of links"
		
		
	# Multiple Worksets input
	elif IN[1] and listlength == True  :
	
		#Get WorksetTable and current workset
		wstable = doc.GetWorksetTable()
		activewsid = wstable.GetActiveWorksetId()
		
		#Create list for output
		links = []
		
		for fpath, ws in zip(in_links, in_ws) :
		
			# Get WorksetId
			wssimpleid = ws.Id
			wsid = WorksetId(wssimpleid)
				
			# Set the workset
			WorksetTable.SetActiveWorksetId(wstable, wsid)
			
			# Create the Revit Link Type and Link Instance
			a = linkmodel(fpath,"", doc, IN[2])
			
			#add created link to output
			links.append(a)
							
		#reset current workset	
		WorksetTable.SetActiveWorksetId(wstable, activewsid)
		
		#output
		OUT = links	

	# No worksets input
	else :
		links = []
		for fpath in in_links :
			a = linkmodel(fpath, "", doc, IN[2])
			links.append(a)
		OUT=links
	
except:
    # if error accurs anywhere in the process catch it
    import traceback
    errorReport = traceback.format_exc()
    OUT = errorReport 

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

