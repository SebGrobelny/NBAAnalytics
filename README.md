# Link to Project:
######	The NBA Shot Analysis Project is available for view at https://sebnba-pro.herokuapp.com/homepage.

## How to Work the Site:
######	Simply type a player's name and select however many filters you would like to take into consideration before hitting the generate stats. Requests on average take 20 seconds so please be patient and preferably run the site on chrome as safari seems to take longer! :)

## Details on the Files submitted:
### app.py:
##### Primary interface for obtaining requests from the user. Since user does not post anything all methods are GET and interact with the player_proccessor.py. Returns dictionary based data to render.js.
### player_proccessor.py:
### use:
#### app.py passes along the filters the user supplied along for actual data processing in this module
###    main methods:
#####   processPlayerDictionary:
###### Opens players.csv and produces three dictionaries with this data playerNameDict which associates a player name with all of their base attributes, notably their player ID and playerIdDict which associates a player id with their name. Doing this made look ups when given either name or id efficient. The final dictionary associates an empty dictionary with every player ID, this dictionary is the populated by data from complete_data.csv, in my current implemenation with shot type but the purpose in doing this was to later link assist data, and defense data with a given player. 

##### get_player_data:
###### Main method for processing player data which gets the filters user specified (season,game,quarter and player name) and calls processPlayerDictionary to obtain playerNameDict and playeIdDict. After checking if the name given by the user is in the playerNameDict, the method uses the id given  After finding the corresponding id in playerNameDict given a name supplied by the user, generatePlayeShots is called with all the filters provided by the user  along with playerCompDict which gets populated by the function. Once generatePlayerShots runs to completion the functions increment_shot_data and identify  are called 
##### generatePlayerShots:	
###### The method takes in playerCompDict as a parameter and opens the complete_data.csv for reading. The method populates the dictionary when encoutering a shooter_id that matches the player_id corresponding to the player the user requested. The series of nested dictionaries effectively associates a player_id with  shot data they had in a given game (i.e. type, defender, passer) using appendPlayer to either append defenders or passers on the given shot. 


### stat_calculation.py:
### use:
###### This module stores the methods behind a lot of the calculations present in player_proccessor.py
### methods:
####			check_shot_type :
###### This method is called from generatePlayerShots and uses the shot_x and shot_y coordinates from complete_csv to determine whether or not the shot was a field goal or 3 pointer based on the calculated distance to the basket. The reason these are passed in as list elements was because I had initally wanted to produce a plot in matlab that would show where on the court the shot took place, unfortunately I did not have sufficient time to figure out how to pass a matlab plot into an html template for rendering. 

#### increment_shot_data
###### Based on the shot type passed in which could either be FG 3PT or their clutch counterparts the 'ATTEMPT' and 'MADE' attributes are updated accordingly as determined by whether or not the shot was made
#### identifyPlayer
##### Used to identify the passers or defenders that have been associated with a given shot based on the id stored from complete_data.csv

### Static Files and Templates:
##### render.js:
######		Primary method utilized for generating the divs associated with the dictionaries acquired based on player data and passing queries into app.py 
##### main.css:
######		Utilized flexbox to generate a structured layout for whatever dictionary data is passed and rendered into render.js 
##### main.html
######		Template user is faced with throughout interaction with site features form where user can enter player name along with option types for filter data for season, quarter and month desired.

### other files included in submission:

#### 	flask:
###### Directory created with flask installation. 

####	pack1:
###### This directory along with all of its subdirectories and files was used in trying to make player_proccessor a cython module that would be imported. The reason for this was to speed up the nested loops going on when reading and storing data in the dictionary as cython compiles as a C file.
## Design:
###### Given the large amount of features present in complete_data.csv it was important for me to associate them with players in an efficient way so as to process requests for shot data associated with a player as fast as possible. I developed a schema wherein the actual player name would act as a primary key for one dictionary and then using the player_id found in that dictionary they could then recreate the shot data from the desired game using a larger dictionary of all shots. I went about this by building out a series of nested dictionaries at every layer while reading in data corresponding to a player the user would query from complete_csv. Doing this takes advantage of a dictionary's lookup time of O(1) when provided with the appropriate key, which would come from the user in the form of what filters they provide before hitting the generate stats button. One can then simply use the key provided by the user to narrow down exactly what player, what season(s), what month(s) and what quarters they would like to generate shot data for from complete_data.csv.  The obvious delay comes from traversing through complete_csv that is why my nested dictionary of player data is done in place as it is passed into the function that reads in complete_csv and updates whenever the corresponding player ID is encountered in the shot. This design can easily be transfered to passer or defender data as both rely on the same player ID.
###	Visual Schema:
######	player_id-->season-->game-->quarter-->shot-->shotdata
###	Visualization of Dictionary:
	{player_id : 
		{season : 
			{game : 
				{quarter: 
					{shot: 


					}
				}
			}
		}
	}

