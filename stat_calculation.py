import math 
import sqlite3



#based on analysis of data and court dimensions the x axis spans the length of the court
#while the y axis spans the width of the court 
#method for determining if the shot taken was a FG, FT or 3PT
def check_shot_type(shot_x, shot_y, offense_basket):

	#need to get the correct x and y distances from the basket
	#47 because that is the location of the baseline so if shooting towards the right
	#player could be lobbing it to the left from the right side of the court
	if shot_x[0] > 47 and offense_basket == 'R':
		shot_x[0] = 94 - float(shot_x[0])
	else:
		#could be the case that player was trying to hit a buzzer beater
		shot_x[0] = shot_x[0]

	#calculate distance to basket and allow for negative values bc our plot is setup with negative_y coordinates
	if shot_y[0] > 25:
		shot_y[0] = float(shot_y[0]) - 50
	else:
		shot_y[0] = 25 - float(shot_y[0])

	#use pythagorean theorem to calculate distance to the basket
	hypotenuse = pow(shot_x[0],2)+ pow(shot_y[0],2)
	distance_to_basket = math.sqrt(hypotenuse)

	#valid three point shot along arc
	if distance_to_basket >= 23.75:
		return "3PT"

	#valid three point shot from the corner
	if distance_to_basket >= 22 and shot_y >= 14:
		return "3PT"

	# if ( shot_x > 15 and shot_x < 16)  and shot_y < 6 :
	# 	return "FT" 

	#not a three point shot
	else:
		# if plot_x ==  plot_y:
			#print "Possible FT"

		return "FG"

#increment either FG or 3PT
def incrementShotData(made, shotData):
	#initialize if not already present
	if 'Total Made' not in shotData:
		shotData['Total Made'] = 0
	if 'Total Attempt' not in shotData:
		shotData['Total Attempt'] = 0



	if made == '1':
						
		shotData['Total Made'] = shotData['Total Made'] + 1
		shotData['Total Attempt'] = shotData['Total Attempt'] + 1

	if made == '0':
		shotData['Total Attempt'] = shotData['Total Attempt'] + 1


def calculatePercentages( percKey,  shotData, returnData):

	#ensure that values exist before trying to calculate 
	if 'Total Made' in shotData and 'Total Attempt' in shotData:
		shotData[percKey] = "{:.3f}".format(float(shotData['Total Made']) / float(shotData['Total Attempt']))
		shotData['Attempts Per Game'] = "{:.3f}".format(float(shotData['Total Attempt']) / float(returnData['Games Played:']))
		shotData['Made Per Game'] = "{:.3f}".format(float(shotData['Total Made']) / float(returnData['Games Played:']))

	# if 'Total Made' in threePTData and 'Total Attempt' in threePTData:
	# 	threePTData['3PT%'] = "{:.3f}".format(float(threePTData['Total Made']) / float(threePTData['Total Attempt']))	
	# 	threePTData['Attempts Per Game'] = "{:.3f}".format(float(threePTData['Total Attempt']) / float(returnData['Games Played:']))
	# 	threePTData['Made Per Game'] = "{:.3f}".format(float(threePTData['Total Made']) / float(returnData['Games Played:']))


#used to identify either the defender or passer associated with a shot
def identifyPlayer(playerBaseDict, playerIdDict, name):
	# print "in ID player"
	for player_id in playerBaseDict:
		# print player_id

		if player_id in playerIdDict:
			# print playerIdDict[player_id]['firstname']
			# print playerIdDict[player_id]['lastname']

			#store the player name in with the id 
			playerBaseDict[player_id][name] = playerIdDict[player_id]['firstname']+" "+playerIdDict[player_id]['lastname']


def identifyPlayerDB(playerNameDict,name):
	#open player database
	conn = sqlite3.connect('player.db')
	cur = conn.cursor() 

	for player_id in playerNameDict:


		cur.execute("SELECT playername FROM player WHERE player_id = ?;", (player_id,))



	conn.commit()
	conn.close()



#used to append either a defender or passer associated with a shot
def appendPlayer(player, made, successKey, failKey):
	
	if successKey not in player:
		player[successKey] = 0

	if failKey not in player:
		player[failKey] = 0

	#player was present for missed shot
	if made == '0':
		player[failKey] = player[failKey]+1
	#player was present for made shot
	else:
		player[successKey] = player[successKey]+1

	#player['shot_type']





# OLD LOGIC--MOST OF THE TIME I HAD PREPROCESSED EVERY PLAYER THIS HOWEVER PROVED INEFFICEINT!!
# def calculateShot(shotDict, months, quarters, threePTData, fgData, returnData):
# 	#len(shotDict['game']) gives us the number of games
# 	#we want to find the number made each game and divide it by the total number of games
# 	# print "in CalculateAverage"

# 	#iterate through all of the games player had in given season
# 	for month in months:
# 		# print month 
# 		for game in shotDict:
# 			#iterate through quarter player had in given game
# 			#verify that the player had a game in the month requested
# 			if int(game[4:6]) == int(month):
# 				# if game == '2015012709':
# 					#print "in game"
# 					for quarter in quarters:
# 						#verify that player actually has data for the given quarter
# 						if quarter in shotDict[game]:
# 							for shot in shotDict[game][quarter]:
# 								# print shotDict[game][quarter]

# 								#made-1 or missed-0 shot 
# 								made = shotDict[game][quarter][shot]['Total Made']

# 								#FG or 3PT?
# 								shot_type = shotDict[game][quarter][shot]['shot_type']


# 								#call helper with fgData
# 								if shot_type == 'FG':
# 									incrementShotData(made, fgData)

								
# 								#call helper with 3ptData
# 								if shot_type == '3PT':
# 									incrementShotData(made, threePTData)



# 								#defender data 
# 								if shot_type == 'FG':
# 									defender_key = 'FG defender'
# 								if shot_type == '3PT':
# 									defender_key = '3PT defender'
									
# 								defender_id = shotDict[game][quarter][shot]['defender']

# 								#TODO factor in defender distance to the player
# 								if defender_id != "NA":
# 								 	#append defensive player to the shot
# 								 	if defender_id not in returnData[defender_key]:
# 								 		returnData[defender_key][defender_id] = {}

# 								 	defender = returnData[defender_key][defender_id]

# 								 	# if shot_type == 'FG':
# 								 	appendPlayer(defender, made, 'Defended Shot', 'Allowed Shot')

# 								 	# if shot_type == '3PT':
# 								 	# 	appendPlayer(defender, made, 'Defended 3PT', 'Allowed 3PT')

# 								#passer data 
# 								if shot_type == 'FG':
# 									passer_key = 'FG passer'
# 								if shot_type == '3PT':
# 									passer_key = '3PT passer'

# 								passer_id = shotDict[game][quarter][shot]['passer']

# 								if passer_id != "NA":
# 									#append passer to the shot

# 									if passer_id not in returnData[passer_key]:
# 								 		returnData[passer_key][passer_id] = {}

# 								 	passer = returnData[passer_key][passer_id]
# 									# if shot_type == 'FG':
# 									appendPlayer(passer, made, 'Successful Assist', 'Failed Assist')

# 								#plot made shot data
# 								# if made == '1':
# 								# 	#flip flop the coordinates because that is the convention for the plotter
# 								# 	returnData['shot']['plot']['x'].append(shotDict[game][quarter][shot]['shot_y'])
# 								# 	returnData['shot']['plot']['y'].append(shotDict[game][quarter][shot]['shot_x'])


# 			returnData['shot']['GAME_COUNT'] = returnData['shot']['GAME_COUNT']+1
# 			# print returnData['shot']['GAME_COUNT']







