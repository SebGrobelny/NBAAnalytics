#sql interfacing 
import sqlite3
import csv





#complete
#0-	1-id	2-season	3-game	4-quarter	5-team	6-opponent	7-home	8-offense_basket	9-passer	
#10-pass_x	11-pass_y	12-pass_distance	13-recorded_assist	14-pass_shot_clock	
#15-pass_game_clock	16-shooter	17-poss_x	18-poss_y	19-poss_shot_clock	
#20-poss_game_clock	21-shot_x	22-shot_y	23-shot_shot_clock	24-shot_game_clock	
#25-dribbles 26-distance_travelled	27-defender	28-ndd	29-made

class csvrd(object):

    def createPlayersTable(self):
    	filename = "players.csv"
        conn = sqlite3.connect('player.db')
        cur = conn.cursor() 
        cur.execute("""CREATE TABLE IF NOT EXISTS player(player_id varchar, playername varchar, position varchar, height int, weight int, byear int, rookie int)""")
        filename.encode('utf-8')
        print "test1"
        with open(filename,'rU') as f:
            reader = csv.reader(f)
            for field in reader:
            	entry = list()
            	entry.append(field[0])
            	entry.append(field[1]+' '+field[2])
            	entry.append(field[3])
            	entry.append(field[4])
            	entry.append(field[5])
            	entry.append(field[6])
            	entry.append(field[7])

                cur.execute("INSERT INTO player VALUES (?,?,?,?,?,?,?);", entry)

        conn.commit()
        conn.close()

    def createPlayerGameTable(self):
    	filename = "complete_data.csv"
        conn = sqlite3.connect('playerGame.db')
        cur = conn.cursor() 
        cur.execute("""CREATE TABLE IF NOT EXISTS playerGame(game int, shooter int, unique(game,shooter) ON CONFLICT REPLACE )""")
        # cur.execute("""CREATE INDEX index_name on playerGame(game, shooter)""")        
        filename.encode('utf-8')
        print "test2"
        with open(filename,'rU') as f:
            reader = csv.reader(f)
            for field in reader:
            	entry = list()
            	entry.append(field[3])
            	entry.append(field[16])


                cur.execute("INSERT INTO playerGame VALUES (?,?);", entry)

        conn.commit()
        conn.close()



c = csvrd().createPlayersTable()
c = csvrd().createPlayerGameTable()
