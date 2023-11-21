from flask import Flask

app=Flask(__name__)

from project2 import routes
from project2 import manager
from project2 import orgchart
from project2 import queries
from project2 import connect_proj2

