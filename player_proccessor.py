#import csvmapper
#%matplotlib inline
import csv 
from stat_calculation import check_shot_type
from stat_calculation import calculatePercentages, identifyPlayer, identifyPlayerDB, incrementShotData, appendPlayer


#database stuff
import sqlite3



# import matplotlib.pyplot as plt

# import seaborn as sns
#player
#0-player_id 1-firstname 2-lastname 3-position 4-height 5-weight 6-byear 7-rookie

#generating the playerlist that shows up in the drop down in main.html
def selectPlayersList():
		conn = sqlite3.connect('player.db')
		cur = conn.cursor() 
		table_name = "player"
		column_name = "playername"

		cur.execute("SELECT DISTINCT playername FROM player ORDER BY playername ASC;")
		all_rows = cur.fetchall()
		
		conn.commit()
		conn.close()

		return all_rows

#find the selected player in our player.db
def queryPlayerDB(playername, playerNameDict):
		conn = sqlite3.connect('player.db')
		cur = conn.cursor() 

		cur.execute("SELECT * FROM player WHERE playername = ?;", (playername,))
		player_base = cur.fetchall()



		playerNameDict["Player Name"] = player_base[0][1]
		playerNameDict['Born: '] = player_base[0][5]
		playerNameDict['Rookie Year: '] = player_base[0][6]
		playerNameDict['Position: '] = player_base[0][2]
		playerNameDict['Weight: '] = player_base[0][4]
		playerNameDict['Height: '] = player_base[0][3]
		playerNameDict['player_id'] = player_base[0][0]
		
		conn.commit()
		conn.close()


		return playerNameDict

def queryPlayerGameDB(playerID):
		conn = sqlite3.connect('playerGame.db')
		cur = conn.cursor()
		cur.execute("SELECT game FROM playerGame WHERE shooter = ?;", (playerID,)) 
		gameAppearances = list(cur.fetchall())
		COLUMN = 0
		games=[game[COLUMN] for game in gameAppearances]
		conn.commit()
		conn.close()

		return games



def generatePlayerShotsNew(filename, playerNameDict, playerID , games, quarters):
	with open(filename, 'rU') as open_file:
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

					#if its the desired season 
					if entry_dict['game'] in games:

						#pull the player id out 
						#print entry_dict
						desiredPlayer = entry_dict['shooter']

						#only store in dictionary if the players match
						if playerID == desiredPlayer:


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
								playerShotData = playerNameDict['shot']

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
									 	if defender_id not in playerNameDict[defender_key]:
									 		playerNameDict[defender_key][defender_id] = {}

									 	defender = playerNameDict[defender_key][defender_id]

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

									if passer_id not in playerNameDict[passer_key]:
								 		playerNameDict[passer_key][passer_id] = {}

								 	passer = playerNameDict[passer_key][passer_id]
									# if shot_type == 'FG':
									appendPlayer(passer, made, 'Successful Assist', 'Failed Assist')

								#less than ten seconds on the shot clock--definitely clutch
								if entry_dict['shot_shot_clock'] != 'NA':
									if float(entry_dict['shot_shot_clock']) <= 10:
											#print "in clutch"
											if shot_type == 'FG':
												clutch_type = 'FG CLUTCH'
											if shot_type == '3PT':
												clutch_type = '3PT CLUTCH'

											incrementShotData(made, playerNameDict['shot'][clutch_type])


										
		

				count=count+1

#complete
#0-	1-id	2-season	3-game	4-quarter	5-team	6-opponent	7-home	8-offense_basket	9-passer	
#10-pass_x	11-pass_y	12-pass_distance	13-recorded_assist	14-pass_shot_clock	
#15-pass_game_clock	16-shooter	17-poss_x	18-poss_y	19-poss_shot_clock	
#20-poss_game_clock	21-shot_x	22-shot_y	23-shot_shot_clock	24-shot_game_clock	
#25-dribbles 26-distance_travelled	27-defender	28-ndd	29-made

def get_player_DB(playerName, seasons,months, quarters):

	#find the player 
	#dictionary that we will append data to to return in form of JSON response
	playerNameDict = {}
	#query the player.db to pull the player info out and plop it into the playerNameDict
	playerNameDict = queryPlayerDB(playerName,playerNameDict)

	#find all the games that the player has shot in
	playerID = playerNameDict['player_id']

	appearances =queryPlayerGameDB(playerID)
	games = dict()

	for game in appearances:
		game = str(game)
		if game[0:4] in seasons:

			#if its the desired month
			if game[4:6] in months:
				games[game] = ""

	playerNameDict['shot'] = {}

	playerShotData = playerNameDict['shot']

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
	playerShotData['Games Played:'] = len(games)


	#maintain FG defenders
	playerNameDict['FG defender'] = {}

	#maintian 3PT defenders
	playerNameDict['3PT defender'] = {}

	#maintain FG passers
	playerNameDict['FG passer'] = {}

	#maintain 3PT passers
	playerNameDict['3PT passer'] = {}

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



	#build data based on player passed in to reduce look up time 
	generatePlayerShotsNew('complete_data.csv', playerNameDict, playerID , games, quarters)

	#identify the defender 
	identifyPlayerDB(playerNameDict['FG defender'], "Defensive Player Name: ")
	identifyPlayerDB(playerNameDict['3PT defender'],"Defensive Player Name: ")

	#identify the passer
	identifyPlayerDB(playerNameDict['FG passer'], "Assist Player Name: ")
	identifyPlayerDB(playerNameDict['3PT passer'], "Assist Player Name: ")


	#identify defenders and passers based on their ID's
	#print playerShotData['GAME_COUNT']
	calculatePercentages( '3PT%', player3PTData, playerShotData)

	calculatePercentages( 'FG%', playerFGData, playerShotData)
	calculatePercentages( 'FG CLUTCH%', playerFGClutch, playerShotData)
	calculatePercentages( 'FG CLUTCH%',  player3PTClutch, playerShotData)



	return playerNameDict
