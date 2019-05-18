# most of the code originally created by Konrad K Sobon : @arch_laboratory, http://archi-lab.net
# options, loop and formatting added by Jonathan ATGER jonathan.atger@yahoo.fr
# suggestions by Alban de Chasteigner

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

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import System

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# number of elements
if isinstance (IN[0], str) : 
	numlinks = 1
else :
	try : numlinks = len(IN[0])
	except : numlinks = 0

try :
	numviews = len(IN[1])
except :
	if IN[1] : numviews = 1
	else : numviews = 0

#check list lengths
if numlinks != numviews :
	listlength = False
else : 
	listlength = True


def linkdwg (fpath, doc, view) : 
		
	#options of the dwg import
	options = DWGImportOptions()
	options.AutoCorrectAlmostVHLines = True
	if IN[5] == True : options.ColorMode = ImportColorMode.BlackAndWhite 
	else : options.ColorMode = ImportColorMode.Preserved
	options.OrientToView = True
	if IN[4] == True : options.ThisViewOnly = False
	else : options.ThisViewOnly = True
	options.VisibleLayersOnly = True
	if IN[6] == "foot" or IN[6] == "Foot": options.Unit = ImportUnit.Foot
	elif IN[6] == "inch" or IN[6] == "Inch": options.Unit = ImportUnit.Inch
	elif IN[6] == "meter" or IN[6] == "Meter": options.Unit = ImportUnit.Meter
	elif IN[6] == "centimeter" or IN[6] == "Centimeter": options.Unit = ImportUnit.Centimeter
	elif IN[6] == "millimeter" or IN[6] == "Millimeter": options.Unit = ImportUnit.Millimeter
	else : options.Unit = ImportUnit.Default 
	options.Placement= ImportPlacement.Shared
	
	
	# Create ElementId / .NET object
	linkedElem = clr.Reference[ElementId]()
	
	#Create the link and the importinstance / Value is .NET
	doc.Link(fpath, options, view, linkedElem)	
	global linkinstance
	linkinstance = doc.GetElement(linkedElem.Value)
	
	#Pin Link
	linkinstance.Pinned = IN[2]

try:
	# Number of worksets input and filepaths input are different
	if IN[1] and listlength == False :
		OUT = "The number of views doesn't match the number of links"
	
	# Multiple Worksets input
	elif IN[3] and listlength == True and numlinks !=1 :
	
		#Get WorksetTable and current workset
		wstable = doc.GetWorksetTable()
		activewsid = wstable.GetActiveWorksetId()
		
		# Get WorksetId
		wssimpleid = IN[3].Id
		wsid = WorksetId(wssimpleid)
				
		# Set the workset
		WorksetTable.SetActiveWorksetId(wstable, wsid)
		
		#loop		
		for fpath, view in zip(IN[0], UnwrapElement(IN[1])) :
			# Create the link and link instance 
			linkdwg(fpath, doc, view)
			links.append(linkinstance)
					
		#reset current workset	
		WorksetTable.SetActiveWorksetId(wstable, activewsid)
	
		#output
		OUT = links	
	
	# Single workset input
	elif IN[3] and listlength == True and numlinks == 1 :
		wstable = doc.GetWorksetTable()
		activewsid = wstable.GetActiveWorksetId()
		links = []
		wssimpleid = IN[3].Id
		wsid = WorksetId(wssimpleid)
		WorksetTable.SetActiveWorksetId(wstable, wsid)
		linkdwg(IN[0], doc, UnwrapElement(IN[1]))
		links.append(linkinstance)
		WorksetTable.SetActiveWorksetId(wstable, activewsid)
		OUT = links	
		
	# No worksets input
	elif numlinks != 1 :
		links = []
		for fpath, view in zip(IN[0], UnwrapElement(IN[1])) :
			linkdwg(fpath, doc, view)
			links.append(linkinstance)
		OUT=links
		
	else :
		links = []
		linkdwg(IN[0], doc, UnwrapElement(IN[1]))
		links.append(linkinstance)
		OUT=links

#Report errors
except:
    # if error accurs anywhere in the process catch it
    import traceback
    errorReport = traceback.format_exc()
    OUT = errorReport 

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

