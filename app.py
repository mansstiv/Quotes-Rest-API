# from tokenize import String
# from urllib import response
from flask import Flask, Response, request
from bson.objectid import ObjectId
import pymongo
import json

####################################################################################################################################

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="docker_mongodb",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.quotes
    mongo.server_info() # trigger exception if cannot establish connection to db
except:
    print("\nCannot connect to db..\n")

####################################################################################################################################

@app.route("/quotes", methods=["POST"])
def create_quote():
    """
    Function to create a quote
        1. check if request's body is empty
        2. check if keys provided have valid name
        3. make sure they are strings
        4. make sure mandatory field 'text' is given
        5. if previous checks were successful create new quote
    """
    try:
        quote = None

        if request.data:
            quote = request.get_json()

        # check if body is empty
        if quote == None or quote == {}:
            return Response(response=json.dumps({"Error": "Empty body in request"}),
                            status=400,
                            mimetype='application/json')

        fieldTextExists = 0
        for key in quote:
            # check if key is valid
            if key not in ["author", "text"]:
                return Response(response=json.dumps({"Error": f"Invalid key name: {key}"}),
                                status=400,
                                mimetype='application/json')
            elif key == "author":
                if isinstance(quote["author"], str) == False:
                    return Response(response=json.dumps({"Error": "Fields must be in string format"}),
                                    status=400,
                                    mimetype='application/json')
            else: # key is text
                if isinstance(quote["text"], str) == False:
                    return Response(response=json.dumps({"Error": "Fields must be in string format"}),
                                    status=400,
                                    mimetype='application/json')
                fieldTextExists = 1
        
        if fieldTextExists == False:
            return Response(response=json.dumps({"Error": "Field 'text' is mandatory"}),
                            status=400,
                            mimetype='application/json')

        resp = db.quotes.insert_one(quote)

        return Response(response=json.dumps({'Status': 'Successfully inserted', 'Quote_ID': str(resp.inserted_id)}),
                        status=200,
                        mimetype='application/json')

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Error": "Cannot create quote"}),
                        status=500,
                        mimetype='application/json')   

####################################################################################################################################

@app.route("/quotes/<id>", methods=["PUT"])
def update_quote(id):
    """
    Function to update a quote
        1. check if request's body is empty
        2. check if quote_id is valid and exists in db
        3. checks for the updating fields
            3.1. check if potential keys provided have valid name
            3.2. make sure they are strings
        4. if previous checks were successful update quote
    """
    try:
        quote = None

        if request.data:
            quote = request.get_json()

        # check if body is empty
        if quote == None or quote == {}:
            return Response(response=json.dumps({"Error": "Empty body in request"}),
                            status=400,
                            mimetype='application/json')

        # check if id is valid 
        if ObjectId.is_valid(id) == False:
            return Response(response=json.dumps({"Error": "Id is invalid"}),
                            status=400,
                            mimetype='application/json')

        # check if id exists in db
        if len(list(db.quotes.find({"_id":ObjectId(id)}))) == 0:
            return Response(response=json.dumps({"Error": "Id does not exist"}),
                            status=400,
                            mimetype='application/json')


        for key in quote:
            # check if key is valid
            if key not in ["author", "text"]:
                return Response(response=json.dumps({"Error": f"Invalid key name: {key}"}),
                                status=400,
                                mimetype='application/json')
            # check if type is string
            elif isinstance(quote[key], str) == False:
                return Response(response=json.dumps({"Error": "Fields must be in string format"}),
                                status=400,
                                mimetype='application/json')

        resp = db.quotes.update_one({"_id":ObjectId(id)},
            {"$set":quote}
        )

        if resp.modified_count > 0:
            return Response(response=json.dumps({"Message": "Quote updated", "Quote_ID":f"{id}"}),
                            status=200,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps({"Message": "Nothing to update", "Quote_ID":f"{id}"}),
                            status=200,
                            mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Error": "Cannot update quote"}),
                        status=500,
                        mimetype='application/json')

####################################################################################################################################

