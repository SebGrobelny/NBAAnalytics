# import pyximport; install.pyximport(reload_support=True)
from flask import Flask,  jsonify, make_response, abort, request, render_template
from flask_cors import CORS, cross_origin

#cython
# from pack1.pack1_1.player_proccessor import generatePlayerShots, generatePlayerAssist, get_player_data, processPlayerDictionary

from player_proccessor import generatePlayerShots, get_player_data, processPlayerDictionary


app = Flask(__name__)
CORS(app)


#display the homepage
@app.route('/homepage')
def main():

	return render_template('main.html')

#GET requests
@app.route('/index/player=<player>/', methods=['GET'])
def parsePlayer(player):
    #pass in all seasons since there is no filter
    seasons = ['2014','2015','2016']

    #pass in all months since there is no filter
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']

    #pass in all quartes since there is no filter
    quarters = ['1','2','3','4']

    single_player_season = get_player_data(player, seasons, months, quarters)

    if single_player_season == 404:
        return jsonify({'':"Error Try a Different Player Name"}),404
    single_player_season["Player Name"] = player


    return jsonify(single_player_season)

#no filters loop over everything 
@app.route('/index/player=<player>/season=<season>', methods=['GET'])
def parsePlayerSeason(player,season):
    print("Season")
	
    #produce a list from the strings passed in 
    seasons = season.split()

    #pass in all months since there is no filter
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']

    #pass in all quartes since there is no filter
    quarters = ['1','2','3','4']

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
    quarters = ['1','2','3','4']


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
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']

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
#app doesn't cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#always goes at the bottom of the page
##has to do with the WSGI
if __name__ == '__main__':
    app.run(debug=True)