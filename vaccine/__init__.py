from flask import Flask
from .config import DevConfig

# Initializing application
vaccine = Flask(__name__,instance_relative_config = True)

# Setting up configuration
vaccine.config.from_object(DevConfig)
vaccine.config.from_pyfile('config.py')

from vaccine import views