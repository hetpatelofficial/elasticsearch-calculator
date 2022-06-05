import socket, struct
from tkinter import *
from tkinter import filedialog
import random
import json
import requests
from elasticsearch import Elasticsearch
import pandas as pd

headers_parameter = {'Content-type': 'application/json'}
id_parameter = None
index_parameter = "calculator"

# Initializing Elasticsearch class
es = Elasticsearch('https://localhost:9200')

# Variable declarations
source_ip = None
destination_ip = None
port_number = None
message = ""
key_message = {}
frequency = None
data_list = None

def browse_files():
    filename = filedialog.askopenfilename(initialdir = "/",
    									title = "Select a File",
    									filetypes = (("Text files",
    													"*.txt*"),
    												("all files",
    													"*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)
    df = pd.read_csv(filename)
    data = df.values
    data_list = data.tolist()
    for index in range(len(data_list)):
        temp = str(data_list[index]).split(';')
        store_data_into_variable(temp)

def store_data_into_variable (temp):
    
    temp[0] = temp[0].replace("'","")
    temp[0] = temp[0].replace("[","")
    message = temp[0]
    source_ip = temp[1]
    port_number = temp[2]
    destination_ip = temp[3]
 

    # using socket, struct
    packedIP = socket.inet_aton(source_ip)
    source_ip = struct.unpack("!L", packedIP)[0]
    
    packedIP = socket.inet_aton(destination_ip)
    destination_ip = struct.unpack("!L", packedIP)[0]    
    port_number = int(port_number)

    key = source_ip + destination_ip + port_number
    
    url_parameter_update = f"http://localhost:9200/calculator/_doc/{key}"
    req_get_info = requests.get(url = url_parameter_update, headers = headers_parameter)


    if req_get_info.status_code == 200:
        random_number = random.randint(0,10)

        req_data = json.loads(req_get_info.text)
        
        try:
            temp_frequency = req_data["_source"][f"{key}"]["frequency"] + 1
        except KeyError as e:
            temp_frequency = req_data["_source"]["doc"]["frequency"] + 1
            temp_message = req_data["_source"]["doc"]["message"]
        temp_dict = {'doc':{
            'frequency': temp_frequency,
            'message': message,
            'score': random_number

        }}
        data_json_update = json.dumps(temp_dict)
        req_update = requests.post(url = url_parameter_update, data = data_json_update, headers = headers_parameter)
        print(data_json_update)
        print(key)


    else:
        random_number = random.randint(80,100)
        temp_dict = {key:{
                            'message': message,
                            'frequency': 1,
                            'score': random_number
                    }}

        id = key
        key_message.update(temp_dict)
        data_json = json.dumps(temp_dict)
        url_parameter = f"http://localhost:9200/calculator/_doc/{key}"

        req = requests.post(url = url_parameter, data = data_json, headers = headers_parameter)
        print(data_json)
        print(key)


        # insert_one_data(data = temp_dict)


# Create the root window
window = Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("500x500")

#Set window background color
window.config(background = "white")

# Create a File Explorer label
label_file_explorer = Label(window,
							text = "File Explorer using Tkinter",
							width = 100, height = 4,
							fg = "blue")

	
button_explore = Button(window,
						text = "Browse Files",
						command = browse_files)

button_exit = Button(window,
					text = "Exit",
					command = exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)

button_explore.grid(column = 1, row = 2)

button_exit.grid(column = 1,row = 3)




if __name__ == "__main__":
    # Let the window wait for any events
    window.mainloop()