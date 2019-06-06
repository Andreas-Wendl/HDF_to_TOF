V1.0

Aim of this skript is to convert the formerly used HDF5 format to the new TOF format at RESEDA (https://mlz-garching.de/instrumente-und-labore/spektroskopie/reseda.html).

Requirements:
- python 2.7 or higher
- h5py
- re
- numpy


Usage:
## string with path and name of the input HDF-file.
hdf_name_w_path = '038725'
## Sample detector distance and wavelength of the experiment
L_SD = 2.25
wavelength = 5.918
## new .tof files are written in the same folder as the HDF-file.
write_tof(hdf_name_w_path,8, L_SD, wavelength)

Andreas Wendl, MSc.
Technische Universität München
Lehrstuhl E51
James-Franck-Str. 1, 85748 Garching
Room Nr: 2341a - https://goo.gl/maps/zo7ZSKoCQeF2
Tel.: +49?89?289 12342
E-mail: andreas.wendl@frm2.tum.de