#pragma rtGlobals=3		// Use modern global access method and strict wave access.
#include <all IP procedures>

Menu "Process SPECSLab HDF5 data"
	"-"
	"Load HDF5 file from SPECSLab...", LoadSpecs()
	"-"
end

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////


Function LoadSpecs ([pathName]) 
	String pathName
	String filename
	
	if (ParamIsDefault(pathName))
		pathName=""
		Prompt pathName, "Enter name of symbolic path if set or leave empty"
		DoPrompt "Path to data", pathName
		if(V_Flag)
			return -1
		endif
	endif
	
	Variable fileID
	Variable result=0
	
HDF5OpenFile /P=$pathName /R /Z fileID as "" 	// Open HDF5 file selected via dialog 

if (strlen(S_fileName)>31)
	filename=S_fileName[0,30]
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

end


/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////