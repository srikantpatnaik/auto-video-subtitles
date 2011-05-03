#!/usr/bin/python
from subprocess import Popen, PIPE
import os

def srt_create(input_file):
        """Creates a subtitles file after getting duration of video."""
        stdout = Popen('ffmpeg -i %s 2>&1  |grep Duration|cut -d , -f 1|cut -d : -f 3-4|cut -d . -f 1' %input_file, shell=True, stdout=PIPE).stdout
            
	#get the pipe output in the form min:sec
        output = stdout.read()
            
        #store output in an array
        duration=[]
        duration = output.strip().split(":")
        mins = duration[0]
        secs = duration[1]
            
	#convert string to integer
        int_mins=int(mins)  
        int_secs=int(secs) 
	#length of the video in seconds
        total_secs=int_mins*60 + int_secs
                
        def split_secs(seconds):
                 return seconds/3600, (seconds%3600)/60, seconds%60
    
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
         stdout = Popen('mencoder %s -sub 2.srt -o converted_videos/%s -oac copy -ovc lavc -lavcopts vbitrate=1200' % (input_file , output_file) , shell=True, stdout=PIPE).stdout
     print "\nConverting %s to %s " %(input_file,output_file)
     stdout.read()
     return 

stdout = Popen('ls -1 *.avi ',shell=True, stdout=PIPE).stdout

video_files=[]
#get the list of files from pipe output
video_files = stdout.read()

#store output in an array
video_files = video_files.split()

for input_file in video_files:
        output_file = '%s_%s' %('subs', input_file)
        srt_create(input_file) 
        rendering_text(input_file, output_file)
        
