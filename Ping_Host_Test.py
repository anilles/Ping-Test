#import pandas and numpy libraries 
#import os to run ping from terminal 
import pandas as pd 
import numpy 
import os

#ask the user for the filename and assign it to the Tickets variable
Tickets = input("What file would you like to import?\n")
#Ask the user if we need to append the Response column with {key} and {ip} or just the (key)
include_host = False 
y_n = None
while y_n not in ("y", "n"):
    y_n = input("would you like to include the host in the Response column? (y/n) \n")
    if y_n == "y":
        include_host = True 
    elif y_n == "n":
        include_host = False 
    else:
        print("Please type ""y"" or ""n"" ")
#read the Ticket variable and assign it to the df Dataframe variable 
df = pd.read_excel(Tickets)

#Create an array from the Configuration items column
#Create an empty list so we can save the ping output. 
arr=df["Configuration item"].to_numpy()
list=[]

#Custom Reponses
Responses = {
    "TTL expired": "TTL expired in transit.",
    "Down": "Destination host unreachable.",
    "Timeout": "Request timed out.",
    "Up": "bytes-32 time-",
    "Not Found": "Ping request could not find host"
}
#Ping the Configuration item once.
#Based on response show if the Config Item it will print a custom response for each type 
#adds output to list so we can append the original xlsx sheet.
#Based on user response list.append will include the host {ip} or not. 
for ip in arr:
    response = os.popen(f"ping -n 1 {ip}").read()
    for key, value in Responses.items():
        if value in response:
            print (key, ip)
            if include_host == True:
                list.append(F"{key} {ip}")
            elif include_host == False:
                list.append (f"{key}")
            else:
                list.append(f"{key}")
#insert the list into the dataframe with column header Reponse.
#It will create a sheet with the reponse column if one doesn't exist or if the imported df is a page. 
df.insert(1, "Response", list)
with pd.ExcelWriter(Tickets, mode = 'a', engine='openpyx1', if_sheet_exists="replace") as writer:
    df.to_excel(writer, index=False) 
#Uncomment print (list) to verify results in the terminal.
#print (list)
