import math 



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


	#x and y coordinates after applying our logic
	#print shot_x
	#print shot_y

	#use pythagorean theorem to calculate distance to the basket
	hypotenuse = pow(shot_x[0],2)+ pow(shot_y[0],2)
	distance_to_basket = math.sqrt(hypotenuse)


	#print distance_to_basket

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
		# 	print "Possible FT"

		return "FG"

#increment either FG or 3PT
def incrementShotData(made, shotData):
	#initialize if not already present
	if 'MADE' not in shotData:
		shotData['MADE'] = 0
	if 'ATTEMPT' not in shotData:
		shotData['ATTEMPT'] = 0



	if made == '1':
						
		shotData['MADE'] = shotData['MADE'] + 1
		shotData['ATTEMPT'] = shotData['ATTEMPT'] + 1

	if made == '0':
		shotData['ATTEMPT'] = shotData['ATTEMPT'] + 1


def calculatePercentages(threePTData, fgData, returnData):

	#ensure that values exist before trying to calculate 
	if 'MADE' in fgData and 'ATTEMPT' in fgData:
		fgData['FG%'] = "{:.3f}".format(float(fgData['MADE']) / float(fgData['ATTEMPT']))
		fgData['AVG_FG_ATTEMPT'] = "{:.1f}".format(float(fgData['ATTEMPT']) / float(returnData['GAME_COUNT']))
		fgData['AVG_FG_MADE'] = "{:.1f}".format(float(fgData['MADE']) / float(returnData['GAME_COUNT']))

	if 'MADE' in threePTData and 'ATTEMPT' in threePTData:
		threePTData['3PT%'] = "{:.3f}".format(float(threePTData['MADE']) / float(threePTData['ATTEMPT']))	
		threePTData['AVG_3PT_ATTEMPT'] = "{:.1f}".format(float(threePTData['ATTEMPT']) / float(returnData['GAME_COUNT']))
		threePTData['AVG_3PT_MADE'] = "{:.1f}".format(float(threePTData['MADE']) / float(returnData['GAME_COUNT']))


#used to identify either the defender or passer associated with a shot
def identifyPlayer(playerBaseDict, playerIdDict, name):
	print "in ID player"
	for player_id in playerBaseDict:
		print player_id

		if player_id in playerIdDict:
			print playerIdDict[player_id]['firstname']
			print playerIdDict[player_id]['lastname']

			#store the player name in with the id 
			playerBaseDict[player_id][name] = playerIdDict[player_id]['firstname']+" "+playerIdDict[player_id]['lastname']

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






def calculateShot(shotDict, months, quarters, threePTData, fgData, returnData):
	#len(shotDict['game']) gives us the number of games
	#we want to find the number made each game and divide it by the total number of games
	print "in CalculateAverage"

	#iterate through all of the games player had in given season
	for month in months:
		print month 
		for game in shotDict:
			#iterate through quarter player had in given game
			#verify that the player had a game in the month requested
			if int(game[4:6]) == int(month):
				# if game == '2015012709':
					print "in game"
					for quarter in quarters:
						#verify that player actually has data for the given quarter
						if quarter in shotDict[game][quarter]:
							for shot in shotDict[game][quarter]:
								print shotDict[game][quarter][shot]

								#made-1 or missed-0 shot 
								made = shotDict[game][quarter][shot]['made']

								#FG or 3PT?
								shot_type = shotDict[game][quarter][shot]['shot_type']


								#call helper with fgData
								if shot_type == 'FG':
									incrementShotData(made, fgData)

								
								#call helper with 3ptData
								if shot_type == '3PT':
									incrementShotData(made, threePTData)



								#defender data 
								if shot_type == 'FG':
									defender_key = 'FG defender'
								if shot_type == '3PT':
									defender_key = '3PT defender'
									
								defender_id = shotDict[game][quarter][shot]['defender']

								#TODO factor in defender distance to the player
								if defender_id != "NA":
								 	#append defensive player to the shot
								 	if defender_id not in returnData[defender_key]:
								 		returnData[defender_key][defender_id] = {}

								 	defender = returnData[defender_key][defender_id]

								 	# if shot_type == 'FG':
								 	appendPlayer(defender, made, 'Defended Shot', 'Allowed Shot')

								 	# if shot_type == '3PT':
								 	# 	appendPlayer(defender, made, 'Defended 3PT', 'Allowed 3PT')

								#passer data 
								if shot_type == 'FG':
									passer_key = 'FG passer'
								if shot_type == '3PT':
									passer_key = '3PT passer'

								passer_id = shotDict[game][quarter][shot]['passer']

								if passer_id != "NA":
									#append passer to the shot

									if passer_id not in returnData[passer_key]:
								 		returnData[passer_key][passer_id] = {}

								 	passer = returnData[passer_key][passer_id]
									# if shot_type == 'FG':
									appendPlayer(passer, made, 'Successful Assist', 'Failed Assist')

								#plot made shot data
								if made == '1':
									#flip flop the coordinates because that is the convention for the plotter
									returnData['shot']['plot']['x'].append(shotDict[game][quarter][shot]['shot_y'])
									returnData['shot']['plot']['y'].append(shotDict[game][quarter][shot]['shot_x'])


						returnData['shot']['GAME_COUNT'] = returnData['shot']['GAME_COUNT']+1
						print returnData['shot']['GAME_COUNT']







