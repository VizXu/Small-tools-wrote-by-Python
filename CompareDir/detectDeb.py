# detect the different files between two directorys

import os

def incOrexc(l1,l2):
	inc = []
	exc = []
	if isinstance(l1,list) and isinstance(l2,list):
		len1 = len(l1)
		len2 = len(l2)
		if len1 >= len2:
			for f in l2:
				if f in l1:
					inc.append(f)
				else:
					exc.append(f)
			return inc,exc
		else:
			return incOrexc(l2,l1)
	else:
		return inc,exc

def catchFilesFormDirs(dir1):
	files = []
	if isinstance(dir1,str):
		cDir = os.getcwd()
		os.chdir(dir1)
		files = os.listdir('.')
		os.chdir(cDir)
	return files

def diffFiles(dir1,dir2):
	files1 = []
	files2 = []
	inc = []
	exc = []
	if isinstance(dir1,str) and isinstance(dir2,str):
		files1 = catchFilesFormDirs(dir1)
		files2 = catchFilesFormDirs(dir2)
		inc,exc = incOrexc(files1,files2)
		return inc,exc
	else:
		return inc,exc

if __name__ == '__main__':
	#print diffFiles('/home/user/Desktop/62022-tag/Sources/Packages/debian','/home/user/Desktop/SecurityPatch/xar/SecurityUpdate_2017Novrollup-1.0hp2a-ThinPro-6.2')
	l1,l2 = diffFiles('/home/user/Desktop/62022-tag/Sources/Packages/debian','/home/user/Desktop/SecurityPatch/xar/SecurityUpdate_2018Aprilrollup-1.0hp1a-ThinPro-6.2')
	print "inc = ",l1
	print "------------------------------------\n\n"
	print "exc = ",l2
