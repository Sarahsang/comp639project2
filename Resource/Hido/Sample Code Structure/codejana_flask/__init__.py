from flask import Flask

app=Flask(__name__)

from codejana_flask import routes
from codejana_flask import admin_view
from codejana_flask import view