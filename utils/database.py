import os
import json

def database():
    if not os.path.isfile('data.json'):
        with open('data.json', 'w') as json_file:
            json.dump({}, json_file) 
            return {}
    else:       
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            return data

def add_data(query, results):
    data = database()
    data[query] = results
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
        
def check_query_exists(query):
    data = database() 
    return query in data 

def get_query(query):
    data = database()
    return data.get(query, None) 