# Agile_Group_Project

| UWA ID     | Full Name | Github User Name |
| --------- | --- | ------ |
| 23328091 | Nina Cimesa |  cimi03  |
| 23419054| Sarah Pinelli | sarahp16 |
| 23355626 | Ben Russell | BenRussell24 |
| 22764777 | Blake Griffiths | Blake-22764777 |


## Description

Our application (GeoQuester) is an exciting game where you are able to explore the world around you through challenging quests. The game is motivated by the success of a similar website, GeoGuesser, which utilises Google Maps to present a location to the user to guess. Our application's main purpose is to educate users on different trivia for their city/suburb as well as advocate for a unique game and exercise experience when played via visiting the different locations to find the hint solutions.  By allowing to create quest submissions that may be selected for the daily quest, this adds an interactive feature to the application as their quest may be picked and played as the daily quest for all users. The daily quest consists of 5 hints which can be answered by visiting a specific location or using trivial knowledge to answer the hints. After completing the quest, the user accumulates points towards their account that ranks them in the leaderboard section of our application against other users in their city. 

## Installation

For launching our application, the following instructions provide a comprehensive guide to installing the application on the users computer. Once the application is set up and functional, there are further instructions on how to create an account and use the application. 

### Step 1: Download All Files onto the Local Computer into a Folder

From Github install all game files into a folder on the local computer before opening a WSL terminal of the folder. 

In the WSL terminal ensure your WSL is up to date by running the following commands:

"sudo apt-get update"

"sudo apt-get upgrade"

### Step 2: Create a Virtual Environment 

In the WSL terminal for the folder path, run the following command to create a virtual environment:

"python -m venv venv"

### Step 3: Activate the Virtual Environment

After creating the virtual environment, activate the virtual environment by running the following command:

(Windows) "venv\Scripts\activate"

(Linux/MacOS) "source venv/bin/activate"

### Step 4: Install Dependencies

Once the virtual environment is activated, install all necessary libraries using "pip install <library_name>". The specific codes are outlined below:

"pip install flask"

"pip install flask-migrate"

"pip install flask-sqlalchemy"

"pip install flask-login"

"pip install flask-wtf"

### Step 5: Set Up Flask App Environment Variable 

To create a flask environment variable for the app, run the following command in the WSL terminal:

"export FLASK_APP = microblog.py"

### Step 6: Run Flask App

To launch the flask application, run the following command in the WSL terminal. This will launch the application on a local browser for the user to play the game.

"flask run"

## Usage

<insert instructions on how to use project including examples>

## Contributions


## Acknowledgements

<insert general description of each members role / responsibilities>



