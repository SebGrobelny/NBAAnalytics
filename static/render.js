

//method for producing lists
function renderPlayerList(players)
{
	var select = document.getElementById("dropdownPlayer");
	console.log("in render");
	console.log(players);
	players = JSON.parse(players);

	console.log(players);

	arrayLength = players.length;

	for(var i=0; i < arrayLength; i++)
	{
		if( i == 0 )
		{
			var opt = document.createElement("option");
			opt.value = "";
			opt.textContent = "Select A Player";
			select.appendChild(opt);


		}
		else
		{
			var opt = document.createElement("option");
			console.log(players[i]);
			opt.value = players[i];
			opt.textContent = players[i];

			select.appendChild(opt);

		}

	}


}

//generic method for producing all of the HTML classses associated with a player
function renderPlayerClass(key, playerData, parentID, suffix)
{
	var newClass = document.createElement('div');
	newClass.setAttribute("id","key");
	newClass.textContent = playerData[key]+suffix;

	document.getElementById(parentID).append(newClass);

}

function getSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
      result.push(opt.value || opt.text);
    }
  }
  return result;
}


//parentID is either FG defender or 3PT defender 
//parentText is either FG Defended By or 3PT Defended By
function renderOtherPlayers(parentID, parentText, shot_type, playerData)
{
	var defend = document.createElement('div');
	defend.setAttribute("id",parentID);
	defend.textContent = parentText
	defend.setAttribute("class","container");


	//create container for all base attributes
	document.getElementById("temp").append(defend)

	var defense = playerData[parentID]
	console.log("starting defense");
	var count = 0
	for (var defender_id in defense)
	{	
		var defender = defense[defender_id]

		console.log(defender);
		for (var defend_key in defender)
		{
			//first intense of class generate variable attributes
			if (count == 0)
			{
				var defendBase = document.createElement('div');
				defendBase.setAttribute("id",shot_type+defend_key);
				defendBase.textContent = defend_key
				document.getElementById(parentID).append(defendBase);

			}
			console.log(defender[defend_key]);

			renderPlayerClass(defend_key, defender, shot_type+defend_key , "")

			

		}
		count = count+1
	}

}

function createBaseShotPlayerAttr(playerData)
{
	console.log("Made it to create player attribute");
	console.log(playerData);

	//var playerName = FirstLast.split(" ")

	var playerData = JSON.parse(playerData);

	//primary container everything gets appended to the point is to dispose of this easily 
	var temp = document.createElement('div');
	temp.setAttribute("id","temp");
	temp.setAttribute("class","container");
	document.getElementById("player").append(temp)

	if ("" in playerData)
	{
		var error = document.createElement('div');
		error.textContent = playerData[""];
		document.getElementById("temp").append(error);
		return 0;

	}



	player = playerData["Player Name"].split(" ")

	// //generate Player picture from API 
	// var playerImage = document.createElement('IMG');
	// playerImage.setAttribute("id", "image")
	// playerImage.setAttribute("src","http://nba-players.herokuapp.com/players/"+player[0]+"/"+player[1]);
	// console.log("http://nba-players.herokuapp.com/players/"+player[1].toLowerCase()+"/"+player[0].toLowerCase()) 

	// document.getElementById("temp").append(playerImage)


	//associate Base Attributes
	var playerBase = document.createElement('div');
	playerBase.setAttribute("id","playerBase");
	playerBase.setAttribute("class","container");


	//create container for all base attributes
	document.getElementById("temp").append(playerBase)

	for (var base_key in playerData)
	{
		if (base_key != "shot" && base_key != "FG defender" && base_key != "FG passer" && base_key != "player_id" && base_key != "3PT defender" && base_key != "3PT passer"  )
		{
			var baseClass = document.createElement('div');
			baseClass.setAttribute("id",base_key);
			baseClass.textContent = base_key
			document.getElementById("playerBase").append(baseClass);

			if (base_key == "weight")
			{
				suffix = " pounds"
			}

			else if (base_key == "height")
			{
				suffix = " inches"
			}

			else
			{
				suffix = ""
			}

			renderPlayerClass(base_key, playerData, base_key, suffix);
		}

	}

	//Offensive Stats stored in 'shot' dictionary 
	for (var shot_key in playerData['shot'])
	{
		if (shot_key == 'Games Played:')
		{
			var shot = playerData['shot'][shot_key];
		 	var shotBase = document.createElement('div');
		 	shotBase.setAttribute("id",shot_key);
		 	shotBase.setAttribute("class","container");
		 	shotBase.textContent = shot_key+" "+playerData['shot'][shot_key]
		 	document.getElementById("temp").append(shotBase);



		}

		//different logic than 3PT or FG
		else{
		var shot = playerData['shot'][shot_key];
		 var shotBase = document.createElement('div');
		 	shotBase.setAttribute("id",shot_key);
		 	shotBase.setAttribute("class","container");
		 	shotBase.textContent = shot_key
		 	document.getElementById("temp").append(shotBase);

		


		//different logic than 3PT or FG


		for (var type in shot)
			{
				console.log(type)
			 	var shotType = document.createElement('div');
			 	shotType.setAttribute("id",shot_key+type);
			 	//shotType.setAttribute("class","");
			 	shotType.textContent = type
			 	document.getElementById(shot_key).append(shotType);
				renderPlayerClass(type, shot, shot_key+type, "")
			}

		}
	}


	//display who the defender was for the specifed key
	renderOtherPlayers('FG defender', "FG Goals Defended By:", "FG", playerData);


	renderOtherPlayers('3PT defender', "3PT Goals Defended By:", "3PT", playerData);



	renderOtherPlayers('FG passer', "FG Goals On Passes From:", "FG", playerData);

	renderOtherPlayers('3PT passer', "3PT Goals On Passes From:", "3PT", playerData);



}


