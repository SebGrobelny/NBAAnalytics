#import csvmapper
#%matplotlib inline
import csv 
from stat_calculation import check_shot_type
from stat_calculation import calculateShot, calculatePercentages, identifyPlayer

import matplotlib.pyplot as plt

import seaborn as sns
#player
#0-player_id 1-firstname 2-lastname 3-position 4-height 5-weight 6-byear 7-rookie


#complete
#0-	1-id	2-season	3-game	4-quarter	5-team	6-opponent	7-home	8-offense_basket	9-passer	
#10-pass_x	11-pass_y	12-pass_distance	13-recorded_assist	14-pass_shot_clock	
#15-pass_game_clock	16-shooter	17-poss_x	18-poss_y	19-poss_shot_clock	
#20-poss_game_clock	21-shot_x	22-shot_y	23-shot_shot_clock	24-shot_game_clock	
#25-dribbles 26-distance_travelled	27-defender	28-ndd	29-made


def processPlayerDictionary(filePath, playerNameDict, completeDict, playerIdDict):

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
					#Build a dictionary for each player
					#primary key is name
					entry_name = {}

					#primary key is id
					entry_id = {}


					#maintain attribute count so that we know when we have the id
					attr_count = 0

					#this will be the first name last name primary key used by the playerDict
					first_last=""

					for attr, value  in zip(attr_list,row):
						if attr_count == 0:
							#set the current player ID so that completeDict can reference later
							curPlayerId = value
							#print curPlayerId

							#set the ID inside of playerDict so that lookup will be fast
							entry_name[attr] = value

							

						#append the first name
						elif attr_count == 1:
							first_last = value

							entry_id[attr] = value

						#append the last name
						elif attr_count == 2:
							first_last = first_last+" "+value
							entry_id[attr] = value

						else:
							#print value
							entry_name[attr] = value
							entry_id[attr] = value


						attr_count = attr_count+1
						#print entry_dict

					playerNameDict[first_last] = entry_name
					#print playerDict[first_last]

					#will get populated by actual stats later the point is to create an association with each
					#player ID and a dictionary 
					completeDict[curPlayerId] = {}

					#create a dictionary by player id as well
					playerIdDict[curPlayerId] = entry_id



				count=count+1
			#print playerDict
			#return value_list

def generatePlayerAssist(filePath, playerCompleteDict):
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

					#associate the headers with the given row to make accessing variables from rows clear to understand
					for attr, value  in zip(attr_list,row):
						entry_dict[attr] = value

					#pull the player id out 
					#print entry_dict
					playerID = entry_dict['passer']

					if playerID in playerCompleteDict:

							#estabilish empty dictionary if no entry associated with current season for current player
							if entry_dict['season'] not in playerCompleteDict[playerID]:
								playerCompleteDict[playerID][entry_dict['season']] = {}

							#making hashing look cleaner so use intermediary variables
							playerSeason = playerCompleteDict[playerID][entry_dict['season']]



							#estabilish empty dictionary if no entry associated with current game for current player

							if entry_dict['game'] not in playerSeason:
							 	playerSeason[entry_dict['game']] = {}


							playerGame = playerSeason[entry_dict['game']]

							#estabilish empty dictionary if no entry associated with current game for current player
							if entry_dict['quarter'] not in playerGame:
								playerGame[entry_dict['quarter']] = {}

							playerQuarter = playerGame[entry_dict['quarter']]

							#now associate the id of the shot with the actual shot attributes
							playerQuarter[entry_dict['id']]= {}

							playerShot = playerQuarter[entry_dict['id']]

							#who shot it?
							playerShot['shooter'] = entry_dict['shooter']


							#what time was the pass made?
							playerShot['pass_clock'] = entry_dict['poss_shot_clock']

							#how far was it passed
							playerShot['pass_distance'] = entry_dict['pass_distance']

							#what time was the shot made?
							playerShot['shot_clock'] = entry_dict['shot_game_clock']


							#what time was the shot made?
							playerShot['shot_clock'] = entry_dict['shot_game_clock']




