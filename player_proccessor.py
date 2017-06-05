#import csvmapper
#%matplotlib inline
import csv 
from stat_calculation import check_shot_type
from stat_calculation import calculatePercentages, identifyPlayer, incrementShotData, appendPlayer

# import matplotlib.pyplot as plt

# import seaborn as sns
#player
#0-player_id 1-firstname 2-lastname 3-position 4-height 5-weight 6-byear 7-rookie


#complete
#0-	1-id	2-season	3-game	4-quarter	5-team	6-opponent	7-home	8-offense_basket	9-passer	
#10-pass_x	11-pass_y	12-pass_distance	13-recorded_assist	14-pass_shot_clock	
#15-pass_game_clock	16-shooter	17-poss_x	18-poss_y	19-poss_shot_clock	
#20-poss_game_clock	21-shot_x	22-shot_y	23-shot_shot_clock	24-shot_game_clock	
#25-dribbles 26-distance_travelled	27-defender	28-ndd	29-made
def processTeamDictionary(filePath, teamNameDict, teamDict):
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
				print row
				#create the dictionary skeleton used 
				if count == 0:
					#store the initial row 
					attr_list = row
					
				else:
					#Build a dictionary for each player
					#primary key is name
					entry_name = {}


					#maintain attribute count so that we know when we have the id
					attr_count = 0

					for attr, value  in zip(attr_list,row):
						entry_name[attr] = value
					
					print entry_name
					team_name = entry_name['team_name']

					teamNameDict[team_name] = {}
					teamNameDict[team_name] ['Team City:'] = entry_name['team_city']
					teamNameDict[team_name] ['Alias:'] = entry_name['team_alias']
					teamNameDict[team_name] ['Conference:'] = entry_name['conference']
					teamNameDict[team_name] ['team_id'] = entry_name['team_id']


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

					#format and append all entries
					playerNameDict[first_last] = {}
					playerNameDict[first_last]['Born: '] = entry_name['byear']
					playerNameDict[first_last]['Rookie Year: '] = entry_name['rookie']
					playerNameDict[first_last]['Weight: '] = entry_name['weight']
					playerNameDict[first_last]['Height: '] = entry_name['height']
					playerNameDict[first_last]['player_id'] = entry_name['player_id']
					#print playerDict[first_last]

					#will get populated by actual stats later the point is to create an association with each
					#player ID and a dictionary 
					completeDict[curPlayerId] = {}

					#create a dictionary by player id as well
					playerIdDict[curPlayerId] = entry_id



				count=count+1
			#print playerDict
			#return value_list
# def generateTeamData(filePath, teamCompleteDict, teamNameDict, seasons, months, quarters ):

# 	print "Team data"




#pass in playerCompleteDict which is initialized to have each player id as a key associated with an empty hash table
def generatePlayerShots(filePath, playerCompleteDict, playerNameDict, desiredPlayer, playerName, seasons, months, quarters):
	
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

					#only store in dictionary if the players match
					if playerID == desiredPlayer:

						#catch error bc given player id that is not in players
						if playerID in playerCompleteDict:

							#if its the desired season 
							if entry_dict['season'] in seasons:

								#if its the desired month
								if entry_dict['game'][4:6] in months:

									#if its the desired quarter
									if entry_dict['quarter'] in quarters:


										made = entry_dict['made']
										#figure out what shot it was based on the distance to the basket and side the basket is on
										#do this so that shot_x updates based on what arithmetic is performed  
										shot_x = []
										shot_x.append(float(entry_dict['shot_x']))

										shot_y = []
										shot_y.append(float(entry_dict['shot_y']))

										shot_type = check_shot_type(shot_x, shot_y, entry_dict['offense_basket'])

										#obtain the shot data
										playerShotData = playerNameDict[playerName]['shot']

										#increment the shot 
										incrementShotData(made, playerShotData[shot_type])



										#defender data 
										if shot_type == 'FG':
											defender_key = 'FG defender'
										if shot_type == '3PT':
											defender_key = '3PT defender'

										defender_id = entry_dict['defender']

										if defender_id != "NA":
											#far away defenders have negligible meaining
											if float(entry_dict['ndd']) < 6:
											 	#append defensive player to the shot
											 	if defender_id not in playerNameDict[playerName][defender_key]:
											 		playerNameDict[playerName][defender_key][defender_id] = {}

											 	defender = playerNameDict[playerName][defender_key][defender_id]

											 	# if shot_type == 'FG':
											 	appendPlayer(defender, made, 'Defended Shot', 'Allowed Shot')
										#passer data 
								
										if shot_type == 'FG':
											passer_key = 'FG passer'
										if shot_type == '3PT':
											passer_key = '3PT passer'

										passer_id = entry_dict['passer']
										if passer_id != "NA":
											#append passer to the shot

											if passer_id not in playerNameDict[playerName][passer_key]:
										 		playerNameDict[playerName][passer_key][passer_id] = {}

										 	passer = playerNameDict[playerName][passer_key][passer_id]
											# if shot_type == 'FG':
											appendPlayer(passer, made, 'Successful Assist', 'Failed Assist')

										#less than ten seconds on the shot clock--definitely clutch
										if entry_dict['shot_shot_clock'] != 'NA':
											if float(entry_dict['shot_shot_clock']) <= 10:
													print "in clutch"
													if shot_type == 'FG':
														clutch_type = 'FG CLUTCH'
													if shot_type == '3PT':
														clutch_type = '3PT CLUTCH'

													incrementShotData(made, playerNameDict[playerName]['shot'][clutch_type])


									playerNameDict[playerName]['shot']['Games Played:'] = playerNameDict[playerName]['shot']['Games Played:']+1
	

				count=count+1

