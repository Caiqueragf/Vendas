from enum import unique
from typing import Text
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import form
from sqlalchemy.orm import backref

app = Flask(__name__)

app.config['SECRET_KEY'] = 'afe6de1d4025444d8585cc498a6a10d1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes