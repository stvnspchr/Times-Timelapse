import os, shutil
import exifread
import datetime
import time
import glob


#--------------------------------
#--------Times Timelapse---------
#--------------------------------
#-- A tool used for extracting --
#- photos at certain times from -
#------ timelapse sequences -----
#--------------------------------
#-- Created by Steven Speicher --
#------------- 2014 -------------
#--------------------------------

print "\n"
print "Greetings!"
print "I'll help you extract specific image files at certain times."
print "I need a bit of info before beginning."
print "\n"

print "What folder are the images located in?"

p1 = raw_input("Folder: ")
e = True #error
while e:
	if os.path.isdir(p1):
		path = p1 + "/*.*"
		e = False # no errors
	else:
		print "Enter a folder that exists."
	  	p1 = raw_input("Folder: ")

print "\n"

# Prompts for date and time ranges
print "What date ranges do you want to search?"
s_year = raw_input("Starting year: ")
s_month = raw_input("Starting month: ")
s_day = raw_input("Starting day: ")

e_year = raw_input("Ending year: ")
e_month = raw_input("Ending month: ")
e_day = raw_input("Ending day: ")

print "What hour do you want to search for?"
s_hour = raw_input("Hour: (1-24) ")
e_hour = int(s_hour) + 1

# DateTime.date object for searching
s_date = datetime.date(int(s_year), int(s_month), int(s_day))
e_date = datetime.date(int(e_year), int(e_month), int(e_day))

# DateTime.time object for searching
s_time = datetime.time(int(s_hour),0)
e_time = datetime.time(e_hour,0)

# DateTime.datetime object for searching
s_datetime = datetime.datetime.combine(s_date, s_time)
e_datetime = datetime.datetime.combine(e_date, e_time)

# Destination directory for copying
dstdir = "%s/selects/%s_%s_%s" % (p1,s_date,e_date,s_hour)
os.makedirs(dstdir)

print "\n"
print "------------------------"
print "Searching for: "
print "Start date: %s" % s_date
print "End date: %s" % e_date
print "At Time: %s" % s_time
print "------------------------"
print "\n"
print "Searching..."

# Total number of images copied
total = 0
# Tag search for in ExifRead module
TAG = 'EXIF DateTimeOriginal'

for file in glob.glob(path):

	# Open each file in path
	f = open(file, 'rb')

	tags = exifread.process_file(f, details=False)

	# Check for the metadata info that the image was taken
	for tag in tags.keys():
		if tag == TAG:
			img_meta = str(tags[tag])

			# Convert tag to DateTime object
			year = img_meta[0:4]
			month = img_meta[5:7]
			day = img_meta[8:10]

			hour = img_meta[11:13]
			
			# DateTime.date object for image
			img_date = datetime.date(int(year), int(month), int(day))
			# DateTime.time object for image
			img_time = datetime.time(int(hour),0)
			# DateTime.datetime object for image
			img_datetime = datetime.datetime.combine(img_date, img_time)
			
			# Compare searching dates with image date, includes endpoints
			if s_date <= img_date <= e_date:
				# Compare searching times with image time, include front endpoint only
				if s_time <= img_time < e_time:

					# Print to screen, increment total count, process image
					print "File: %s was taken on %s at %s" % (file, img_date, img_time)
					total += 1
					shutil.copy(file, dstdir)

	f.close()

print "\n"
print "------------------------"
print "Results:"
if total==0:
	print "I'm sorry there are no files between"
	print "%s and %s at %s " % (s_date, e_date, s_time)
else: 
	print "%s files were copied" % total
	print "to the folder %s" % dstdir
print "------------------------"
