# import pyximport; install.pyximport(reload_support=True)
from flask import Flask,  jsonify, make_response, abort, request, render_template
from flask_cors import CORS, cross_origin

import json

#module that contains queries to databases
from player_proccessor import generatePlayerShots, get_player_data, processPlayerDictionary, selectPlayersList



app = Flask(__name__)
CORS(app)

#Globals
fullseasons= ['2014','2015','2016']
fullmonths= ['01','02','03','04','05','06','07','08','09','10','11','12']
fullquarters= ['1','2','3','4']


#display the homepage
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/index')
def playerList():
    print "in here"
    player_list = selectPlayersList()
    print "made it out"
    return json.dumps(player_list)

#GET player requests
@app.route('/index/player=<player>/season=<season>', methods=['GET'])
def parsePlayerSeason(player,season):
    #pass in all seasons since there is no filter
    seasons = season.split()

    #pass in all months since there is no filter
    months = fullmonths

    #pass in all quartes since there is no filter
    quarters = fullquarters

    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)


@app.route('/index/player=<player>/month=<month>', methods=['GET'])
def parsePlayerMonth(player,month):
    #pass in all seasons since there is no filter
    seasons = fullseasons

    #pass in all months since there is no filter
    months = month.split()

    #pass in all quartes since there is no filter
    quarters = fullquarters

    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)

@app.route('/index/player=<player>', methods=['GET'])
def parsePlayer(player):
    player = player.replace("-"," ")
    #pass in all seasons since there is no filter
    seasons = fullseasons

    #pass in all months since there is no filter
    months = fullmonths

    #pass in all quartes since there is no filter
    quarters = fullquarters

    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)

#no filters loop over everything 
@app.route('/index/player=<player>/quarter=<quarter>', methods=['GET'])
def parsePlayerQuarter(player,quarter):
    print("Season")
	
    #produce a list from the strings passed in 
    seasons = fullseasons

    #pass in all months since there is no filter
    months = fullmonths

    #pass in all quartes since there is no filter
    quarters = quarter.split()

    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)

@app.route('/index/player=<player>/season=<season>/month=<month>', methods=['GET'])
def parsePlayerSeasonMonth(player,season,month):
    print("SeasonMonth")
    
    #produce a list from the strings passed in 
    seasons = season.split()

    #produce a list from the strings passed in 
    months = month.split()

    #pass in all quartes since there is no filter
    quarters = fullquarters


    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)

@app.route('/index/player=<player>/season=<season>/quarter=<quarter>', methods=['GET'])
def parsePlayerSeasonQuarter(player,season,quarter):
    print("SeasonQuarter")
    
    #produce a list from the strings passed in 
    seasons = season.split()

    #assume all months are fair game since none have been selected 
    months = fullmonths

    #pass in all quartes since there is no filter
    quarters = quarter.split()


    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)

@app.route('/index/player=<player>/month=<month>/quarter=<quarter>', methods=['GET'])
def parsePlayerMonthQuarter(player,month,quarter):
    print("SeasonQuarter")
    
    #produce a list from the strings passed in 
    seasons = fullseasons

    #assume all months are fair game since none have been selected 
    months = month.split()

    #pass in all quartes since there is no filter
    quarters = quarter.split()


    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)

@app.route('/index/player=<player>/season=<season>/month=<month>/quarter=<quarter>', methods=['GET'])
def parsePlayerFull(player,season,month,quarter):
    print("Full")
    print(season)
    #produce a list from the strings passed in 
    seasons = season.split()
    print seasons

    #produce a list from the strings passed in 
    months = month.split( )

    #pass in all quartes since there is no filter
    quarters = quarter.split( )


    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)


#GET team requests
# @app.route('/index/team=<team>/', methods=['GET'])
# def parseTeam(team):

#     single_team = get_team_data(team)

#     single_team["Team Nam: "] = team

#     return jsonify(single_team)






#app doesn't cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#always goes at the bottom of the page
##has to do with the WSGI
if __name__ == '__main__':
    app.run(ssl_context='adhoc')