from cmath import e
from email import header
from logging import exception
import socket, struct
import tkinter as tk
import random
import json
from wsgiref import headers 
import requests
from elasticsearch import Elasticsearch

headers_parameter = {'Content-type': 'application/json'}
id_parameter = None
index_parameter = "calculator"

# Initializing Elasticsearch class
es = Elasticsearch('https://localhost:9200')

# ------- Insert Data in the index ---------------
def create_index(index):
    es.indices.create(index=index, ignore=400)

def insert_one_data(data):
    # index and doc_type you can customize by yourself
    res = es.index(index=index_parameter, id=id_parameter, body=data)
    # index will return insert info: like as created is True or False
    print(res)
    """
    {'_index': 'test-index', '_type': 'authors', '_id': '5', '_version': 1, 'result': 'created', '_shards': {'total': 2, 's
uccessful': 1, 'failed': 0}, '_seq_no': 4, '_primary_term': 1}
    """

# Initializing Tkinter
root= tk.Tk()

# Variable declarations
source_ip = None
destination_ip = None
port_number = None
message = ""
key_message = {}
frequency = None

# Canvas Initialization
canvas1 = tk.Canvas(root, width = 400, height = 400,  relief = 'raised')
canvas1.pack()

# Label for ElasticSearch Calculator
label1 = tk.Label(root, text='ElasticSearch Claculator')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

# Label For Type Source IP:
label2 = tk.Label(root, text='Type Source IP:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 50, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(200, 75, window=entry1)

# Label For Type Destination IP:
label3 = tk.Label(root, text='Type Destination IP:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label3)

entry2 = tk.Entry (root) 
canvas1.create_window(200, 125, window=entry2)

# Label for Type Port Number'
label4 = tk.Label(root, text='Type Port Number')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 150, window=label4)

entry3 = tk.Entry (root) 
canvas1.create_window(200, 175, window=entry3)

# Label for Type Message
label5 = tk.Label(root, text='Type Message')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 200, window=label5)

entry4 = tk.Entry (root) 
canvas1.create_window(200, 225, window=entry4)

def store_data_into_variable ():
    
    source_ip = entry1.get()
    destination_ip = entry2.get()
    port_number = entry3.get()
    message = entry4.get()

    # using socket, struct
    packedIP = socket.inet_aton(source_ip)
    source_ip = struct.unpack("!L", packedIP)[0]
    
    packedIP = socket.inet_aton(destination_ip)
    destination_ip = struct.unpack("!L", packedIP)[0]    
    port_number = int(port_number)

    key = source_ip + destination_ip + port_number
    
    label3 = tk.Label(root, text= f'The key is {key}',font=('helvetica', 10))
    canvas1.create_window(200, 295, window=label3)

    label4 = tk.Label(root, text= f'The Message is "{message}"',font=('helvetica', 10))
    canvas1.create_window(200, 310, window=label4)
    
    url_parameter_update = f"http://localhost:9200/calculator/_doc/{key}"
    req_get_info = requests.get(url = url_parameter_update, headers = headers_parameter)


    if req_get_info.status_code == 200:
        random_number = random.randint(0,10)

        req_data = json.loads(req_get_info.text)
        
        try:
            temp_frequency = req_data["_source"]["frequency"] + 1
        except KeyError as e:
            temp_frequency = req_data["_source"]["doc"]["frequency"] + 1
            temp_message = req_data["_source"]["doc"]["message"]

        temp_dict = {
            'frequency': temp_frequency,
            'message': message,
            'score': random_number

        }
        data_json_update = json.dumps(temp_dict)
        req_update = requests.post(url = url_parameter_update, data = data_json_update, headers = headers_parameter)
        


    else:
        random_number = random.randint(80,100)
        temp_dict = {
                            'message': message,
                            'frequency': 1,
                            'score': random_number
                    }

        id = key
        key_message.update(temp_dict)
        data_json = json.dumps(temp_dict)
        url_parameter = f"http://localhost:9200/calculator/_doc/{key}/_create"

        req = requests.post(url = url_parameter, data = data_json, headers = headers_parameter)

        # insert_one_data(data = temp_dict)

    
button1 = tk.Button(text='Store the Key and Message', command=store_data_into_variable, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 265, window=button1)

if __name__ == "__main__":
    root.mainloop()