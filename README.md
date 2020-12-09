<a href="https://codeclimate.com/github/LimaGuilherme/what-is-your-band-favorite-word-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/4927af0fbe2bc1bf9c29/maintainability" /></a> [![Coverage Status](https://coveralls.io/repos/github/LimaGuilherme/what-is-your-band-favorite-word-api/badge.svg?branch=master)](https://coveralls.io/github/LimaGuilherme/what-is-your-band-favorite-word-api?branch=master)  ![Python application](https://github.com/LimaGuilherme/what-is-your-band-favorite-word-api/workflows/Python%20application/badge.svg)

# Set Up Your Account (Spotify)

To use the Web API, start by creating a Spotify user account (Premium or Free). To do that, simply sign up at www.spotify.com.

When you have a user account, go to the Dashboard page at the Spotify Developer website https://developer.spotify.com/dashboard/applications create an APP and get your CLIENT_ID and your CLIENT_SECRET. 

# Set Up Your Account (Genius)

To use Genius API you will need a token. Create a account https://genius.com/signup_or_login

Then acess https://genius.com/api-clients setup your APP infos at "New Api Client". Then go to "ALL Api Clients" and look for "Generate Acess Token".

# Use CLI

Config Credentials - You must provide your credentials only once, you will need your SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, GENIUS_ACCESS_TOKEN (all required)
    
    $ python commands.py config-credentials
    
Top Words - You must provide the name of artist or band (required), and the number of top terms you desire (required)
    
    $ python commands.py get-top-words


Help commands - To see available commands
    
    $ python commands.py --help
    
Help get-top-words - To see command parameters  

    $ python commands.py get-top-words --help

Help conf-credentials - To see command parameters  

    $ python commands.py config-credentials --help
    
# Setting using Docker

    $ cp .env.sample .env #change your variables
    $ cp .env.test.sample .env.test #change your variables
    $ docker-compose up --build -d

# Running

    $ docker-compose up

# Running tests
    $ docker-compose --env-file .env-test up
    $ docker exec -it wiybfw-api bash
    $ python -m unittest

# Use API

# METHOD POST
Use to save all lyrics in your choosen repository:

    $ curl -X POST "http://0.0.0.0:6669/api/artists/Queen/lyrics" 

# METHOD GET
Use to get term frequency lyrics in your choosen repository:

    $ curl -X GET "http://0.0.0.0:6669/api/artists/Queen/lyrics" 


# Authors 
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/LimaGuilherme">
        <img src="https://avatars1.githubusercontent.com/u/13668673?s=460&u=6db061321b83a015314e8ab53b1a0bead7919310&v=4" width="100px;" alt=""/>
        <br />
        <sub>
          <b>Guilerme Lima</b>
          <span> - Lead Development</span>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/antunesleo">
        <img src="https://avatars0.githubusercontent.com/u/13929952?s=400&u=8c46ff05e5295aa7f085f5ec8aeddf5af6bc4677&v=4" width="100px;" alt=""/>
        <br />
        <sub>
          <b>Leonardo Antunes</b>
          <span> - Architecture Adviser </span>
        </sub>
      </a>
    </td>
  </tr>
</table>  

# License
This project is licensed under the MIT License - see the LICENSE.md file for details

# Warning
This code uses an  part of the Genius API and Spotifity API. So there is no guarantee 
that it won't stop working tomorrow, if they change how things work. I will however do
my best to make things working again as soon as possible if that happens. So if it 
stops working, let me know!


    