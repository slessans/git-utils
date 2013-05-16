#!/usr/bin/python

import subprocess
import sys
import argparse

# originally from http://davidchambersdesign.com/converting-integers-to-ordinals/
def ordinal(n):
    if 10 < n < 14: return u'%sth' % n
    if n % 10 == 1: return u'%sst' % n
    if n % 10 == 2: return u'%snd' % n
    if n % 10 == 3: return u'%srd' % n
    return u'%sth' % n

parser = argparse.ArgumentParser(description='Sum commit history into list. Helpful for ' + 
								'summarizing release notes eg for test flight. ' +
								'Splits up messages by semi-colon and new lines.')
parser.add_argument('num_commits', metavar='N', type=int, default=1, nargs='?',
                   help='integer. how many previous commits to use in summary. ' +
                   'if 0, just shows last commit. If negative, same as positive so ' +
                   '-3 is the same as 3 and so on.')
                   
parser.add_argument('--sep', dest='sep', type=str, default=";",
                   help='Split up commit messages by this separator (default: ";").')

parser.add_argument('-d', dest='show_details', action='store_const', const=True, default=False,
					help='Show details; shows commit info also')

args = parser.parse_args()
num_commits = args.num_commits;
show_details = args.show_details;
sep = args.sep;

if num_commits == 0 :
	num_commits = 1

if num_commits < 0 :
	num_commits = num_commits * -1
	
output_str = subprocess.check_output("git status 2>/dev/null | tail -n 1", shell=True)
if output_str == "" :
	print "No git repo detected. Please run this inside of a git repo."
	sys.exit(0)

output_str = subprocess.check_output("git log --pretty=format:\"%s\" -" + str(num_commits), shell=True)
lines = output_str.split("\n")

num_commits_str = ''
if num_commits == 1 : 
	num_commits_str = 'commit'
else :
	num_commits_str = str(num_commits) + ' commits'

print 'Summary of last ' +  num_commits_str + ':'
for commit_num, line in enumerate(lines, start=1):
	line = line.strip();
	if ( line == "" ) :
		continue;
	
	if (show_details) :
		if (commit_num == 1) :
			print "  Last commit:"
		else :			
			print "  " + ordinal(commit_num) + " to last commit:"
	
	pieces = line.split(sep)

	for piece in pieces :
		piece = piece.strip()
		if piece == "" :
			continue
		print "    - " + piece	
