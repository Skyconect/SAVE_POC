import pandas as pd
import os,shutil
import numpy as np

import re,json

class Extract:
	def __init__(self,*args,**kargs):
		self.filename= kargs.get("file")
		try:
			self.df = pd.read_csv(self.filename)
		except FileNotFoundError:
			print("No such file {}".format(self.filename))

	def convert_asesment_to_field(self,*args,**kargs):
		self.filename= kargs.get("filename")
		negative_assesment ="VIA neg"
		new_rows =[]
		total_rows = self.df.shape[0]
		for index,row in self.df.iterrows():
			print("Processing {} % ".format(round((index/total_rows*100))),end="\r")		
			try:
				r_assesment = json.loads(row.get("reviewer_assessment","")).get("assessment")

				row["reviewer_assessment"]=r_assesment

			except TypeError:
				print("got nan")
			except AttributeError:
				print("no attribut")

			
			new_rows.append(row)
		
		print("done")
		self.df_extract = pd.DataFrame(new_rows)

		self.df_extract.to_csv(self.filename,index=False)

		pass

	def convert_assesment_to_binary(self,*args,**kargs):
		self.filename= kargs.get("filename")
		negative_assesment ="VIA neg"
		new_rows =[]
		total_rows = self.df.shape[0]
		for index,row in self.df.iterrows():
			print("Processing {} % ".format(round((index/total_rows*100))),end="\r")		

			if str(row.get("provider_assessment","")).strip().lower()==negative_assesment.strip().lower():
				row["provider_assessment"]=0
			else:
				row["provider_assessment"]=1

			# print(row["id"],row.get("reviewer_assessment",""))

			try:
				r_assesment = json.loads(row.get("reviewer_assessment","")).get("assessment")

				if r_assesment.strip().lower()==negative_assesment.strip().lower():
					row["reviewer_assessment"]=0
				else:
					row["reviewer_assessment"]=1

			except TypeError:
				print("got nan")
			except AttributeError:
				print("no attribut")

			
			new_rows.append(row)
		
		print("done")
		self.df_extract = pd.DataFrame(new_rows)

		self.df_extract.to_csv(self.filename,index=False)

	def extract_patient_info_to_csv(self,*args,**kargs):
		self.filename= kargs.get("filename")
		new_rows =[]
		for index,row in self.df.iterrows():
			data = json.loads(row.get("data"),strict=False)

			new_row ={"id":row.get("case_id"),"fname":data.get("fname",""),"mname":data.get("mname",""),"lname":data.get("lname",""),"phone_number":data.get("phone_number","")}

			new_rows.append(new_row)

			print(row.get("case_id"),end="\r")

		print(" done ")

		self.df_extract = pd.DataFrame(new_rows)

		self.df_extract.to_csv(self.filename,index=False)



	def extract_data_to_csv(self,*args,**kargs):
		self.filename= kargs.get("filename")
		new_rows =[]
		for index,row in self.df.iterrows():
			data = json.loads(row.get("data"),strict=False)
			new_row ={"id":row.get("case_id"),"screen_date":data.get("screen_date"),"age":data.get("age"),"hiv_status":data.get("hiv_status"),"parity":data.get("parity"),"reviewer_assessment":data.get("assessment"),"country":data.get("country"),"region":data.get("region"),"district":data.get("ccs_facility_no"),"image1":data.get("photo_1"),"image2":data.get("photo_2"),"image3":data.get("photo_3")}

			new_rows.append(new_row)

			print(row.get("case_id"),end="\r")

		print(" done ")

		self.df_extract = pd.DataFrame(new_rows)

		self.df_extract.to_csv(self.filename,index=False)


class MergeLocation:
    def __init__(self,*args,**kargs):
        self.file_location= kargs.get("file_location")
        self.file_meta= kargs.get("file_meta")
        try:
            self.df_location = pd.read_csv(self.file_location)
            self.df_meta = pd.read_csv(self.file_meta)

            self.df_meta.update(self.df_location)

            print(self.df_meta.head)
            
            self.df_meta.to_csv(self.file_meta,index=False)

        except FileNotFoundError:
            print("Error: file not fund ")

        
if __name__ == '__main__':
	# Extract(file="meta_data_all.csv").extract_data_to_csv(filename="new_meta.csv")
	Extract(file="new_meta.csv").convert_asesment_to_field(filename="meta_data.csv")

	# Extract(file="new_meta.csv").convert_assesment_to_binary(filename="meta_data.csv")
	# Extract(file="meta_data_all.csv").extract_patient_info_to_csv(filename="patient_info.csv")
    # MergeLocation(file_location="patient_info.csv",file_meta="new_meta.csv")
	
	# df = pd.read_csv("reveiwer_meta_data.csv")
	# print(df.head)


# {"form_name":"Patient data capture form","form_id":"1009","patient_id":"9Tqw3NwrHeItpkD0v-sadNL","ccs_providers_full_name":"Loveness ","ccs_providers_phone_no":"0785643164","screen_date":"July 01, 2016","fname":"Happy ","lname":"Magoma ","phone_number":"0769845324","age":"January 10, 1987","parity":"586","ccs_no":"0886688680958688568","patient_received_pitc":"Yes","hiv_status":"Negative","assessment":"Suspect Cancer","visit_status":"Postponed cryo","photo_1":"uploads/img_20160701_162527_2.png"}


# {"to_reviewer":1,"ccs_providers_full_name":"Rachel mjatta","ccs_providers_phone_no":"0764181092","screen_date":"November 13, 2018","fname":"zainabu","mname":"azizi","lname":"abdala","phone_number":"0715842033","age":"36","parity":"3","patient_received_pitc":"Yes","ccs_facility_no":"mbezi h\/s","ccs_no":"0030","hiv_status":"Negative","assessment":"VIA neg","visit_status":"New client (never been screened)","photo_1":"public\/uploads\/img_20181113_124157_7565.png","photo_2":"public\/uploads\/img_20181113_124315_5931.png","photo_3":"public\/uploads\/img_20181113_124403_5086.png","patient_id":"DQfUiXiWeafgnlRjacsotBq","form_version":"1011"}


# SELECT 
#     case_id,
#     `form_data`.`date_data_created`,
#     `users`.`user_id`,
#     `users`.`participant_name`,
#     `facilities`.`facility_id`,
#     `facilities`.`facility_name`,
#     `country`.`country_name`,
#     `district`.`district_name`,
#     `region`.`region_name`
# FROM
#     form_data
#         LEFT JOIN
#     `users` ON (`users`.`user_id` = `form_data`.`creator_id`)
#         LEFT JOIN
#     `user_facility` ON (`user_facility`.`user_id` = `users`.`user_id`)
#         LEFT JOIN
#     `facilities` ON (`facilities`.`facility_id` = `user_facility`.`facility_id`)
#         LEFT JOIN
#     `district` ON (`district`.`district_id` = `facilities`.`district_id`)
#         LEFT JOIN
#     `region` ON (`region`.`region_id` = `district`.`region_id`)
#         LEFT JOIN
#     `country` ON (`country`.`country_id` = `region`.`country_id`);
        