###### If given more time, I would integrate teams in a similiar fashion by using a function similiar to generatePlayerShots to obtain data on a given team given its id.

### Planned Integration of Teams:
#### team_id->player_id->...

## Alternative Approaches:
	
###### I had considered building out a database in sqlite3 and then simply dumping the data into a database and running queries that way. This does not fix the query time as you are still traversing through every possible shot in every possible game. If a database implementation is desired  then I believe mulitple are necessary so as to associate different keys with different values to minimize look up time. Overall I believe the in place, nested dictionary approach I undertook requires less space and time than maintaining a full database and takes advantage of the fact that the framework I chose, FLASK, does not need an underlying database.

## Alternative Deployment:
###### With my local version I was able to run every query on every filter without timing out. Given that Heroku times out when requests take 30 seconds to process which queries relating to a player's entire season , which led me to pursue the use of cython so as to attempt to improve the data processing by utilizing C, this can still be seen if looking inside my pack1 directory on git as I have a setup.py file used to compile the cython file.  This unfortunately did not work on Heroku, although it did work locally and actually sped up a lot of the vaster queries, as Heroku was not able to recognize the pyx modules that cython produces. So I would definitely invest in some other host that does not fall under that restriction. 
###### I found Flask to be perfect for this project as there was no underlying database I was interacting with. Had there been I probably would have prefered to use Node.JS as I would prefer to have the server side code to be the same language as the one used to generate the responsive layouts. 

###### I made a very strong effort to make every Javascript and even Python functions for processing data as generic as possible to open the window for the rendering of future dictionaries such as the planned one I had for teams. 

## Stats Produced:
###### Every shot was taken and characterized by its distance to the basket this in turn would produce either an FG for Field Goal or 3PT for 3 pointer. The stat I introduced is the clutch field goal or three pointer and this is basically when a shot is fired off with 10 or less seconds left off on the shot clock potentially useful in determining a player's utility in close situations. I then went on to generate stats for players who guarded and assisted so as to maybe guage player compatability or lackthereof. 
## Take Aways:
### Dedicate Time to Error Checking Right Away:
###### One thing I was not careful about enough in my implementation was returning error messages back to the user. I do have one when someone for instance enters an invalid player name but error handling should have been apart of the process from the start and I will be sure to place an emphasis on that in future projects I undertake.

### Don't Save Deployment For Last:
###### All of my work up until the last 12 hours before submission had been done locally. When I deployed I realized that my requests would actually time out on heroku forcing me to dedicate more time to optimized my implementation's query performance rather than integrating the team data. Had I deployed the most basic instance of the app I would have caught this flaw sooner and would have been able to dedicate time towards optimization sooner allowing for the last few hours to be spent integrating team data and ironing out the design. Even in the end my local version has queries that work when only player is searched but due to an HTTP vs HTTPS request error thrown by heroku the app is limited in that the user must enter a player name and select filters in order to display data.

# Personal
## Web Development Projects:
###### One of my first Web Development Projects was interacting with an API using Django as a framework, this app is available at https://pokemon-go-search.herokuapp.com/ with source code available on https://github.com/SebGrobelny/PokemonGoSearchEngine and as this was my first project using HTML, CSS in correspondence with Python a lot of the initial struggle came from how to generate information from Python for instance and render it back to the HTML while still styling it with the CSS. What got me through a lot of this struggle was the utilization of Google Chrome's Developer Tools to track the changes made and where, in this case, the form data was getting processed. Learning how to utilize the Developer Tools in Chrome to track changes in my project, I was able to gain a fuller understanding of what Python returns to HTML and how the HTML processes the data. Though basic, this project taught me a lot of the fundamentals of Full Stack Web Development. 

