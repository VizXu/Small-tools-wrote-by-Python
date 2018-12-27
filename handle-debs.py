# this is a python shell to handle the packages in definitions directory to make a xar automaticly
# 
#
#

import os
import sys

def generate_xml_name(xmlName,version,arch,osNumber,releaseNumber):
	"""
	This function is to generate .xml file according to xml name, product version, machine architectrue, os number and 
	release number,all parameters should be string type
	For example:
		xmlName        ---> hplip
		version        ---> 3.18.12
		arch           ---> ThinPro7.0
		osNumber       ---> 70015
		releaseNumber  ---> hp1a
	xml file:          ---> hplip3.18.12-hp1a-ThinPro7.0_7.0.xml
	"""
	xml = ""
	if isinstance(xmlName,str):
		xml += xmlName
	else:
		xml += "unknow"
	if isinstance(version,str):
		xml += version
	else:
		xml += ""
	xml += "-"
	if isinstance(releaseNumber,str):
		xml += releaseNumber
	else:
		xml += "hp1a"
	xml += "-"
	if isinstance(arch,str):
		if arch == "ThinPro6.0" or arch == "ThinPro7.0":
			xml += arch
		else:
			xml += "ThinPro"
	else:
		xml += "ThinPro"
	if isinstance(osNumber,str):
		if osNumber >= "70000":
			xml += "_7.0"
		elif osNumber >= "60000":
			xml += "_6.0"
		else:
			xml += "_5.0"
	else:
		xml += ""
	return xml

def strip_percent_symbol(debName):
		retName = ""
		if isinstance(debName,str):
			if "%3a" in debName:
				retName = debName.replace("%3a",":")
			else:
				retName = debName
			return retName
		else:
			return None

def extract_deb_name(directory):
	"""
	The name of packages in directory are consist with [name]_[version]_[arch].deb,for instance, acl_2.2.52-3_amd64.deb. 
	This function is to extract names and version numbers from the packages to ([names],[versions]) then transfer it to
	[name version] and return it
	"""
	debs = []
	packages = []
	cwd = "."
	if isinstance(directory,str):
		try:
			cwd = os.getcwd()
			os.chdir(directory)
			debs = os.listdir('.')
		except OSError:
			print "No such files or directory!"
	else:	
		return packages
	for deb in debs:
		plainDeb = strip_percent_symbol(deb)
		splitDeb = plainDeb.split('_')
		name = splitDeb[0]
		version = splitDeb[1]
		package = name
		package += " "
		package += version
		packages.append(package)
	os.chdir(cwd)
	return packages

def generate_xml(xmlName,version,arch,osNumber,releaseNumber,description,packages,architecture,notes = ""):
		xmlFile1 = generate_xml_name(xmlName,version,arch,osNumber,releaseNumber)
		xmlFile = xmlFile1 + ".xml"
		fd = os.open(xmlFile,os.O_RDWR|os.O_CREAT|os.O_APPEND)
		os.write(fd,'<?xml version="1.0" encoding="UTF-8"?>\n')	
		os.write(fd,'<service-pack-description version="1.0">\n')
		name = "  <name>" + xmlFile1 + "</name>\n"
		os.write(fd,name)
		base_release = "  <base_releases>"
		if osNumber >= "70000":
			base_release += "T7X70..."
		elif osNumber >= "60000":
			base_release += "T7X60..."
		else:
			base_release += "T7X50..."
		base_release += "</base_releases>\n"
		os.write(fd,base_release)
		for package in packages:		# add the packages to xml
			packageTag = "  <package>"
			packageTag += package
			packageTag += "</package>\n"
			os.write(fd,packageTag)
		title = '  <title xml:lang="en_US.UTF-8">' # to explain what it to do
		title += description
		title += '</title>\n'
		os.write(fd,title)
		ver = "  <version>1.0</version>\n"
		os.write(fd,ver)
		arc = "  <architecture>"   # shoule be amd64 or i386 or all
		arc += architecture
		arc += "</architecture>\n"
		os.write(fd,arc)
		thinClient = "  <thin_client>all</thin_client>\n"
		os.write(fd,thinClient)
		nts = '  <notes xml:lang="en_EN.UTF-8">'
		if notes == "":
			#no notes specific, use the description as notes
			nts += description
		else:
			nts += notes
		nts += '</notes>\n' 
		os.write(fd,nts)
		end = "</service-pack-description>\n"
		os.write(fd,end)

def handle_packages():
	print """
	Before handling packages, some notes should be noticed, and some necessary parameters should be input to define the xml name and its content.
	For example:
        xmlName        ---> hplip
        version        ---> 3.18.12
        arch           ---> ThinPro7.0
        osNumber       ---> 70015
        releaseNumber  ---> hp1a
    	xml file:      ---> hplip3.18.12-hp1a-ThinPro7.0_7.0.xml	
	"""
	xmlName = raw_input("input xml name,for example hplip ---> ")
	version = raw_input("input version, for example 3.18.12 ---> ")
	osArch  = raw_input("input os arch, for example ThinPro7.0 ---> ")
	osNumber = raw_input("input os number, for example 70015 ---> ")
	releaseN = raw_input("input release number, for example hp1a ---> ")
	architecture = raw_input("input architecture, for example amd64 ---> ")
	description = raw_input("input description of this xar ---> ")
	notes = raw_input("input notes of this xar, if it's none,then the notes defined by description ---> ")
	directory = raw_input("input directory of packages,please make sure there's no other irrelevant files ---> ")
	#print generate_xml_name(xmlName,version,osArch,osNumber,releaseN)
	packages = extract_deb_name(directory)
	#print packages
	generate_xml(xmlName,version,osArch,osNumber,releaseN,description,packages,architecture,notes)	
	pass


if __name__ == "__main__":
	print "start to handle packages..."
	#print generate_xml_name("hplip","3.18.12","ThinPro7.0","70015","hp1a")
	#print strip_percent_symbol("acl_2.2.5-ubuntu%3ax_amd.deb")
	#print extract_deb_name("HPLIP")
	handle_packages()
