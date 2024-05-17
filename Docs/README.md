# Agile_Group_Project

| UWA ID     | Full Name | Github User Name |
| --------- | --- | ------ |
| 23328091 | Nina Cimesa |  cimi03  |
| 23419054| Sarah Pinelli | sarahp16 |
| 23355626 | Ben Russell | BenRussell24 |
| 22764777 | Blake Griffiths | Blake-22764777 |


## Description

Our application (GeoQuester) is an exciting game where you are able to explore the world around you through challenging quests. The game is motivated by the success of a similar website, GeoGuesser, which utilises Google Maps to present a location to the user to guess. Our application's main purpose is to educate users on different facts pertaining to their city/suburb. The app also advocates for a unique game and exercise experience when played as players must visit the different locations to find quest solutions. Players can find quests suited to them by filtering using duration, difficulty and location. Our application also allows users to create quest submissions which other users can then play. Each quest consists of 5 questions which can be answered by visiting a specific location or using trivia knowledge. Users have three attempts for each question, and points are awarded for accuracy. After completing the quest, the user points are added to their account, ranking them on the leaderboard against other users in their city and suburb. Currently, the application is specified for the city of Perth, Australia, however the implementations allow for global expansion!

## Architecture

Client-side architecture refers to the part of an application or system that runs on the client's device which is responsible for rendering the user interface and handling user interactions.

Server-side architecture refers to the part of an application or system that runs on the server, handling requests from clients, processing data, and generating responses to send back to clients.

Below, details the client-side and server-side architectures present during different stages of the application's running:

### Registering

For registering, the main components involve HTML, CSS, Flask forms, routes and interactions with the database. The HTML and CSS handle the client-side presentation of the registration form, this is the styling and layout of the register page. Once the user inputs their information into the HTML and clicks the submit button (styled with CSS), this is loaded into the server-side Flask form which validates the form data. Once validated the /register route handles the HTTP client request, rendering the registration form, redirecting to another page and finally processes the form submission to send that information to the correct table in the database, the UsersInfo model. The sqlite database stores the user registration information in the UsersInfo model defined in the models.py file. 

### Logging In

For logging in, the main components involve HTML, CSS, Flask forms, routes and interactions with the database. The HTML and CSS handle the client-side presentation of the login form, this is the styling and layout of the login page. Once the user inputs their information into the HTML and clicks the submit button (styled with CSS), this is loaded into the server-side Flask form which validates the form data. Once validated the /login route handles the HTTP client request, rendering the login form, redirecting to another page and finally processes the form submission to send that information to the correct table in the database, the UsersInfo model. The route uses database queries to confirm that the user email and password are correct before redirecting to the user dashboard. If the email or password is incorrect, the user stays on the login page rather than being redirected.

### Create a Quest 

For creating a quest, the main components involve HTML templates, CSS, Flask forms, routes and interactions with the database. The HTML template and CSS handle the client-side presentation of the create a quest form. The HTML template renders the structure of the form where users can input quest details. The CSS styles the quest creation through visual elements. Once the user inputs the quest data into the form and clicks the submit button, this information is sent to the Flask form. The Quest Form is a server-side architecture whch handles the form validation and processing on the server side. When this form validates, the data is sent to the route. The server-side architecture of the /create route is responsible for handling the HTTP requests and sends the data to the corresponding Quests and HintsSolutions models of the sqlite database.

### Filtering for Quests/Leaderboard

For filtering for quests or on the leaderboard, the main components involve HTML templates, CSS, JavaScript and flask routes which interact with the database. The HTML template and CSS handle the client-side presentation of play/leaderboard page. The HTML template renders the structure of the form where users can input quest details. The CSS styles the quest creation through visual elements. The JavaScript code in the HTML acts as a client-side architecture which listens for changes in the filter input and sens an AJAX request to the server to get filtered quest and leaderboard data. In the server-side flask route, the route handles the AJAX request, querying the database based on the inputted filters and returns the filtered data as a JSON response to be displayed to the user. 

### Playing a Quest
For filtering for quests or on the leaderboard, the main components involve HTML templates, CSS and flask routes which interact with the database. The HTML template and CSS handle the client-side presentation of quest page. The HTML template renders the structure of the form where users can input quest details. The CSS styles the quest creation through visual elements. On clicking the check button, the server-side route handles both get and post requests for playing a quest. The check button is a POST request which submits the quest's answer to be processed by the server. In the route, it processes correct and incorrect answers with correct answers getting the next hint and rendering that quest page, whereas if the answer is incorrect, the number of hearts decreases and the page does not progress to the next hint. This is repeated until the quest is completed (i.e., the user has answered all 5 questions), where the points are added to the user's points and the user's id and quest id is pushed to the Completed Quests model in the sqlite database, so that the completed quest will no longer show in that user's available quests table.

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

Once the flask app is opened from the url given by the WSL terminal after running the command "flask run", the user will see the initial homepage with either login or register options. As a first time user, you should click register to create an account filling in all options with correct information and creating a strong password. Once the user's account is registered, the user will need to login in with their selected email and password. Alternatively, you can use the registered Alan Turing account with email: alan.turing@cs.com, and password: genius.

This will direct the user to their user dashboard with a sidebar of the options available to them. Within their dashboard will be their points earned from completing quests, rank in their city, number of quests completed and number of quests created. The sidebar contains the main functionality of the app with three distinct options for the user: Play, Create and Leaderboard. These features are explained below:

###PLAY

Play contains all the available quests for a user to play. This does not include the quests that the user has already completed or the quests that user created. The user is able to use the filters to specify where, how long and how hard their desired quest is to filter through available quests. By clicking the name of the quest, users are redirected to play the quest (which has 5 questions) and only when the current question is answered correctly will the user be able to move onto the next question. There is 3 lives available for each question, which earns different points for the user. 

###CREATE

Create contains a form for users to create their own quest. This quest will be available for other users of the app, but not the user who created it. All boxes must be filled to submit a quest.

###LEADERBOARD

The Leaderboard function allows users to see their ranking of all users registered in the app. This is their ranking based on points earned from completing quests. The leaderboard can be filtered on city and suburb to see the leaderboard of specific cities and suburbs. 

Finally, at all points, the user can return to home which will be their user dashboard. Similarly, the user can also choose to Log Out which will return them to the initial homepage asking the user to login or register. 

Happy questing!