//-----------------------------------------------------------------------------------
//functions called from main.html
//-----------------------------------------------------------------------------------
//method for populating the players tab 
function generateSelect()
{
	var url = 'https://sebnba-pro.herokuapp.com/index';

	console.log(url);

	function reqListener () {
		
		renderPlayerList(this.responseText);

    }



	//put a request into FLASK
	var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("GET", url);
    oReq.send();

}


function processPlayer()
{
	//clear method for previously displayed player
	//if our temp is still there from the last request
	if(document.getElementById("temp"))
		{
			myNode = document.getElementById("temp")
			myNode.remove(myNode.firstChild)
		}
	//primary url for deploying requests for apps.py 
	//url will include an appended request type at the end i.e. base stats 
	var url = 'https://sebnba-pro.herokuapp.com/';

	var season = document.getElementById('dropdownSeason');

	var seasonSelected = getSelectValues(season);
	console.log(seasonSelected);
	if(seasonSelected == "Select a Season")
	{
		seasonSelected="";
	}

	var month = document.getElementById('dropdownMonth');

	var monthSelected = getSelectValues(month);
	console.log(monthSelected);

	if(monthSelected == "Select a Season")
	{
		monthSelected="";
	}

	var quarter = document.getElementById('dropdownQuarter');

	var quarterSelected = getSelectValues(quarter);
	console.log(quarterSelected);
	if(quarterSelected == "Select a Season")
	{
		quarterSelected="";
	}



	//pull the form associated with the player name out of the main.html
	var player = document.getElementById("dropdownPlayer");
	var playerName = getSelectValues(player);
	
	// //pull the form associated with the team name out of the 
	// var teamName = document.getElementById("teamData").value;

	if(playerName != "")
	{
		//set the base player url
		url = url+'index/player='+playerName;
	}

	// if(teamName != "")
	// {
	// 	url = url+'index/team='+teamName;
	// }


	//if the list of season filters is not empty
	if (seasonSelected.length > 0)
	{
		url = url+'/season='+seasonSelected.toString();
	}
	//if the list of month filters is not empty
	if (monthSelected.length > 0)
	{
		url = url+'/month='+monthSelected.toString();
	}
	//if the list of quarter filters is not empty
	if (quarterSelected.length > 0)
	{
		url = url+'/quarter='+quarterSelected.toString();
	}





	console.log(playerName);
	//console.log(season);

	//append it to the url which will be sent back to the flask
	

	console.log(url);

	function reqListener () {

		if(season == ""){
			//render the player with shots from the season 
			createBasePlayerAttr(this.responseText);
			
		}
		else
		{
			createBaseShotPlayerAttr(this.responseText)
			
		}
		

		//call functions that will actually create the playerDiv
		//player_id	firstname	lastname	position	height	weight	byear	rookie

    }


	//put a request into FLASK
	var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("GET", url);
    oReq.send();
}


function main(display)
{
	var main_str = display;
	console.log(main_str);
	var mainDiv = document.getElementById("mainBody");
	mainDiv.textContent = display['firstname'];
	
}