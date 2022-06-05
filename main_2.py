import ipaddress
import socket, struct
import tkinter as tk
import random

root= tk.Tk()

# Variable declarations
source_ip = None
destination_ip = None
port_number = None
message = ""

key_message = {}

frequency = None

canvas1 = tk.Canvas(root, width = 400, height = 400,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='ElasticSearch Claculator')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Type Source IP:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 50, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(200, 75, window=entry1)

label3 = tk.Label(root, text='Type Destination IP:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label3)

entry2 = tk.Entry (root) 
canvas1.create_window(200, 125, window=entry2)

label4 = tk.Label(root, text='Type Port Number')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 150, window=label4)

entry3 = tk.Entry (root) 
canvas1.create_window(200, 175, window=entry3)

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
    # x1 = entry1.get()

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
    
    # label4 = tk.Label(root, text= float(x1)**0.5,font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 240, window=label4)
    
    if key in key_message.keys():
        random_number = random.randint(0,10)
        
        key_message[key]['frequency'] += 1
        key_message[key]['message'] = message
        key_message[key]['score'] = random_number


    else:
        random_number = random.randint(80,100)
        temp_dict = {key:{
                            'message': message,
                            'frequency': 1,
                            'score': random_number
                    }}

        key_message.update(temp_dict)

    print(key_message)
    
button1 = tk.Button(text='Store the Key and Message', command=store_data_into_variable, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 265, window=button1)

root.mainloop()




# source_ip,destination_ip,port_number = input("Enter Source IP, Destination IP and Port Numeber: ").split()
# message = input("Enter message: ")

# source_ip = "10.10.20.2"
# destination_ip = "20.30.40.3"
# port_number = "4000"

# Using ipaddress module 
# source_ip = ipaddress.ip_address(source_ip)
# destination_ip = ipaddress.ip_address(destination_ip)
# port_number = int(port_number)
# message = "hello"

# using socket, struct
packedIP = socket.inet_aton(source_ip)
source_ip = struct.unpack("!L", packedIP)[0]
print(source_ip)

packedIP = socket.inet_aton(destination_ip)
destination_ip = struct.unpack("!L", packedIP)[0]
print(destination_ip)

port_number = int(port_number)

# Dereferencing IP
print(socket.inet_ntoa(struct.pack('!L', source_ip)))


# ip_int = int(source_ip)
# print(type(int(source_ip)))


# Print file types 

# print(f'''
# Types
# source_ip: {type(source_ip)},
# destination_ip: {type(destination_ip)},
# port_number: {type(port_number)},
# message: "{type(message)}"
# ''')


print(f'''
source_ip: {source_ip},
destination_ip: {destination_ip},
port_number: {port_number},
message: "{message}"
''')

key = source_ip + destination_ip + port_number
print(key)


