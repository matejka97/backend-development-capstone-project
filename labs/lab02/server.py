"""
Second task in flask training
"""
# Import the Flask calss from the flask module
from flask import Flask
from data import data
from flask import make_response
from flask import request
# Create an instance ofthe Flask class, passing in the name of the current module

app = Flask(__name__)

@app.route("/")
def home():
    # Function that handles requests to the root URL
    return {'message':"Hello, World!"}

@app.route('/no_content')
def no_content():
    """
    Return of "No content found" with a status of 204

    Returns:
    String: No Content Found
    Status: 204
    """
    return ({'message':'No Content Found'},204)

@app.route("/exp")
def index_explicit():
    """
    Return 'hello world' message with the status code of 200

    Returns:
        String: Hello World!
        Status: 200
    """
    resp = make_response({'message':"Hello, World!"})
    resp.status_code = 200

    return resp

@app.route("/data")
def get_data():
    try:
        # Chek if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404
    
@app.route("/name_search")
def name_search():
    """
    Find a person in the database.


    Returns:
        json: Person if found, with status of 200
        404: If not found
        422: If argument 'q' is missing
    """
    # Get the argument 'q' from the query parameters of the request
    query = request.args.get('q')

    # Check if the query parameter 'q' is missing
    if not query:
        # Return a JSON response with a message indicating 'q' is missing and a 422 Unprocessable
        return {"message": "Query parameter 'q' is missing"}, 422
    # Iterate through the 'data' list to look for the person whose first name matches the query
    for person in data:
        if query.lower() in person['first_name'].lower():
            # If match
            return person
        
    return {'message': "Preson not found"}, 404

@app.route("/count")
def count():
    try:
        # Attempt to return a JSON response with the count of items in 'data'
        # Replace {insert code to find length of data} with len(data) to get the length of data
        return {"data count": len(data)}, 200
    except NameError:
        # If 'data' is not defined and raises a NameError
        return {"message": "data not defined"}, 500

@app.route("/person/<var_name>")
def find_by_uuid(var_name):
    # Iterate through the 'data' list to search for a person with matching ID
    for person in data:
        # Check if the 'id' field of the person matches the 'var_name' parameter
        if person["id"] == str(var_name):
            # Return the person
            return person
        
    return {"message": "Person not found"}, 404

@app.delete("/person/<var_name>")
def delete_person(var_name):
    for person in data:
        if person["id"] == str(var_name):

            # remove data form the list
            data.remove(person)

            return {"message": f"Person with ID: {str(var_name)} deleted"}, 200
        
    return {"message": "Person not found"}, 404

@app.route("/person", methods=['POST'])
def create_person():
    # Get the JSON data form the incoming request
    new_person = request.get_json()

    # Check if the JSON data is empty or None
    if not new_person:

        return {"message": "Invalid input, no data provided"}, 400
    
    # Proceed with further processing of new_person, such as addinf it to a database
    # of validating its contents before saving it

    # Assuming the processing is successful, return a success message with statuce code 201 (created)
    return {"message": "Person created sucessfully"}, 201

@app.errorhandler(404)
def api_not_found(error):
    # This function is a custom error handler for 404 Not Found errors
    # It is triggered whenever a 404 error occurs within the Flask application
    return {"message": "API not found"}, 404