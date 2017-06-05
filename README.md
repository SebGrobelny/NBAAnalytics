Link to Project:
	The Kings Interview Project is available for view at https://sebnba-pro.herokuapp.com/homepage
Design:
	Given the large amount of features present in complete_data.csv it was important for me to associate them with players in an efficient way so as to process requests for shot data associated with a player as fast as possible. I developed a schema wherein the actual player name would act as a primary key for one dictionary and then using the player_id found in that dictionary they could then recreate the shot data from the desired game using a larger dictionary of all shots. 

	I went about this by building out a series of nested dictionaries at every layer while reading in data corresponding to a player the user would query from complete_csv. Doing this takes advantage of a dictionary's lookup time of O(1) when provided with the appropriate key, which would come from the user in the form of what filters they provide before hitting the generate stats button. One can then simply use the key provided by the user to narrow down exactly what player, what season(s), what month(s) and what quarters they would like to generate shot data for from complete_data.csv.  The obvious delay comes from traversing through complete_csv that is why my nested dictionary of player data is done in place as it is passed into the function that reads in complete_csv and updates whenever the corresponding player ID is encountered in the shot. This design can easily be transfered to passer or defender data as both rely on the same player ID.

	The user can pass in filters depending on what options they check on 

	Visual Schema:
	player_id-->season-->game-->quarter-->shot

	If given more time, I would integrate teams in a similiar fashion and use the same approach for filters.

	Planned Integration of Teams:
	team_id->player_id->...

Alternative Approaches:
	
	I had considered building out a database in sqlite3 and then simply dumping the data into a database and running queries that way. This does not fix the query time as you are still traversing through every possible shot in every possible game. If a database implementation is desired  then I believe mulitple are necessary so as to associate different keys with different values to minimize look up time. Overall I believe the in place, nested dictionary approach I undertook requires less space and time than maintaining a full database and takes advantage of the fact that the framework I chose, FLASK, does not need an underlying database.

Alternative Deployment:
	With my local version I was able to run every query on every filter without timing out. Given that Heroku times out when requests take 30 seconds to process which queries relating to a player's entire season , which led me to pursue the use of cython so as to attempt to improve the data processing by utilizing C, this can still be seen if looking inside my pack1 directory on git as I have a setup.py file used to compile the cython file.  This unfortunately did not work on Heroku, although it did work locally and actually sped up a lot of the vaster queries, as Heroku was not able to recognize the pyx modules that cython produces. So I would definitely invest in some other host that does not fall under that restriction. 

	I found Flask to be perfect for this project as there was no underlying database I was interacting with. Had there been I probably would have prefered to use Node.JS as I would prefer to have the server side code to be the same language as the one used to generate the responsive layouts. 

	I made a very strong effort to make every Javascript 

Stats Produced:
	Every shot was taken and characterized by its distance to the basket this in turn would produce either an FG for Field Goal or 3PT for 3 pointer. The stat I introduced is the clutch field goal or three pointer and this is basically when a shot is fired off with 10 or less seconds left off on the shot clock potentially useful in determining a player's utility in close situations. I then went on to generate stats for players who guarded and assisted so as to maybe guage player compatability or lackthereof. 

Web Development Projects:
	One of my first Web Development Projects was interacting with an API using Django as a framework, this app is available at https://pokemon-go-search.herokuapp.com/ and as this was my first project using HTML, CSS in correspondence with Python a lot of the initial struggle came from how to generate information from Python for instance and render it back to the HTML while still styling it with the CSS. Though basic, this project taught me a lot of the fundamentals of Full Stack Web Development. 

	A slightly more intricate project found at https://sebweatherapp.herokuapp.com/ had me deal with the Yahoo Weather API. The reason this project stands out for me was that it was the first time I had used javascript to develop a responsive layout as I implemented buttons that would allow the forecast to shift to the next day as the browser view would display five boxes out of 10 total, while using Flask for the first time to actually host the app. 

	One of my most complicated web projects to date can be found at https://sebphoto.herokuapp.com/ and this app allows a user to upload a photo of their chosing from their local directories and upon upload makes a call to Google Cloud Platform API to generate tags for the images. The reason this project was the most complex is because it featured the use of Node.JS, requiring me to utilize javascript for the server side applications dealing with a SQLite3 database of pictures while also dealing with API calls. The approach was sytematic as I started out doing very basic request calls between the server and non server javascript and queried a dictionary whose values I know by heart. From there I expanded and began to dynamically update the 


Software Development Experience:
	My initial back-end experience stems from my internship with GoodData. There I worked alongside their Professional Services team as they tackled on a wide variety of database implementations with clients such as HortonWorks, AccessData, and LogMeIn.There I had the opportunity to participate in part of the implementation starting with the collection of requirements from clients, then going on to produce the data models, using ETL to make the necessary transformations to the data, producing tables in SQL based on how the data was to be accessed, and design of the actual dashboard using a SQL-esque language to produce queries that fueled the dynamic reporting and configuring GoodData's built in JSON features for the front end design. While there I also participated in a performance test project under the guidance of a Solutions Architect, as we tested different database configurations would optimize load times given different distributions of features and attributes. If you would like further information about this internship, please feel free to contact the Project Manager I worked closely with Nikka Mathur at niharika.mathur@gooddata.com.

	I then began interning with Niche Holdings based out of San Francisco. There I implement XML and HTML parsers using BeautifulSoup that automate data collections across a variety of different sites looking for financial information about companies publicly trading on the stock market. I have also gained proficiency at OpenSSL technology for client server interaction. Please feel free to reach out to Justin Howe at justinxhowe@gmail.com for any questions about the nature of the project.

	As of now I currently tutor UC Davis's operating systems class. The class itself is driven towards projects in C that build off of the development of a user level thread library as the projects expanded into thread storage and the implementation of a virtual file system. As a tutor I help guide students in a broader understanding of the concepts while also helping them debug and design the projects in C. As a non-native English speaker, I pride myself on being able to take the very technical terms and utilize visual aids along with simple examples so as to guide my students toward a greater understanding of the material. Please feel free to reach out to my supervisor Inez Anders at cianders@ucdavis.edu.

	For me Software Development was something I first picked up my Sophomore year in college when taking my first object-oriented programming class in C and honed as a tutor for a class with deeper applications. But the programming skills I have acquired at UC Davis and in my internship experience come second to the lifelong communication skills and teambuilding skills that I have developed throughout my education at UC Davis and while participating in the Young Entrepreneurs at Haas program. I feel as if that is my strongest asset as a Software Engineer and something that I would very much like to showcase in future interviews, and if I'm lucky enough, as a Back End Developer for the Sacramento Kings.
	