@app.route("/quotes/<id>", methods=["DELETE"])
def delete_quote(id):
    """
    Function to delete a quote
        1. check if quote_id is valid exists in db
        2. delete quote
    """
    try:
        # check if id is valid and exists in db
        if ObjectId.is_valid(id)==False:
            return Response(response=json.dumps({"Error": "Id is invalid"}),
                            status=400,
                            mimetype='application/json')
                            
        # check if id exists in db
        if len(list(db.quotes.find({"_id":ObjectId(id)}))) == 0:
            return Response(response=json.dumps({"Error": "Id does not exist"}),
                            status=400,
                            mimetype='application/json')

        
        resp = db.quotes.delete_one({"_id":ObjectId(id)})

        return Response(response=json.dumps({"Message": "Quote deleted", "Quote_ID":f"{id}"}),
                        status=200,
                        mimetype='application/json')

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Error": "Cannot delete quote"}),
                        status=500,
                        mimetype='application/json')

####################################################################################################################################

@app.route("/quotes", methods=["GET"])
def get_quotes():
    """
    Function to return all quotes
    """
    try:
        quotes = list(db.quotes.find())

        # check if collection is empty
        if len(quotes) == 0:
            return Response(response=json.dumps({"Message": "No documents in collection"}),
                            status=200,
                            mimetype='application/json')

        for quote in quotes:
            quote["_id"] = str(quote["_id"])

        return Response(response=json.dumps(quotes),
                        status=200,
                        mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Error": "Cannot read quotes"}),
                        status=500,
                        mimetype='application/json')

####################################################################################################################################

@app.route("/quotes/<id>", methods=["GET"])
def get_quote(id):
    """
    Function to get a quote
        1. check if quote_id is valid exists in db
        2. get quote
    """
    try:
        # check if id is valid and exists in db
        if ObjectId.is_valid(id)==False:
            return Response(response=json.dumps({"Error": "Id is invalid"}),
                            status=400,
                            mimetype='application/json')
                            
        # check if id exists in db
        quote = list(db.quotes.find({"_id":ObjectId(id)}))
        if len(quote) == 0:
            return Response(response=json.dumps({"Error": "Id does not exist"}),
                            status=400,
                            mimetype='application/json')

        quote[0]["_id"] = str(quote[0]["_id"])

        return Response(response=json.dumps(quote[0]),
                        status=200,
                        mimetype='application/json')

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Error": "Cannot read quote"}),
                        status=500,
                        mimetype='application/json')

####################################################################################################################################

@app.route("/quotes/random", methods=["GET"])
def get_random_quote():
    """
    Function to return a random quote 
    """
    try:

        randomQuote = list(db.quotes.aggregate(
            [ { "$sample": { "size": 1 } } ]
        ))

        if len(randomQuote) == 0:
            return Response(response=json.dumps({"Message": "No documents in collection"}),
                            status=200,
                            mimetype='application/json')
        
        randomQuote[0]["_id"] = str(randomQuote[0]["_id"])

        return Response(response=json.dumps(randomQuote[0]),
                        status=200,
                        mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Error": "Cannot read quotes"}),
                        status=500,
                        mimetype='application/json')

####################################################################################################################################

@app.route("/quotes/substring", methods=["GET"])
def get_quote_with_substring():
    """
    Function to return a quote that contain specific text (substring must be provided in body of request)
        1. check if body of request is empty
        2. make sure that one key-value pair is given
        3. make sure value is in string format
        4. return possible quotes
    """
    try:

        reqData = None
        if request.data:
            reqData = request.get_json()

        # check if body is empty
        if reqData == None or reqData == {}:
            return Response(response=json.dumps({"Error": "Empty body in request"}),
                            status=400,
                            mimetype='application/json')

        if len(reqData) > 1:
            return Response(response=json.dumps({"Error": "Give only one key-value pair containing the substring"}),
                            status=400,
                            mimetype='application/json')

        # extract substring from body's request
        substring = None
        for key in reqData:
            if isinstance(reqData[key], str) == False:
                return Response(response=json.dumps({"Error": "Substring must be in string format"}),
                                status=400,
                                mimetype='application/json')
            substring = str(reqData[key])

        quotesWithSubstring = []
        quotes = list(db.quotes.find()) 
        # iterate through quotes
        for quote in quotes:
            # if text field contains the substring add quote to the list
            if substring in quote["text"]:
                quote["_id"] = str(quote["_id"])
                quotesWithSubstring.append(quote)
        
        if len(quotesWithSubstring) == 0:
            return Response(response=json.dumps({"Message": f"No quotes containing substring '{substring}' found"}),
                            status=200,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps(quotesWithSubstring),
                            status=200,
                            mimetype='application/json')

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"Error": "Cannot get quote with substring"}),
                        status=500,
                        mimetype='application/json')

####################################################################################################################################


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    