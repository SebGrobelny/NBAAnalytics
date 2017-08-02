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
@app.route('/index/player=<player>/season=<season>/month=<month>/quarter=<quarter>', methods=['GET'])
def parsePlayerFull(player,season,month,quarter):
    print("Full")
    print(season)
    #produce a list from the strings passed in 
    if season == "NA":
        seasons = fullseasons
    else:
        seasons = season.split()

    #produce a list from the strings passed in 
    if month == "NA":
        months = fullmonths
    else:
        months = month.split()

    #pass in all quartes since there is no filter
    if quarter == "NA":
        quarters = fullquarters
    else:
        quarters = quarter.split()




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
    app.run(debug=True)