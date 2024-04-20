import secrets
from datetime import datetime

def search(query, collection):
    return list(collection.find(query))

def searchWithProjection(query, projection, collection):
    res = list(collection.find (query, projection))
    if not res:
        status = 404
        res = [{'message' : 'ERROR. Payment not found'}]
        return (res, status)
    else:
        return (res, 200) 
    
def deleteExtraQueries(data, expected_keys):
        # Get the keys of the JSON object
    data_keys = data.keys()
    
    # Check if all keys are in the expected keys list
    for key in data_keys:
        if key not in expected_keys:
            del data[key]
    return data

def getIDEvento(date, bytes):
    # Generate a random string
    random_string = secrets.token_hex(bytes)  # Generate a random hex string of 16 bytes (32 characters)
    id_evento = [random_string] + date.split('-')
    
    return ''.join(id_evento)

# check if contains all the expected_keys and not others
def checkData(data, keys):
    for key in keys:
        if key not in data:
            return (False, "Missing key {} in data sent".format(key))
    return (True, "Data seems good")

# check if contains keys between a range
def check_keys(data, expected_keys):
    # Get the keys of the JSON object
    data_keys = data.keys()
    
    # Check if all keys are in the expected keys list
    for key in data_keys:
        if key not in expected_keys:
            return False
    return True

def updateData(collection, query, updateQuery):
    res = collection.update_one(query, updateQuery)

    update_result = res.raw_result
    

    response = {"Matched" : "{} rows".format(update_result["n"])}
    response["Modified"] = "{} rows".format(update_result["nModified"])
    print(update_result['ok'])

    return response

def checkForChangeOfID(data, collection):
    id_evento = data['id_evento']
    old_id = id_evento
    
    res = collection.find_one({'id_evento' : id_evento})
    if res['location'] != data['location'] or res['date'] != data['date']:
        return (getIDEvento(data), old_id)
    return (id_evento, id_evento)

def getDate():
    present_date = datetime.now().date()
    present_date_str = present_date.strftime("%d-%m-%Y")
    return present_date_str

def generateTicketNumber(bytes, date):
    random_start = secrets.token_hex(bytes)  
    randon_end = secrets.token_hex(bytes)
    id_ticket = [random_start] + date.split('-') + [randon_end]
    return ''.join(id_ticket)

def findAbono(query, collection):
    res = list(collection.find(query))
    status = 200
    if not res:
        status = 404
        res = [{'message' : 'ERROR. Payment not found'}]
    return (res, status)