###### A slightly more intricate project found at https://sebweatherapp.herokuapp.com/ and source code on https://github.com/SebGrobelny/YahooWeatherApp, had me deal with the Yahoo Weather API. The reason this project stands out for me was that it was the first time I had used javascript to develop a responsive layout as I implemented buttons that would allow the forecast to shift to the next day as the browser view would display five boxes out of 10 total, while using Flask for the first time to actually host the app. Using the Developer Tools again I was able to understand how the Javascript interacts with the HTML and how the Python interacts with the Javascript data. As this was the first time I had interacated with an API in Javascript, I learned how API responses are returned as JSON objects or dictionaries, which was pivotal in my design of the player dictionary in my submitted project for the Kings.

###### One of my most complicated web projects to date can be found at https://github.com/SebGrobelny/PhotoBooth. Though not yet deployed, this app allows a user to upload a photo of their chosing from their local directories and upon upload makes a call to Google Cloud Platform API to generate tags for the images. The reason this project was the most complex is because it featured the use of Node.JS, requiring me to utilize javascript for the server side applications dealing with a SQLite3 database of pictures while also dealing with API calls. The approach was sytematic as I started out doing very basic request calls between the server and non server javascript and queried a dictionary whose values I know by heart. From there I expanded and began to dynamically update the actual database with photos and the labels that correspond to them. Working off of one photo, I worked on dumping the database on page reloads which would effectively prevent the photo from dissapearing off a page during a reload. Currently working on filtering the favorites category and adding an option to filter by labels. 


## Software Development Experience:
###### My initial back-end experience stems from my internship with GoodData. There I worked alongside their Professional Services team as they tackled on a wide variety of database implementations with clients such as HortonWorks, AccessData, and LogMeIn.There I had the opportunity to participate in part of the implementation starting with the collection of requirements from clients, then going on to produce the data models, using ETL to make the necessary transformations to the data, producing tables in SQL based on how the data was to be accessed, and design of the actual dashboard using a SQL-esque language to produce queries that fueled the dynamic reporting and configuring GoodData's built in JSON features for the front end design. While there I also participated in a performance test project under the guidance of a Solutions Architect, as we tested different database configurations would optimize load times given different distributions of features and attributes. If you would like further information about this internship, please feel free to contact the Project Manager I worked closely with Nikka Mathur at nikkamathur@gmail.com.

###### I then began interning with Niche Holdings based out of San Francisco. There I implement XML and HTML parsers using BeautifulSoup that automate data collections across a variety of different sites including Google and the SEC, looking for financial information about companies publicly trading on the stock market. I have also gained proficiency at OpenSSL technology for client server interaction. Please feel free to reach out to Justin Howe at justinxhowe@gmail.com for any questions about the nature of the project, as I did sign a Non Disclosure Agreement and am limited in discussing how this data is going to be used.

###### As of now I currently tutor UC Davis's operating systems class. The class itself is driven towards projects in C that build off of the development of a user level thread library. The projects delve into thread storage and the implementation of a virtual file system. As a tutor I help guide students in a broader understanding of the concepts and technologies necessary to succeed in the class such as GDB and Git. In this job I also help debug and design the projects in C. As a non-native English speaker, I pride myself on being able to take the very technical terms and utilize visual aids along with simple examples so as to guide my students toward a greater understanding of the material. Please feel free to reach out to my supervisor Inez Anders at cianders@ucdavis.edu.

###### For me Software Development was something I first picked up my Sophomore year in college when taking my first object-oriented programming class in C and honed over the next 2 years as I am now a tutor for a class with deeper applications in C. But the programming skills I have acquired at UC Davis and in my internship experience come second to the lifelong communication skills and teambuilding skills that I have developed throughout my education at UC Davis and while participating in the Young Entrepreneurs at Haas program. I feel as if that is truly my strongest asset as a Software Engineer and something that I would very much like to showcase in future interviews, and if I'm lucky enough, as a Back End Developer for the Sacramento Kings.
	
