from app import application as app
import admin
from app import db
import models
import views

from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')

if __name__ == "__main__":
    app.run()
