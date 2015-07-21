
#imports for the original code
import heapq
import csv
import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageOps
#imports for Damon's Modified Code
import pandas as pd
import sys

class Histograms:
	''' Create and Manage Histograms'''
	def __init__(self):
		print "Beginning Process"
	
	def input_data(self, src_path, dest_path):
		self.src_path = src_path
		self.dest_path = dest_path

	def input_data2(self, infile, outfile, x_var, sort_var, num_bins, thumb_size):
		self.infile = infile
		self.outfile = outfile
		self.x_var = x_var
		self.sort_var = sort_var
		self.num_bins = int(num_bins)
		self.thumb_size = int(thumb_size)


	def create_image_hist(self):
		f = open(self.src_path, 'rb')
		data = csv.reader(f)
				#initializing the heapq to be read into 
		heap = []
		#initializing the dict to be read into
		bins = {}
		#for loop to read through the csv file
		for row in data:
			#first read the bin into an int
			bin = int(row[1])
			#check if this key already exists in the dict
			#if the bin is not in the bins
			if bin not in bins.keys():
				#if not create a new list at that bin index in the dict
				bins[int(bin)] = []
			#either way append the tuple to the list at the right bin
			#appending the path and appending the value together at the indexed bin
			bins[int(bin)].append((int(row[2]), row[0]))
			#pushing the value and path combination onto the heap
			#heappush(heap, (int(row[2]), row[0]))    bins
		#have now finished reading in all the data, now must make all the lists, min heaps with heapq
		#for loop to do this
		#find the max value of keys so can have the appropriate number of bins
		listbin = bins.keys()
		biggestbin = int (max(listbin))
		height = 0
		index = 0
		for key in bins:
			#changing every list into a heapq
			heapq.heapify(bins[key])
			length  = len(bins[key])
			#getting the tallest height
			if height<length:
				height=length
		#getting the total number of bins
		NumBins = biggestbin
		#size of each image
		size = 40
		size1 = size 
		graphH = (size1 * height) 
		graphW = size1 * NumBins
		#creating the background window
		img = Image.new('RGB',(graphW,graphH),(255,255,255))
		SIZES = size, size
		#for loop to loop through each bin and paste
		for key in bins:
			theQ = bins[key]
			#initializing the yCoord as the very bottom of the graph
			yCoord = graphH-size1
			xCoord = key * size1
			#while loop to loop through the heapq and paste the images one by one from bottom up
			while len(theQ) != 0:
			#getting the image path 
				popped = heapq.heappop(theQ)
				path = popped[1]
				im = Image.open(path)
				im.thumbnail(SIZES, Image.ANTIALIAS)
				image_size = im.size
				thumb = ImageOps.fit(im, SIZES, Image.ANTIALIAS, (0.5,0.5))
				img.paste(thumb,(xCoord,yCoord))
				yCoord = yCoord - size1

		#saving the image 
		img.save(self.dest_path + "hist.png")    
		print "...done."

#Damon's Panda Code
	def create_image_hist_panda(self):
		# read in data file as pandas DataFrame object (df)
		df = pd.read_csv(self.infile)

		# option to sample the dataframe
		df = df.sample(n=1048576)

		

		# create 'x_bin' column in df using pandas.cut()
		df['x_bin'] = pd.cut(df[self.x_var],self.num_bins,labels=False)

		# find length of largest bin using groupby method
		bin_max = df.groupby('x_bin').size().max()

		# use bin_max, num_bins, and thumb_side to determine size of canvas
		px_w = (self.thumb_size) * self.num_bins
		px_h = (self.thumb_size) * bin_max
		print str(px_w)+'w',str(px_h)+'h'

		# build canvas (final triplet is the color of background, currently dark grey)
		canvas = Image.new('RGB',(px_w,px_h),(50,50,50))

		# set thumbnail size tuple using thumb_size
		thumb_px = (self.thumb_size,self.thumb_size)

		print "Building image..."

		# make a list of unique bins
		bins = list(set(list(df.x_bin)))

		# build image bin by bin
		for item in bins:
			# select rows of df in bin
			tmp = df[df.x_bin==item]

			# sort the resulting DataFrame (tmp) by the sorting variable
			tmp = tmp.sort(self.sort_var)

			# reset index because we'll use the index in a loop
			tmp.reset_index(drop=True,inplace=True)

			# define x and y coordinates for pasting
			y_coord = px_h
			x_coord = self.thumb_size * item

			# loop over rows in tmp
			n = len(tmp.index)
			for i in range(n):
				print x_coord,y_coord
				thumb = Image.open(tmp.filename.loc[i])
				thumb.thumbnail(thumb_px,Image.ANTIALIAS)
				canvas.paste(thumb,(x_coord,y_coord))
				y_coord = y_coord - self.thumb_size

		print "...done."

		print "Saving image..."

		# save written canvas to outfile
		canvas.save(self.dest_path + "hist.png")

		# optional: crop image then save
		#top = px_h/2
		#canvas.crop((0,top,px_w,px_h)).save(outfile.rstrip(".png")+"_cropped.png")

		print "...done."

#only executed if not called by another module. Allows you to call this directly as well.
if __name__ == "__main__":
	in_file = "/Users/myazdaniUCSD/Dropbox/Broadway_processed_data/processedData/dom_HSV_small_sample.csv"
	image_dir = "/Users/myazdaniUCSD/Dropbox/Broadway_processed_data/broadway_images_sample/"
	out_file = "/Users/myazdaniUCSD/Desktop/"
	a_histogram = Histograms()
	#CHANGED to input_data from intput data
	a_histogram.input_data(src_path = in_file, dest_path = out_file)
	#what about for the pandas one?


