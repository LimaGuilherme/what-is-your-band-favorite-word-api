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
    

   
   # Built With
* Coveralls - Python interface to coveralls.io API
* coverage - Code coverage measurement for Python
* Flask - The web framework used
* ElasticSearch - 
* MongoDB - 


# Authors
Guilherme Lima - Initial work

# License
This project is licensed under the MIT License - see the LICENSE.md file for details

# Warning
This code uses an  part of the Genius API and Spotifity API. So there is no guarantee 
that it won't stop working tomorrow, if they change how things work. I will however do
my best to make things working again as soon as possible if that happens. So if it 
stops working, let me know!


    