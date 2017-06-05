#import csvmapper
import csv 
from pack.pack_1.stat_calculation import check_shot_type, calculateShot




#generates a list of dictionaries associated with each entry in the CSV passed into it
def generateDictionary(filePath):
	#will store the names of the associated player attributes found in the players.csv
	with open(filePath, 'rU') as open_file:
			#read in the first row to obtain necessary features
			open_reader = csv.reader(open_file)
			value_list = []

			#store the headers in which will be used as keys for the dictionary
			attr_list = []

			#only want the first row the rest will be processed as JSON 
			count = 0
			for row in open_reader:

				#create the dictionary skeleton used 
				if count == 0:
					#store the initial row 
					attr_list = row
					
				else:
					#print row
					#Build a dictionary for each player
					#dictionary who's keys will be the player attributes will return list of these to calling method
					entry_dict = {}
					for attr, value  in zip(attr_list,row):
						entry_dict[attr] = value

					value_list.append(entry_dict)

				count=count+1
			return value_list


#cur_value refers to the value associated with the current key under consideration used to filter results
#entry_key will refer to the key that is being compared against
#keys will be the modified list of keys excluding the current key
def get_Improved(cur_value, entry_key, keys, complete_list):
		#maintain a prev_values and if cur_value != prev_value update 
		result_dict = {}

		#initialize prev Value
		prev_value = complete_list[0][entry_key]

		#total Field Goals 
		total_FG = 0

		made_FG = 0

		#total 3PT
		total_3PT = 0

		#total 3PT
		made_3PT = 0

		#total free throws
		total_FT = 0

		made_FT = 0


		for entry in complete_list:
			shot_dict = {}


			#match playerIDs with shooter ID match up 
			if cur_value == entry[entry_key]:

				if cur_value != prev_value:

				#print entry
				shot_type = check_shot_type(float(entry['shot_x']), float(entry['shot_y']))
				print shot_type
				shot_dict['shot_type'] = shot_type

				#transfer data over to reduce the hash itself
				for var in keys:
					shot_dict[var] = entry[var]

				result_dict.append(shot_dict)

		#return the hash table associated with the current key value
		return result_dict

def getImproved(playerID, complete_list):

	#shot dictionary that will get updated as soon as an attribute i.e. season changes
	attr_dict = {}
	attr_dict['FG_TOTAL'] = 0
	attr_dict['FG_MADE'] = 0
	attr_dict['3PT_TOTAL'] = 0
	attr_dict['3PT_MADE'] = 0
	attr_dict['FT_TOTAL'] = 0
	attr_dict['FT_MADE'] = 0 


#method for determing the amount of field goals a player has made or attempted
def get_complete(playerID,complete_list):
	print "in get_player_complete"
	#complete_list = generateDictionary('data/complete_data.csv')

	player_shots = {}

	#total Field Goals 
	total_FG = 0

	made_FG = 0

	#total 3PT
	total_3PT = 0

	#total 3PT
	made_3PT = 0

	#total free throws
	total_FT = 0

	made_FT = 0

	for entry in complete_list:
		#match playerIDs with shooter ID match up 
		if playerID == entry['shooter']:
			#print entry
			shot_type = check_shot_type(float(entry['shot_x']), float(entry['shot_y']))
			print shot_type

		caclulateShot(shot_type, total_FG, made_FG, total_3PT, made_3PT, total_FT, made_FT)



	print made_FG
	print made_3PT
	#calcuate FG%
	player_shots['FG%'] = float(made_FG)/float(total_FG)

	#calculate FG
	player_shots['FG_TOTAL'] = total_FG

	#calculate 3PT%
	player_shots['3PT%'] = float(made_3PT)/float(total_3PT)

	#calculate 3PT
	player_shots['3PT_TOTAL'] = total_3PT

	player_shots['FT%'] = float(made_FT)/float(total_FT)

	#calculate FT
	player_shots['FT_TOTAL'] = total_FT


	return player_shots
			

#method for determing the amount of field goals a player has made or attempted in a given season
def get_complete_season(playerID, season, complete_list):
	print "in get_player_complete"
	#complete_list = generateDictionary('data/complete_data.csv')

	player_shots = {}

	#total Field Goals 
	total_FG = 0

	made_FG = 0

	#total three pointers
	total_3PT = 0


	made_3PT = 0

	#total free throws
	total_FT = 0

	made_FT = 0


	for entry in complete_list:
		#match playerIDs with shooter ID match up 
		if playerID == entry['shooter'] and season == entry['season']:
			#print entry
			shot_type = check_shot_type(float(entry['shot_x']), float(entry['shot_y']))
			print shot_type

			caclulateShot(shot_type, total_FG, made_FG, total_3PT, made_3PT, total_FT, made_FT)


	print made_FG
	print made_3PT
	print made_FT
	#calcuate FG%
	player_shots['FG%'] = float(made_FG)/float(total_FG)

	#calculate FG
	player_shots['FG_TOTAL'] = total_FG

	#calculate 3PT%
	player_shots['3PT%'] = float(made_3PT)/float(total_3PT)

	#calculate 3PT
	player_shots['3PT_TOTAL'] = total_3PT

	#calculate FT%
	player_shots['FT%'] = float(made_FT)/float(total_FT)

	#calculate FT
	player_shots['FT_TOTAL'] = total_FT


	return player_shots



#method for returning a massive JSON of all players with base attributes
def get_all_players():
	 
	 return player_list



#method for returning a massive JSON of all players with base attributes (height, weight, )
def get_player( playerName, complete_list, player_list):

	#split the user's input of the full name
	fullName = playerName.split(" ") 
	firstName = fullName[0]
	print firstName
	lastName = fullName[1]

	#player_list = generateDictionary('data/players.csv')

	#the list we will return with all the player data back to the JS
	player_data ={}

	for player in player_list:
		#print player['firstname']
		if firstName in player['firstname'] and lastName in player['lastname']:
			player_data['base'] = player
			#pass in player_id so as to extract information from complete_data
			player_data['complete'] = get_complete(player["player_id"],complete_list) 
			return player_data

def get_player_season(playerName, season, complete_list, player_list):

	#split the user's input of the full name
	fullName = playerName.split(" ") 
	firstName = fullName[0]
	print firstName
	lastName = fullName[1]

	#player_list = generateDictionary('data/players.csv')

	#the list we will return with all the player data back to the JS
	player_data ={}

	for player in player_list:
		#print player['firstname']
		if firstName in player['firstname'] and lastName in player['lastname']:
			player_data['base'] = player
			# keys.append(player["player_id"])
			# keys.append(season)
			#pass in player_id so as to extract information from complete_data
			player_data['complete'] = get_complete_season(player['player_id'], 'player_id', season, 'season', complete_list) 
			return player_data



	
