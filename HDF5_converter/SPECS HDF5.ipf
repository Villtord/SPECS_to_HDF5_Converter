#pragma rtGlobals=3		// Use modern global access method and strict wave access.
#include <all IP procedures>

Menu "Process SPECSLab HDF5 data"
	"-"
	"Load HDF5 file from SPECSLab...", LoadSpecs()
	"-"
end

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////


Function LoadSpecs () 

Variable refNum
Variable fileID
Variable result=0
String filename
String message = "Select one or more files"
String outputPaths
String fileFilters = "HDF5 Files (*.h5,*.hdf5):.h5,.hdf5;"
fileFilters += "All Files:.*;"

Open /D /R /MULT=1 /F=fileFilters /M=message refNum
outputPaths = S_fileName
	
if (strlen(outputPaths) == 0)
	Print "Cancelled"
else
	Variable numFilesSelected = ItemsInList(outputPaths, "\r")
	Variable i
		for(i=0; i<numFilesSelected; i+=1)
			String path = StringFromList(i, outputPaths, "\r")
			Printf "%d: %s\r", i, path	
			
			HDF5OpenFile /R /Z fileID as path 	// Open HDF5 file selected via dialog 
		
			if (strlen(S_fileName)>31)
				filename=S_fileName[0,30]
			else
				filename=S_fileName
			endif

			NewDataFolder /S root:$filename					// create datafolder according to filename
	
			if (V_flag==0) 
				Print "loading data ..."
				HDF5LoadGroup /IGOR=-1 /O /R /TRAN=0 /Z :, fileID, "." // loads 2D/3D matrix of raw data
			if (V_flag != 0)
				HDF5CloseFile fileID // close HDF5 file
				Abort "HDF5LoadData failed"
				result = -1
			endif
				Print "done!"
			else
				Abort "No file selected!"
			endif
	
			HDF5CloseFile fileID // close HDF5 file
		endfor
endif
End


/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////