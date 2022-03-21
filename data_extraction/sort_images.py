import pandas as pd
import os,shutil


import re,json

class SortImages:
	def __init__(self,*args,**kargs):	
		self.filename= kargs.get("meta_data","image_meta_data.csv")
		self.all_images_dir= kargs.get("cervical_images","")
		# trqining folder
		self.positive_dir="positive_train"
		self.negative_dir="negative_train"
		self.positive_suspect_dir = "positive_suspect_train"
		self.positive_only_dir = "positive_only_train"
		# validation folder
		self.positive_validation_dir="positive_validation"
		self.negative_validation_dir="negative_validation"
		self.positive_suspect_validation_dir = "positive_suspect_validation"
		self.positive_only_validation_dir = "positive_only_validation"

		self.image_list = os.listdir(self.all_images_dir)
		self.non_reviwed_cases=0

		try:
			os.mkdir(self.positive_dir)
			os.mkdir(self.negative_dir)
			os.mkdir(self.positive_suspect_dir)
			os.mkdir(self.positive_only_dir)
			os.mkdir(self.positive_validation_dir)
			os.mkdir(self.negative_validation_dir)
			os.mkdir(self.positive_suspect_validation_dir)
			os.mkdir(self.positive_only_validation_dir)

		except FileExistsError:
			print("{} and {} directories exists ".format(self.positive_dir,self.negative_dir))

		try:
			self.df = pd.read_csv(self.filename)
			self.separate()
		except FileNotFoundError:
			print("The file {} not ound".format(self.filename))
	

	def separate(self,*args,**kargs):
		total_rows = self.df.shape[0]
		for index,row in self.df.iterrows():
			print("Processing {} % ".format(round((index/total_rows*100))),end="\r")
			three_images=[row["image1"],row["image2"],row["image3"]]
			available_images=[]
			for image in re.findall('([-\w]+\.(?:jpg|gif|png))', str(three_images)):
				if len(image)>0:
					available_images.append(image)
			# print(available_images)
			self.copy_image_if_exist(images=available_images,assesment=row["reviewer_assessment"],position =round((index/total_rows*100)))
			
		print("proessing complete")
	
	def training_vlaidation_split(self,*args,**kargs):
		
		images_dir= kargs.get("folder_to_split","")
		image_list = os.listdir(images_dir)

		


	def copy_image_if_exist(self,*args,**kargs):
		negative_assesment ="VIA neg"
		positive_only_assesment =["VIA+ for cryotherapy","VIA+ for LEEP"]
		positive_suspect_assesment = "Suspect Cancer"
		positive_only_assesment_Key = "VIA+"
		poor_image_quality_keyword = "poor"

		images_to_copy= kargs.get("images",[])
		position= kargs.get("position",0)

		if position > 80:
			self.positive_dir = self.positive_validation_dir
			self.negative_dir = self.negative_validation_dir
			self.positive_suspect_dir = self.positive_suspect_validation_dir
			self.positive_only_dir = self.positive_only_validation_dir

		try:
			assesment = json.loads(kargs.get("assesment","")).get("assessment")
			comment = json.loads(kargs.get("assesment","")).get("comment")
			if comment.strip().lower().__contains__(poor_image_quality_keyword.strip().lower()):
				pass
			else:
				for image_to_copy in images_to_copy:
					if self.image_list.__contains__(image_to_copy):
						# print("Copying {}".format(image_to_copy))
						if assesment.strip().lower() == negative_assesment.strip().lower():
							shutil.copy2(os.path.join(self.all_images_dir,image_to_copy), self.negative_dir, follow_symlinks = False)
						else:

							shutil.copy2(os.path.join(self.all_images_dir,image_to_copy), self.positive_dir, follow_symlinks = False)

	# 
							if assesment.strip().lower() == positive_suspect_assesment.strip().lower():
								shutil.copy2(os.path.join(self.all_images_dir,image_to_copy), self.positive_suspect_dir, follow_symlinks = False)
								pass

	# 
							if assesment.strip().lower().__contains__(positive_only_assesment_Key.strip().lower()) :
								shutil.copy2(os.path.join(self.all_images_dir,image_to_copy), self.positive_only_dir, follow_symlinks = False)
								pass
							
		except Exception:
			self.non_reviwed_cases+=1
			print("Not Reviewed {}".format(self.non_reviwed_cases),end="\r")


if __name__ == '__main__':
	# SortImages(meta_data="new_meta.csv",cervical_images="sevia_ave_Tanzania")
	SortImages(meta_data="new_meta.csv",cervical_images="images_tz")


