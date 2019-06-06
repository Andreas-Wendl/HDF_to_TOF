import h5py
import re
import numpy as np


def load_hdf(hdf_file, number_of_foils, lsd, wavelength, exclude = []):
        '''
        Returns:
        5D np.array [#jobs, #foils (8 in this version), 16, 128, 128]), rearranged according to foil_order
        Adapted from F. Haslbecks (TUM) analysis code.
        '''
        hdf = h5py.File(hdf_file,"r")
        exclude = exclude
        foil_order=[7,6,5,0,1,2]
        jobs_sort = sorted([k for k in hdf.keys() if "Echo" in k], key = lambda z: int(re.split('(\d+)',z)[1]))
        jobs = []
        for j in jobs_sort:
            if not j in jobs and not j in exclude:
                jobs.append(j)

        reshaped = []
        monitor = np.zeros(len(jobs))
        freqs = np.zeros((len(jobs), 2))

        for step, job in enumerate(jobs):
            subjobs = [key for key in hdf[hdf.keys()[0]].keys() if 'ew_Counts' in key]
            freqs[int(step)][0] = (hdf[str(job)][str(subjobs[0])].attrs.get('ChangedHF'))[1,2]
            freqs[int(step)][1] = (hdf[str(job)][str(subjobs[0])].attrs.get('ChangedHF'))[1,1]
            monitor[int(step)] = (hdf[str(job)][str(subjobs[0])].attrs.get('ev_Monitor'))
            subjobs = [key for key in hdf[hdf.keys()[0]].keys() if 'ew_MDMiezeCounts' in key]
            for subjob in subjobs:
                reshaped.append(np.reshape(hdf[str(job)][str(subjob)], (number_of_foils,16,128,128)))   
        reshaped = np.asarray(reshaped)
        reshaped = reshaped[:,foil_order,:,:,:]
        
        return (reshaped, hdf_file, lsd, wavelength, monitor, freqs)

def write_tof(hdf_name, number_foils,lsd, wavelength):
    '''
    Writes the data stored in the hdf-file in .tof-files. 
    One .tof file for each Mieze_Echo (frequency) within the HDF-file.
    Output is named NAMEOFHDF_i. The files are not sorted by frequency or so.
    '''
    data = load_hdf(hdf_name, number_foils, lsd, wavelength,exclude=[])
    for i in range(len(data[0])):
        f = open(data[1]+'_'+str(i)+'.tof', 'wb')
        bytes = data[0][i].tobytes()
        f.write(bytes)
        f.write('\n    cbox_0a_fg_freq_value : '+str(data[5][i][0])+' Hz')
        f.write('\n    cbox_0b_fg_freq_value : '+str(data[5][i][1])+' Hz')
        f.write('\n    selector_lambda_value : '+str(data[3])+' A')
        f.write('\n       psd_distance_value : '+str(data[2])+' m')
        f.write('\n           monitor1 : '+str(data[4][i]))
        f.close()

# usage:
## string with path and name of the input HDF-file.
hdf_name_w_path = '038725'
## Sample detector distance and wavelength of the experiment
L_SD = 2.25
wavelength = 5.918
## new .tof files are written in the same folder as the HDF-file.
write_tof(hdf_name_w_path,8, L_SD, wavelength)