# def get_team_data( teamName):
# 	teamNameDict = { }
# 	teamCompDict = { }
# 	processTeamDictionary('teams.csv',teamNameDict, teamCompDict)

# 	print teamNameDict

# 	if teamName not in teamNameDict:
# 		return 404
# 	else:
# 		return teamNameDict[teamName]



def get_player_data( playerName, seasons, months, quarters):
	##Globals for processing that get_commands will use 
		playerNameDict = { }


		#dictionary holding shot data about each player from complete_data.csv, where the key is the ID
		playerCompDict = { }


		#dictionary holding basic player data but the key is the player ID--used for identifying defenders/passers
		playerIdDict = {}


		#want all the players to be in our Name Dictionary
		processPlayerDictionary('players.csv',playerNameDict, playerCompDict, playerIdDict)
		
		if playerName not in playerNameDict:
			#player is not here
			return 404


		else:

			playerID = playerNameDict[playerName]['player_id']




			playerNameDict[playerName]['shot'] = {}

			playerShotData = playerNameDict[playerName]['shot']

			#Based on player performance with low shot clock
			playerShotData['FG CLUTCH'] ={}
			playerFGClutch = playerShotData['FG CLUTCH']

			playerShotData['3PT CLUTCH'] = {}
			player3PTClutch = playerShotData['3PT CLUTCH']

		
			playerShotData['FG'] = {}



			playerFGData = playerShotData['FG']
			# playerFGData['MADE'] = 0
			# playerFGData['ATTEMPT'] = 0

			#averages calculated based on the number of games taken into consideration
			#via game count
			# playerFGData['Made Per Game'] = 0
			# playerFGData['Attempts Per Game'] = 0

		


			#3PTer attributes
			playerShotData['3PT'] = {}

			player3PTData = playerShotData['3PT']


			#averages calculated based on the number of games taken into consideration
			#via game count
			# player3PTData['Made Per Game'] = 0
			# player3PTData['Attempts Per Game'] = 0

			


			#count of games under consideration
			playerShotData['Games Played:'] = 0


			#maintain FG defenders
			playerNameDict[playerName]['FG defender'] = {}

			#maintian 3PT defenders
			playerNameDict[playerName]['3PT defender'] = {}

			#maintain FG passers
			playerNameDict[playerName]['FG passer'] = {}

			#maintain 3PT passers
			playerNameDict[playerName]['3PT passer'] = {}


			#build data based on player passed in to reduce look up time 
			generatePlayerShots('complete_data.csv', playerCompDict, playerNameDict, playerID , playerName, seasons, months, quarters)

			#will plot the shots made unto python matplot thing
			# playerShotData['plot'] = {}
			# playerShotData['plot']['x'] = []
			# playerShotData['plot']['y'] = []

			#plot the data
			# sns.set_style("white")
			# sns.set_color_codes()
			# plt.figure(figsize=(12,11))
			# plt.scatter(playerShotData['plot']['y'], playerShotData['plot']['x'])
			# plt

			#identify the defender 
			identifyPlayer(playerNameDict[playerName]['FG defender'], playerIdDict, "Defensive Player Name: ")
			identifyPlayer(playerNameDict[playerName]['3PT defender'], playerIdDict, "Defensive Player Name: ")

			#identify the passer
			identifyPlayer(playerNameDict[playerName]['FG passer'], playerIdDict, "Assist Player Name: ")
			identifyPlayer(playerNameDict[playerName]['3PT passer'], playerIdDict, "Assist Player Name: ")


			#identify defenders and passers based on their ID's
			#print playerShotData['GAME_COUNT']
			calculatePercentages( '3PT%', player3PTData, playerShotData)
	
			calculatePercentages( 'FG%', playerFGData, playerShotData)
			calculatePercentages( 'FG CLUTCH%', playerFGClutch, playerShotData)
			calculatePercentages( 'FG CLUTCH%',  player3PTClutch, playerShotData)


			#return the base player info with the associated stats
			return playerNameDict[playerName]
