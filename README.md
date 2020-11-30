# Set Up Your Account (Spotify)

To use the Web API, start by creating a Spotify user account (Premium or Free). To do that, simply sign up at www.spotify.com.

When you have a user account, go to the Dashboard page at the Spotify Developer website and, if necessary, log in. Accept the latest Developer Terms of Service to complete your account set up.

# Set Up Your Account (Genius)

To use Genius API you will need a token. Create a account https://genius.com/signup_or_login

Then setup your infos at "New Api Client" and get your "ACCESS TOKEN"

# Setting using Docker

    $ cp .env.sample .env #change your fvariables
    $ docker-compose up --build -d

# Running

    $ docker-compose up

# Running tests
    $ docker exec -it wiybfw-api bash
    $ python -m unittest
 
 # Installing Local
 
    Requirements
    
     Linux
     Python 3.9
     Elasticsearch 7+
     MongoDB
     
    $ cp .env.sample .env
    $ python3.8 -m venv wiybfw-api
    $ source wiybfw-api/bin/activate
    $ pip install -r requirements.txt
    $ export $(cat .env | xargs)
    $ flask run
    



# Authors
Guilherme Lima - Initial work

# License
This project is licensed under the MIT License - see the LICENSE.md file for details

# Warning
This code uses an  part of the Genius API and Spotifity API. So there is no guarantee 
that it won't stop working tomorrow, if they change how things work. I will however do
my best to make things working again as soon as possible if that happens. So if it 
stops working, let me know!


    