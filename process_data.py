import csv
import pickle
import matplotlib.pyplot as plt

cyf_file 		= "CYF Active 2010 to 2016-11-09(1).csv"
bhs_file 		= "Behavioral Health Services.csv"
shelter_file 	= "HomelessShelters(1).csv"

read_csv_files 	= False

class client(object):

	def __init__(self, mci_id, cas_id, birthdate, age, 
		gender, race, in_cyf, in_bhs, in_shelter):
		self.mci_id 	= mci_id
		self.cas_id		= cas_id
		self.birthdate	= birthdate
		self.age		= age
		self.gender		= gender
		self.race		= race
		self.in_cyf		= in_cyf
		self.in_bhs		= in_bhs
		self.in_shelter	= in_shelter

class family(object):
	def __init__(self, cas_id, members = []):
		self.cas_id  = cas_id
		self.members = members

if read_csv_files:
	#  initiate dictionaries
	client_dict = {}
	family_dict = {}

	with open(cyf_file, 'rBU') as f:
		print "Reading in %s" % cyf_file
		csvreader 		= csv.reader(f)
		headers 		= next(csvreader)
		cas_id_col 		= headers.index('CAS_ID')
		mci_id_col 		= headers.index('MCI_ID')
		birthdate_col 	= headers.index('BRTH_DT')
		age_col 		= headers.index('AGE')
		gender_col		= headers.index('GENDER')
		race_col		= headers.index('RACE')
		cas_ids			= []
		for row in csvreader:
			mci_id 		= row[mci_id_col]
			if int(mci_id) > 0:
				if not mci_id in list(client_dict.keys()):
					cas_id 		= row[cas_id_col]
					new_client 	= client(mci_id, cas_id, row[birthdate_col],
						row[age_col], row[gender_col], row[race_col], in_cyf = True,
						in_bhs = False, in_shelter = False)
					client_dict[mci_id] = new_client
				if not cas_id in cas_ids:
					cas_ids 	+= [cas_id]
					new_family	= family(cas_id, [mci_id])
					family_dict[cas_id] = new_family
				else:
					family_dict[cas_id].members += [mci_id]

	with open(bhs_file) as f:
		print "Reading in %s" % bhs_file
		csvreader 		= csv.reader(f)
		headers 		= next(csvreader)
		mci_id_col 		= headers.index('MCI_UNIQ_ID')
		# look at first row seperately to speed up process afterwards
		first_row 		= next(csvreader)
		mci_id 			= first_row[mci_id_col]
		new_client 	= client(mci_id, None, "Unknown",
			"Unknown", "Unknown", "Unknown", in_cyf = False,
			in_bhs = True, in_shelter = False)
		client_dict[mci_id] = new_client
		for row in csvreader:
			if row[mci_id_col] == mci_id:
				continue
			else:
				mci_id 		= row[mci_id_col]
				if mci_id in list(client_dict.keys()):
					# print "Found match: %s" % mci_id
					client_dict[mci_id].in_bhs = True
				else:
					new_client 	= client(mci_id, None, "Unknown",
						"Unknown", "Unknown", "Unknown", in_cyf = False,
						in_bhs = True, in_shelter = False)
					client_dict[mci_id] = new_client

	with open(shelter_file) as f:
		print "Reading in %s" % shelter_file
		csvreader 		= csv.reader(f)
		headers 		= next(csvreader)
		mci_id_col 		= headers.index('MCI_ID_OR_HMIS_CLIENT_ID')
		for row in csvreader:
			mci_id 		= row[mci_id_col]
			if mci_id in list(client_dict.keys()):
				client_dict[mci_id].in_shelter = True
			else:
				new_client 	= client(mci_id, None, "Unknown",
					"Unknown", "Unknown", "Unknown", in_cyf = False,
					in_bhs = False, in_shelter = True)
				client_dict[mci_id] = new_client	
	with open('client_dict', 'wb') as f:
		pickle.dump(client_dict, f)
	with open('family_dict', 'wb') as f:
		pickle.dump(family_dict, f)

else:
	with open('client_dict', 'rb') as f:
		client_dict = pickle.load(f)
	with open('family_dict', 'rb') as f:
		family_dict = pickle.load(f)


plotlist 		= []
for family in family_dict.values():
	members_in_shelter = 0
	for member in family.members:
		if client_dict[member].in_shelter:
			members_in_shelter += 1
	for i in xrange(members_in_shelter):
		plotlist += [members_in_shelter-1]

plt.hist(plotlist)
plt.xlabel("Number of family members who are also in shelter")
plt.ylabel("Number of people in shelter (with family data available from CYF)")
plt.show()


# total_cyf 		= 0
# cyf_and_shelter = 0
# cyf_shelter_bhs = 0
# for client in client_dict.values():
# 	if client.in_shelter:
# 		if client.cas_id != None:
# 			print client.cas_id
# 			print "family members: %d" % (len(family_dict[client.cas_id].members) - 1)
	# if client.in_cyf:
	# 	total_cyf += 1
	# 	if client.in_shelter == True:
	# 		cyf_and_shelter += 1
	# 		if client.in_bhs == True:
	# 			cyf_shelter_bhs += 1


# print "Total CYF: %d" % total_cyf
# print "CYF and shelter %d" % cyf_and_shelter
# print "CYF and shelter and bhs %d" % cyf_shelter_bhs

