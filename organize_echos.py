import os
import numpy as np
import pydicom as dcm
from pydicom.encaps import encapsulate

def safe_makedir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def count_dicoms(direc):
	counter = 0
	filenames = os.listdir(direc)
	for filename in filenames:
		if filename[-3:] == 'dcm':
			counter += 1
	return counter

def parse_name(old_name):
	cage_number = old_name[20:28]
	cage_number = int(cage_number.replace(' ', ''))
	mouse_number = old_name[29:31]
	return [cage_number, mouse_number]

def change_name(ds, save_direc, cage_number, mouse_number, dicom_count):
	ds.PatientName = mouse_number + '_' + str(cage_number)
	new_name =  mouse_number + '_' + str(cage_number) + '_' + str(dicom_count + 1)
	ds.PixelData = ds.pixel_array.tobytes()
	dcm.filewriter.write_file(os.path.join(save_direc, new_name + '.dcm'), ds)

def organize(data_direc, new_direc):
	safe_makedir(new_direc)
	filenames = os.listdir(data_direc)
	for filename in filenames:
		if filename[-3:] == 'dcm':
			print('Processing ' + filename + '...')
			ds = dcm.dcmread(os.path.join(data_direc, filename))
			if ds.file_meta.TransferSyntaxUID.is_compressed is True:
				ds.decompress()		
			cage_number, mouse_number = parse_name(filename)
			cage_direc = os.path.join(new_direc, str(cage_number))
			mouse_direc = os.path.join(cage_direc, mouse_number)
			safe_makedir(mouse_direc)
			dicom_count = count_dicoms(mouse_direc)
			new_name =  mouse_number + '_' + str(cage_number) + '_' + str(dicom_count + 1)
			print('Renaming to ' + new_name + '.dcm ...')
			change_name(ds, mouse_direc, cage_number, mouse_number, dicom_count)


########################################################################################################


if __name__ == '__main__':

	data_direc = '/Users/nicolasquach/Documents/medschool/hiesinger_lab/LAD_echodata/'
	new_direc = '/Users/nicolasquach/Documents/medschool/hiesinger_lab/organized_data/'
	organize(data_direc, new_direc)




