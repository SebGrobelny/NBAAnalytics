#sql interfacing 
import sqlite3
import csv

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


c = csvrd().createPlayersTable()
