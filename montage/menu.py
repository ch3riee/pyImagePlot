import sys
import os
from montage_manager import Montages
from histogram_manager import Histograms

class Menu:
	'''Display menu and respond to choices when run.'''
	def __init__(self):
		self.montage = Montages()
		self.histogram = Histograms()
		self.choices = {
		"1": self.montage_dir,
		"2": self.montage_from_csv,
		"3": self.vertical_montage_from_csv,
		"4": self.image_hist_from_csv,
		"5": self.image_hist_panda,
		"6": self.quit
		}

	def display_menu(self):
		print("""
PyMontage Menu

1. Create montages from recursively from given directory and sub-directories
2. Create montages from provided CSV files (split by categories or bins)
3. Create vertical montage from provided CSV file
4. Create image histogram from provided CSV file
5. Create image histogram using panda
6. Quit 
""")

	def run(self):
		'''Display the menu and responsd to choices'''
		while True:
			self.display_menu()
			choice = input("Enter an option: ")
			action = self.choices.get(str(choice))
			if action:
				action()
			else:
				print("{0} is not a valid choice".format(choice))

	def enter_dir(self, message = "Provide valid directory"):
		while True:
			provided_dir = raw_input(message)
			if os.path.isdir(provided_dir): break
			else: print("Not a valid directory")

		return provided_dir

	def montage_dir(self):
		input_dir = self.enter_dir("Provide full path to directory to create montages: ")
		output_dir = self.enter_dir("Provide full path to valid direcotry to save montages: ")
		self.montage.input_data(src_path = input_dir, dest_path = output_dir)
		print("Creating montages...")
		self.montage.montages_from_directory()
		print("Saving montages complete.")

	def enter_csv(self, message = "provide path to valid csv"):
		while True:
			provided_csv = raw_input(message)
			if os.path.isfile(provided_csv): break
			else: print("Not a valid file")

		return provided_csv

	def montage_from_csv(self):
		input_csv = self.enter_csv("Provide full path to csv file for creating montages: ")
		image_path = self.enter_dir("Provide path to where images are located: ")
		output_dir = self.enter_dir("Provide full path to valid direcotry to save montages: ")
		self.montage.input_data(src_path = input_csv, dest_path = output_dir, image_src_path = image_path)
		print("Creating montages...")
		self.montage.montage_from_csv_binned()

	def vertical_montage_from_csv(self):
		input_csv = self.enter_csv("Provide full path to csv file for creating montages: ")
		image_path = self.enter_dir("Provide path to where images are located: ")
		output_dir = self.enter_dir("Provide full path to valid direcotry to save montages: ")
		self.montage.input_data(src_path = input_csv, dest_path = output_dir, image_src_path = image_path)
		print("Creating montages...")
		self.montage.montage_from_csv_binned(ncols = 0, nrows = 1)		

		#Adding helper functions
	#X var in an input array to be binned, essentially the column in the csv file you want
	def enter_xvar(self, message = "choose your x variable"):
		providedx_var = raw_input(message)
		return providedx_var

	def enter_sortvar(self, message = "choose your sort variable"):
		providedsortvar = raw_input(message)
		return providedsortvar

	def enter_numbins(self, message = "choose the number of bins"):
		providednumbins = raw_input(message)
		return providednumbins
	
	def enter_thumbsize(self, message = "choose the thumbnail size"):
		providedthumbsize = raw_input(message)
		return providedthumbsize

	def image_hist_from_csv(self):
		#changed to lower case csv not CSV
		input_csv = self.enter_csv("Provide full path to csv file for creating image histogram: ")
		output_dir = self.enter_dir("Provide full path to valid directory to  save image histogram: ")
		#accesses the histogram object it previously used instantiated and calls input_data method
		self.histogram.input_data(src_path = input_csv, dest_path = output_dir)
		print("Creating image histogram...")
		#than it calls the create_image_hist method. changed from self.create_image_hist() to self.montage.create_image_hist()
		self.histogram.create_image_hist()

	#method that calls Damon's Code in Panda
	def image_hist_panda(self):
		#gets all the necessary information from the user
		input_csv = self.enter_csv("Provide full path to csv file for creating image histogram: ")
		output_dir = self.enter_dir("Provide full path to valid directory to  save image histogram: ")
		xvar = self.enter_xvar("Provide X Variable to bin for creating image histogram: ")
		sortvar = self.enter_sortvar("Provide the sort variable for sorting image histogram: ")
		numbins = self.enter_numbins("Provide the number of bins for creating image histogram: ")
		thumbsize = self.enter_thumbsize("Provide the thumbnail size for creating image histogram")
		self.histogram.input_data2(infile = input_csv, outfile = output_dir, x_var = xvar, sort_var = sortvar, num_bins = numbins, thumb_size = thumbsize)
		print("Creating image histogram...")
		#calls the correct histogram method
		self.histogram.create_image_hist_panda()


	def quit(self):
		print("Good bye!")
		sys.exit(0)

if __name__ == "__main__":
	Menu().run()
