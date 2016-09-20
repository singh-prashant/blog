from app import application as app

@app.route('/')
def homepage():
    return 'Home Page of the app.'

