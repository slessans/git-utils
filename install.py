#!/usr/bin/python

import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Install git utils for a mac. By default, will prompt before overwriting anything.")

parser.add_argument('-f', dest='force_copy', action='store_const', const=True, default=False,
					help="Force install the files, that is, don't prompt before overwriting any existing files (default: False).")                   
					
parser.add_argument('-d', dest='destination', nargs='?', default="/usr/bin",
					help='Where to move the files to (default: /usr/bin).')

args = parser.parse_args()
force_copy = args.force_copy;
destination = args.destination;

if destination is None :
	destination = '.'

if len(destination) > 0 and destination[-1] != '/' :
	destination = destination + "/"
	
if not os.path.exists(destination) :
	os.makedirs(destination)
	
if not os.path.isdir(destination) :
	sys.exit("Soething exists at \"" + destination + "\" but it is not a directory.")
	
filenames = ["summarizeGitCommits"];

cp_options = " -i";
if force_copy :
	cp_options = ""

for filename in filenames :
	python_file = filename + ".py"
	dest_file = destination + filename;
	
	retval = subprocess.call("sudo cp" + cp_options + " " + python_file + " " + dest_file, shell=True)
	if retval == 0 :
		# operation was successful
		print python_file + " succesfully copied to " + dest_file
		retval = subprocess.call("sudo chmod +x " + dest_file, shell=True)
		if retval == 0 :
			print "  Changed file permissions to +x"
		else :
			print "  Could not change file permission to +x"
	else :
		print "DID NOT copy " + python_file + " to " + dest_file
	
	
