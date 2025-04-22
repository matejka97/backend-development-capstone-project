"""
First task in flask training
"""
# Import the Flask calss from the flask module
from flask import Flask

# Create an instance ofthe Flask class, passing in the name of the current module
app = Flask(__name__)

@app.route("/")
def home():
    # Function that handles requests to the root URL
    return {'message':"Hello, World!"}