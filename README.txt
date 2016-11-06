This is a scheduler app.

This app requires python3, mongodb, and virtualenv.

To setup a test environment:
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt 

To run the app
python scheduler.py

The app will attempt to connect to a local mongodb instance.
