#!/usr/bin/env python
from subprocess import Popen, PIPE
import os

os.system('mkdir -p converted_videos')

def split_secs(seconds):
	return seconds/3600, (seconds%3600)/60, seconds%60
    
def srt_create(input_file):
        """Creates a subtitles file after getting duration of video."""
        stdout = Popen('ffmpeg -i %s 2>&1  |grep Duration|cut -d , -f 1|cut -d : -f 2-4|cut -d . -f 1' %input_file, shell=True, stdout=PIPE).stdout

	#get the pipe output in the form min:sec
        output = stdout.read()
            
        #store output in an array
        duration=[]
        duration = output.strip().split(":")
	hrs, mins, secs = [int(i) for i in duration]

	#length of the video in seconds
        total_secs = hrs*3600 + mins*60 + secs
                
	# No. of seconds to show the text on the video
	gap = 5
            
	f = open('1.srt')
            
	lines = [l.strip() for l in f.readlines()]
	lines[lines.index('2')+1] = "%02d:%02d:%02d,000 --> %02d:%02d:%02d,000" %(split_secs(total_secs-gap)+split_secs(total_secs))
	f.close()
            
	f = open('2.srt', 'w')
	for l in lines:
		f.write('%s\n' %l)
	f.close()
	return  

    
def rendering_text(input_file, output_file):
     stdout = Popen('mencoder %s -subpos 85 -sub 2.srt -o converted_videos/%s -oac copy -ovc lavc -lavcopts vbitrate=1200 -subfont-text-scale 3' % (input_file , output_file) , shell=True, stdout=PIPE).stdout
 
     print "Converting %s to %s " %(input_file,output_file)
     stdout.read()
     return 

stdout = Popen('ls -1 *.avi ',shell=True, stdout=PIPE).stdout

video_files=[]
#get the list of files from pipe output
video_files = stdout.read()

#store output in an array
video_files = video_files.split()
#print "Converting %d file(s)." %len(video_files)

for i, input_file in enumerate(video_files):
        output_file = '%s_%s' %('subs', input_file)
	print "Converting %d of %d file(s)..." %(i+1, len(video_files))
        srt_create(input_file) 
        rendering_text(input_file, output_file)
        