#pass in playerCompleteDict which is initialized to have each player id as a key associated with an empty hash table
def generatePlayerShots(filePath, playerCompleteDict):
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

					#associate the headers with the given row to make accessing variables from rows clear to understand
					for attr, value  in zip(attr_list,row):
						entry_dict[attr] = value

					#pull the player id out 
					#print entry_dict
					playerID = entry_dict['shooter']

					#catch error bc given player id that is not in players
					if playerID in playerCompleteDict:

							#figure out what shot it was based on the distance to the basket and side the basket is on
							#do this so that shot_x updates based on what arithmetic is performed  
							shot_x = []
							shot_x.append(float(entry_dict['shot_x']))

							shot_y = []
							shot_y.append(float(entry_dict['shot_y']))

							shot_type = check_shot_type(shot_x, shot_y, entry_dict['offense_basket'])



							#estabilish empty dictionary if no entry associated with current season for current player
							if entry_dict['season'] not in playerCompleteDict[playerID]:
								playerCompleteDict[playerID][entry_dict['season']] = {}

							#making hashing look cleaner so use intermediary variables
							playerSeason = playerCompleteDict[playerID][entry_dict['season']]



							#estabilish empty dictionary if no entry associated with current game for current player

							if entry_dict['game'] not in playerSeason:
							 	playerSeason[entry_dict['game']] = {}


							playerGame = playerSeason[entry_dict['game']]

							#estabilish empty dictionary if no entry associated with current game for current player
							if entry_dict['quarter'] not in playerGame:
								playerGame[entry_dict['quarter']] = {}

							playerQuarter = playerGame[entry_dict['quarter']]

							#now associate the id of the shot with the actual shot attributes
							playerQuarter[entry_dict['id']]= {}

							playerShot = playerQuarter[entry_dict['id']]

							#FG 3PT FT etc
							playerShot['shot_type'] =  shot_type


							#made or missed?
							playerShot['made'] = entry_dict['made']

							#where were they?
							playerShot['shot_x'] = shot_x[0]

							playerShot['shot_y'] = shot_y[0]




							#how far did the shooter travel?
							playerShot['distance_travel'] = entry_dict['distance_travelled']

							#who passed it?
							playerShot['passer'] = entry_dict['passer']


							#what time was the pass made?
							playerShot['pass_clock'] = entry_dict['poss_shot_clock']

							#how far was it passed
							playerShot['pass_distance'] = entry_dict['pass_distance']

							#what time was the shot made?
							playerShot['shot_clock'] = entry_dict['shot_game_clock']

							#who was guarding?
							playerShot['defender'] = entry_dict['defender']

							#how close were they?
							playerShot['ndd'] = entry_dict['ndd']

				count=count+1


#method for returning a massive JSON of all players with base attributes (height, weight, )
def get_player( playerName, playerNameDict):

	if playerName not in playerNameDict:
			#player is not here
			return 404
	else:

		#retreieve the base information associated with the playername
		return playerBaseDict[playerName]




def get_player_data( playerName, seasons, months, quarters, playerNameDict, playerCompDict, playerIdDict):

		if playerName not in playerNameDict:
			#player is not here
			return 404

		else:
			#pass the player shots and calculate percentages based on what is currently in the dictionary
			playerID = playerNameDict[playerName]['player_id']

			playerNameDict[playerName]['shot'] = {}

			playerShotData = playerNameDict[playerName]['shot']

			playerShotData['FG'] = {}

			playerFGData = playerShotData['FG']
			# playerFGData['MADE'] = 0
			# playerFGData['ATTEMPT'] = 0

			#averages calculated based on the number of games taken into consideration
			#via game count
			playerFGData['AVG_ATTEMPT'] = 0
			playerFGData['AVG_MADE'] = 0

			#Based on player performance with low shot clock
			playerFGData['CLUTCH'] = 0


			#3PTer attributes
			playerShotData['3PT'] = {}

			player3PTData = playerShotData['3PT']


			#averages calculated based on the number of games taken into consideration
			#via game count
			player3PTData['AVG_MADE'] = 0
			player3PTData['AVG_ATTEMPT'] = 0

			#Based on player performance with low shot clock
			player3PTData['CLUTCH'] = 0

			


			#count of games under consideration
			playerShotData['GAME_COUNT'] = 0


			#maintain FG defenders
			playerNameDict[playerName]['FG defender'] = {}

			#maintian 3PT defenders
			playerNameDict[playerName]['3PT defender'] = {}

			#maintain FG passers
			playerNameDict[playerName]['FG passer'] = {}

			#maintain 3PT passers
			playerNameDict[playerName]['3PT passer'] = {}

			#will plot the shots made unto python matplot thing
			playerShotData['plot'] = {}
			playerShotData['plot']['x'] = []
			playerShotData['plot']['y'] = []

			#iterate through all the seasons passed in by the user
			for season in seasons:
				#verify that player has data associated with the season 
				if season in playerCompDict[playerID]:
					#calculate Average FG 3PT for given player
					calculateShot(playerCompDict[playerID][season], months, quarters, player3PTData, playerFGData, playerNameDict[playerName])

			#plot the data
			sns.set_style("white")
			sns.set_color_codes()
			plt.figure(figsize=(12,11))
			plt.scatter(playerShotData['plot']['y'], playerShotData['plot']['x'])
			plt

			#identify the defender 
			identifyPlayer(playerNameDict[playerName]['FG defender'], playerIdDict, "Defensive Player Name: ")
			identifyPlayer(playerNameDict[playerName]['3PT defender'], playerIdDict, "Defensive Player Name: ")

			#identify the passer
			identifyPlayer(playerNameDict[playerName]['FG passer'], playerIdDict, "Assist Player Name: ")
			identifyPlayer(playerNameDict[playerName]['3PT passer'], playerIdDict, "Assist Player Name: ")


			#identify defenders and passers based on their ID's
			print playerShotData['GAME_COUNT']
			calculatePercentages(player3PTData, playerFGData, playerShotData)

			#return the base player info with the associated stats
			return playerNameDict[playerName]
