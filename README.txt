This is a scheduler app.

This app requires python3, pip, mongodb, and virtualenv.

Templates are made using jinja2.

How to set up the app to run locally:

- Install mongodb
https://docs.mongodb.com/manual/installation/

If you're running this on a mac and use the brew package manager, you can run 
brew install mongodb

- Install python3 

- create a virtualenv in the root directory, virtualenv -p python3 venv
- source venv/bin/activate
- pip install -r requirements.txt 

Configuring the app

The app is looking for 2 environment variables:
ENV - the environment that the server is running in.  For this demo app, set this to devel
MONGO_URI - the uri of the mongodb that this service will connect to.  For a local mongodb, that uri
is mongodb://localhost:27017

You can also set these two vars by 

source config.sh


To create some sample coaches / customers, you can run the data_helper.py file

python data_helper.py

This will create 2 coaches and 4 users.



To run the app
python scheduler.py

Once the app is running, you can access each of the 4 test customers by placing their ids in the
url, like so:

http://localhost:5000/appt/zeke/
http://localhost:5000/appt/perri/
http://localhost:5000/appt/nora/
http://localhost:5000/appt/buddy/
