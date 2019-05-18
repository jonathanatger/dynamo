import clr

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

#math module
import math

#import system
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import System

#instance or list
if isinstance(IN[0],list):
	views = UnwrapElement(IN[0])
	horAngles = IN[1]
	vertAngles = IN[2]
else : 
	views = [UnwrapElement(IN[0])]
	horAngles = [IN[1]]
	vertAngles = [IN[2]]

#out
out = []

try : 
	for view, horAngle, vertAngle in zip(views, horAngles, vertAngles) :
		# is perspective check
		try : Pers = view.IsPerspective
		except : out.append("View is not a perspective view"); Pers = False
		
		#Launch 
		if Pers == True : 
			
			Zmax = -0.1
				
			#max point coordinates : closest to viewer
			Xmax = -Zmax*math.tan(math.radians(horAngle/2))
			Ymax = -Zmax*math.tan(math.radians(vertAngle/2))
			CalcPointMax = XYZ(Xmax, Ymax, Zmax)
			
			
			#min point coordinates
			Xmin = -Xmax
			Ymin = -Ymax
			Zmin = Zmax*1000
			CalcPointMin = XYZ(Xmin, Ymin, Zmin)
			
			#Create Bounding Box to apply to view
			NewCrop = BoundingBoxXYZ()
			NewCrop.Min = CalcPointMin
			NewCrop.Max = CalcPointMax
			
			#Start transaction
			TransactionManager.Instance.EnsureInTransaction(doc)
			
			# Set Cropbox active
			if view.CropBoxActive == False :
				view.CropBoxActive = True
			
			#Apply Cropbox settings to put
			view.CropBox = NewCrop
			
			#Transaction end
			TransactionManager.Instance.ForceCloseTransaction()
			
			out.append("Success")
	OUT = out
	
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()
	OUT = errorReport





