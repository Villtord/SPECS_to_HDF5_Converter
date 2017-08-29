"""
Created on Fri Jul 21 14:24:17 2017

@author: Victor Rogalev

This script is intended to transform XML data from SPECSLAb files regarding analyser part

"""
def converter_function(filename):
    
    from bs4 import BeautifulSoup
    import numpy as np
    import math
    from scipy.interpolate import InterpolatedUnivariateSpline
    import h5py
    
    
#    def drange(x, y, jump):
#      while x < y:
#        yield float(x)
#        x += jump
    
    
    def unique_names(list_of_names):

        seen=set()
        i=0
        j=1 
        for x in list_of_names:
            if x not in seen:
                seen.add(x)
            else:
                list_of_names[i]=list_of_names[i]+'_'+str(j)
                seen.add(list_of_names[i])
                j+=1
            
            i+=1
        return list_of_names
   
    
    
    def parse_attribute(string, attributes):
        result=[]
        scan_mode = soup.find_all(string, attrs=attributes)
        for scan in scan_mode:
            try:
                result.append(scan.string)
            except:
                print('shit happens')
        return result
    
    """ Open the file and load it to python """
     
    with open(filename) as fd:
        soup = BeautifulSoup(fd.read(),"xml")
        fd.close
        
    """ Some constants for the analyser """
    
    wide_angle=29.296875
    low_angle=15
    
    """ Find all tags that have certain attribute that has an attribute type_name="RegionGroup" and show the type_id attribute""" 
    
    list_of_lens_modes  =   parse_attribute('string',{'name':'analyzer_lens'})
    list_of_slits       =   parse_attribute('string',{'name':'analyzer_slit'})
    list_of_dE          =   parse_attribute('double',{'name':'scan_delta'})
    list_of_XPS         =   parse_attribute('double',{'name':'excitation_energy'})
    list_of_KE          =   parse_attribute('double',{'name':'kinetic_energy'})
    list_of_PassE       =   parse_attribute('double',{'name':'pass_energy'})
    list_of_shift       =   parse_attribute('double',{'name':'position'})
    list_of_shift       =   np.array(list(map(float, list_of_shift)))
    angular_channels    =   parse_attribute('ulong',{'name':'curves_per_scan'})
    list_of_mcd_head    =   parse_attribute('ulong',{'name':'mcd_head'})
    list_of_mcd_head    =   np.array(list(map(int, list_of_mcd_head)))
    list_of_mcd_tail    =   parse_attribute('ulong',{'name':'mcd_tail'})
    list_of_mcd_tail    =   np.array(list(map(int, list_of_mcd_tail)))
    ####################################################################
    ####################### Find all detectors  ########################
    ####################################################################
    list_of_Detectors   =   []
    for i in soup.find_all('sequence',{'name':'detectors'}):
        list_of_Detectors.append(int(i.attrs['length']))
    
    ####################################################################
    ####################### Find all scan_modes ########################
    ####################################################################
    
    list_of_scanmodes   =   []
    scan_mode=soup.find_all(type_name="ScanMode", recursive=True)
    for scan in scan_mode:
        scan_parameters=scan.contents
        list_of_scanmodes.append(scan_parameters[1].string)
            
    ####################################################################
    ####################### Find all Region_names     ##################
    ####################################################################
    
    #type_name="RegionData">
    
    list_of_Region_Names    =   []
    scan_mode = soup.find_all('struct', attrs={'type_name':'RegionData'})
    for var_scan in scan_mode:
        scan=var_scan.contents[1]
        list_of_Region_Names.append(scan.string)
    
    #####################################################################
    ####################### Find all Region_Group_names #################
    ################ and number of regions in each group ################
    #####################################################################
    
    #type_name="RegionGroup"
    
    list_of_Group_Names=[]
    regions_per_group=[]
    scan_mode = soup.find_all('struct', attrs={'type_name':'RegionGroup'})
    for var_scan in scan_mode:
        scan=var_scan.contents[1]
        regions=var_scan.contents[3]
        regions_per_group.append(int(regions.attrs['length']))
        list_of_Group_Names.append(scan.string)
    
    ####################################################################
    ####################### Find all regions with data #################
    ####################### In Each group - each region #################
    ####################### Summ up all cycles if any #################
    ####################################################################
    
    list_data=[]
    list_of_cycles=[]
    
    """ Check for type_name="CompactCycleSeq" --- if the data are compacted """
    
    scan_mode=soup.find_all(type_name="CycleSeq", recursive=True)
    compact_scan_mode=soup.find_all(type_name="CompactCycleSeq", recursive=True)
    j=0
    compact_mode_list=[]
    
    for i in range(len(compact_scan_mode)):
    
        if int(compact_scan_mode[i].attrs['length'])==1:    #this is if the data are compact
            compact_mode_list.append(1)
            level_down=compact_scan_mode[i].contents
            level_down_down=level_down[1].contents
            scan=level_down_down[5]
            data=scan.contents
            data=data[1]
            data_array=np.fromstring(data.string, dtype=float, sep=' ')
            if int(angular_channels[i])!=1:
                data_array.shape = (int(angular_channels[i]), int(data_array.size/int(angular_channels[i])))
            list_data.append(data_array)
            list_of_cycles.append(1)
            j+=list_of_Detectors[i]
            
        elif int(scan_mode[i].attrs['length'])==1:   # This is relevant if data are saved in a non-compact mode (a pain)"""
            
            compact_mode_list.append(0)
            level_down=scan_mode[i].contents
            level_down_down=level_down[1].contents
            scan=level_down_down[3]
    
            number_of_cycles=int(scan.attrs['length'])
            list_of_cycles.append(number_of_cycles)
            level_one        =  scan.contents
            Flag=0
            data_array_detectors=[]
            
            if (list_of_mcd_head[i]!=0) and (list_of_mcd_tail[i]!=0):
                
                factor1=list_of_mcd_head[i]/abs(max(list_of_shift[j:(j+list_of_Detectors[i])]))
                factor2=list_of_mcd_tail[i]/abs(min(list_of_shift[j:(j+list_of_Detectors[i])]))
                
                for k in range(list_of_Detectors[i]):
                    if (list_of_shift[j+k]<=0):
                        list_of_shift[j+k]=list_of_shift[j+k]*factor1
                    else:
                        list_of_shift[j+k]=list_of_shift[j+k]*factor2
        
            for counter in range(1,number_of_cycles*2,2):                         # summ up all cycles of one region
                level_two       =   level_one[counter].contents
                level_three     =   level_two[1].contents
                data=level_three[1]
                data_array_nc=np.fromstring(data.string, dtype=float, sep=' ')         # here is the whole data array from all detectors as is
                
                """ here interpolate over detectors including shift of each detector """
                
                for k in range(list_of_Detectors[i]):
                    
                    if Flag!=0:
                        
                        one_detector            =   np.array(data_array_nc[k::list_of_Detectors[i]])
                        delta                   =   math.floor(list_of_shift[j+k])-list_of_shift[j+k]                 # shift in (-1:0) interval
                        x_shift                 =   np.linspace(delta,len(one_detector)-1+delta,len(one_detector), endpoint=True)    # shifted axis of channel
                        x_axis                  =   np.linspace(0,len(one_detector)-2,len(one_detector)-1, endpoint=True)                # non-shifted axis
                        function_interpol       =   InterpolatedUnivariateSpline(x_shift, one_detector)                 # interpolation function
                       
                        y_interpol              =   function_interpol(x_axis)
                        
                        
                        data_array_detectors    +=  np.roll(y_interpol,math.floor(list_of_shift[j+k]))
                    
                    else:
                        
                        one_detector            =   np.array(data_array_nc[k::list_of_Detectors[i]])
                        delta                   =   math.floor(list_of_shift[j+k])-list_of_shift[j+k]                 # shift in (-1:0) interval
                        x_shift                 =   np.linspace(delta,len(one_detector)-1+delta,len(one_detector), endpoint=True)    # shifted axis of channel
                        x_axis                  =   np.linspace(0,len(one_detector)-2,len(one_detector)-1, endpoint=True)                # non-shifted axis
                        function_interpol       =   InterpolatedUnivariateSpline(x_shift, one_detector)                 # interpolation function
                        
                        y_interpol              =   function_interpol(x_axis)
                         
                        data_array_detectors    =  np.roll(y_interpol,math.floor(list_of_shift[j+k]))
                        
                        Flag                    +=  1
                
            cut_ends=[math.floor(l) for l in list_of_shift[j:(j+k+1)]]
            
            cut_value1  = (abs(max(cut_ends)))
            cut_value2  = (abs(min(cut_ends)))
            
            """ Let's cut out max(list_of_shift[range(list_of_Detectors[])]) first and last elements in the data array """
            
            length=len(data_array_detectors)
            if (min(cut_ends)<=0):
                data_array_detectors=np.delete(data_array_detectors,[l for l in range(length-cut_value2,length)])
            if (max(cut_ends)>=0):
                data_array_detectors=np.delete(data_array_detectors,[l for l in range(cut_value1)])
            
            list_data.append(data_array_detectors)
            j+=list_of_Detectors[i]
        
        else:
        
            compact_mode_list.append(2)             # This is empty region
            list_of_cycles.append(1)
            list_data.append([])
            # This is the case when nothing is written in file """
        
    ####################################################################
    ####################### Create HDF5 file NEXUS #################
    ####################################################################
    from time import gmtime, strftime
    
    #print ("Write HDF5 file")
    fileNameHDF5 = filename.replace(".xml",".hdf5")
    #    fileNameHDF5 = filename.split('/')[-1].replace(".xml",".hdf5")
    
    # create the HDF5 NeXus file
    f = h5py.File(fileNameHDF5, "w")
    
    timestamp=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    f.attrs['default']          = 'entry'
    f.attrs['file_name']        = fileNameHDF5
    f.attrs['file_time']        = timestamp
    f.attrs['instrument']       = 'SPECS'
    f.attrs['HDF5_Version']     = h5py.version.hdf5_version
    f.attrs['h5py_version']     = h5py.version.version
    
    counter=0
    
    #   check for similar names in Group_names and Region Names
    
    list_of_Group_Names     =   unique_names(list_of_Group_Names)
    list_of_Region_Names    =   unique_names(list_of_Region_Names)
    
    #   create the NXentry group
    for i in range (len(list_of_Group_Names)):
        nxgroup = f.create_group(str(list_of_Group_Names[i]))
        nxgroup.attrs['NX_class']       = 'NXdata'
        nxgroup.attrs['Regions_number'] = float(regions_per_group[i])
            
    #        write Data
        for j in range (counter,counter+int(regions_per_group[i]),1):
            
            if compact_mode_list[j]!=2:
           
                ds = nxgroup.create_dataset(str(list_of_Region_Names[j]), data=list_data[j])
                
                ds.attrs['Scan_Mode']         = str(list_of_scanmodes[j])
                ds.attrs['Lens_Mode']         = str(list_of_lens_modes[j])
                ds.attrs['Slit']              = str(list_of_slits[j])
                ds.attrs['Pass_energy']       = float(list_of_PassE[j])
                ds.attrs['Start_energy']      = float(list_of_KE[j])
                ds.attrs['Delta_energy']      = float(list_of_dE[j])
                ds.attrs['Excitation_energy'] = float(list_of_XPS[j])
                ds.attrs['Number of cycles']  = float(list_of_cycles[j])
                
        #            Set up IGOR attributes 
                
                if int(angular_channels[j])==1:
                    

                    ds.attrs['IGORWaveScaling'] = [[0,0],[float(list_of_dE[j]),float(list_of_KE[j])]]   
                    
                    Wave_Note=['Scan_Mode = '+str(list_of_scanmodes[j])+', Lens_Mode = '+str(list_of_lens_modes[j])+', Pass_energy = '+str(list_of_PassE[j])+' eV']
                    Wave_Note_ascii = [n.encode("ascii", "ignore") for n in Wave_Note]
                    ds.attrs['IGORWaveNote'] = Wave_Note_ascii
                
                else:    
        
                    if compact_mode_list[j]==1:
                        if list_of_lens_modes[j]=='WideAngleMode:3.5kV':
                            ds.attrs['IGORWaveScaling'] = [[0,0],[float(wide_angle/int(angular_channels[j])),-wide_angle/2],[float(list_of_dE[j]),float(list_of_KE[j])]]
                        if list_of_lens_modes[j]=='LowAngleMode:3.5kV':
                            ds.attrs['IGORWaveScaling'] = [[0,0],[float(low_angle/int(angular_channels[j])),-low_angle/2],[float(list_of_dE[j]),float(list_of_KE[j])]]
                    
                    
                    #Wave_Units=[""+"\0","degree"+"\0","eV"+"\0"]
                    #Wave_Units_ascii = [[n.encode("ascii", "ignore") for n in Wave_Units]]
                    #ds.attrs['IGORWaveUnits'] = Wave_Units_ascii
        
                    Wave_Note=['Scan_Mode = '+str(list_of_scanmodes[j])+', Lens_Mode = '+str(list_of_lens_modes[j])+', Pass_energy = '+str(list_of_PassE[j])+' eV']
                    Wave_Note_ascii = [n.encode("ascii", "ignore") for n in Wave_Note]
                    ds.attrs['IGORWaveNote'] = Wave_Note_ascii
    
        counter=counter+int(regions_per_group[i])
    
    f.close()













































