from fastapi import FastAPI, HTTPException, Response, status, Depends
import requests
import json
from requests.auth import HTTPBasicAuth
from fastapi.params import Body
from typing import Optional
import re



app = FastAPI()

print("TEST CONNECTION FOR ARTIFACT")
# artifact_url = input(" Enter Artifact component  Oneops url ")
# local_var = input(" Enter Local variable Oneops url ")
# global_var = input(" Enter  Global variable  Oneops url ") or 'https://oneops.prod.walmart.com/boppa/assemblies/SGAv2-REST/transition/environments/498128035/variables.json'


import re
artifact_old_url = input("enter Artifact component url : ")

if '#configuration' in artifact_old_url:
    artifact_url = artifact_old_url.replace("#configuration", ".json")
else :
    print("not find")


local_old_url = input("enter local variable url : ")

if '#variables' in local_old_url:
    local_var = local_old_url.replace("#variables", "/variables.json")
else :
    print("not find")



global_old_url = input("enter global variable  url : ") or "https://oneops.prod.walmart.com/boppa/assemblies/SGAv2-REST/transition/environments/498128035#variables"

if '#variables' in global_old_url:
    global_var = global_old_url.replace("#variables", "/variables.json")
    
else :
    print("not find")


 


#dummy_url = 'https://oneops.prod.walmart.com/boppa/assemblies/SGAv2-REST/transition/environments/498128035/variables.json'
# global_var = 'https://oneops.prod.walmart.com/ukgrsps/assemblies/asda-user-lists/transition/environments/988438002/variables.json'
# artifact_url = 'https://oneops.prod.walmart.com/ukgrsps/assemblies/574888052/transition/environments/988438002/platforms/988438042/components/988438105/edit.json'
# local_var = 'https://oneops.prod.walmart.com/ukgrsps/assemblies/asda-user-lists/transition/environments/prod-canary/platforms/user-lists!1/variables.json'
basic = HTTPBasicAuth('v0n00v2', 'Commando!209081')
headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
platform = requests.get(artifact_url, auth=basic, headers=headers)
platform_var_data = platform.json()
# # # Store the JSON data in a file
# with open("oneops_platform_data.json", "w") as file:
#      json.dump(artifact_json, file, indent=4)

# print("Data stored successfully! PLATFORM ")

# with open("oneops_platform_data.json") as file:
#    platform_var_data =  json.load(file)


a = platform_var_data['ciAttributes']['url']
b = platform_var_data['ciAttributes']['repository']
c = platform_var_data['ciAttributes']['version']
d = platform_var_data['ciAttributes']['location']


print()
print('###################  Variable define at Artifact-Component #################################')
print()
print ({"Url " : a  })
print('---')
print ({"Repository " :  b  })
print('---')
print({"Location ":  d })
print('---')
print({"Version ": c })
print('---')
print('######################################################')
print('********************************************************************************************')
print()


local_var_platform = requests.get(local_var,  auth=basic, headers=headers)
local_var_data = local_var_platform.json()
# with open("oneops_local_var.json", "w") as file:
#     json.dump(local_var_json, file, indent=4)

# print("Data stored  successfully for local !")

# with open("oneops_local_data.json") as file:
#     local_var_data =  json.load(file)





global_url = requests.get(global_var,  auth=basic, headers=headers)
global_var_data = global_url.json()
# # Store the JSON data in a file
# with open("oneops_global_data.json", "w") as file:
#     json.dump(global_var_json, file, indent=4)

# print("Data stored successfully! for global")

# with open("oneops_global_data.json") as file:
#     global_var_data =  json.load(file)


# @app.get("/platform")
# #def get_posts():
   
   
#@app.get("/platform/local")
#def get_posts():

# Function to load JSON data from a file
# def load_json(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

target_keys = [item for item in input("Enter the list variable like 1:repository 2:groupId 3:artifactId 4:appVersion 5:extension  respectively:  ").split()]



# Function to search for a value in the Local JSON data
def search_value(local_data, target_key):
        for item in local_data:
            if target_key in item["ciName"]:
                return item["ciAttributes"]["value"]
        raise KeyError(f'Element with key {target_key} not found in the LOCAL')

    # Load JSON data
    # json_file_path = 'nested_data.json'
    # local_data = load_json(json_file_path)

local_data = local_var_data

# List of target keys to search for
# Search for each target key in the JSON data
    
local_result = {}
for local_target_key in target_keys:
        #print(f'Searching for {local_target_key} in Local variable.')
        try:
            value = search_value(local_data, local_target_key)
        except KeyError as e:
            print(e)
        else:
            #print(f' {local_target_key} :  {value}')
            local_result[local_target_key] = value
        
    
print("Final for local_variable results:", local_result)
print()
print()

#searching in global variable

def search_value(global_data , target_key):
        for item in global_data:
            if target_key in item["ciName"]:
                return item["ciAttributes"]["value"]
        raise KeyError(f'Element with key {target_key} not found in GLOBAL')

    # Load JSON data
    # json_file_path = 'nested_data.json'
    # global_data, = load_json(json_file_path)

global_data = global_var_data
# List of target keys to search for
# Search for each target key in the JSON data
global_result = {}
for target_key in target_keys:
        #print(f'Searching for {target_key} in GLOBAL')
        try:
            value = search_value(global_data, target_key)
        except KeyError as e:
            print(e)
        else:
            #print(f' {target_key} :  {value}')
            global_result[target_key] = value
       
print("Final for Global_variable results:", global_result)

print(target_keys)


final_local =  [target_keys  for target_keys in local_result.values()]

final_global =  [target_keys  for target_keys in global_result.values()]

# print(final_global)
# print(final_local)


url_id = input("do you want to correction at url or press enter to continue :  ") or a


if '$OO_LOCAL' in b:
        
    new_repository_id =  final_local[0]
else:
    new_repository_id =  final_global[0]

repository_id = input("do you want to correction at repository or press enter to continue :  ") or new_repository_id

if '$OO_LOCAL' in d:
        
    modified_string  =  final_local[1]
else:
    modified_string  =  final_global[1]

if '$OO_LOCAL' in d:
        
    artifact_Id =  final_local[2]
else:
    artifact_Id =  final_global[2]

if '$OO_LOCAL' in c:
        
    appVersion_id =  final_local[3]
else:
    appVersion_id =  final_global[3]

if '$OO_LOCAL' in d:
        
    extension_id =  final_local[4]
else:
    extension_id =  final_global[4]

# # # Replace periods with slashes
group_Id = modified_string.replace('.', '/')


if url_id == "https://mvn.ci.artifacts.walmart.com/" or "https://mvn.ci.artifacts.walmart.com" :

    web_address = [f"{url_id}/artifactory/{repository_id}/{group_Id}/{artifact_Id}/{appVersion_id}/{artifact_Id}-{appVersion_id}.{extension_id}"]

elif url_id == "https://repository.walmart.com/" or "https://repository.walmart.com/" or "http://repo.wal-mart.com/" or "http://repo.wal-mart.com" :
    
    web_address = [f"{url_id}/content/repositories/{repository_id}/{group_Id}/{artifact_Id}/{appVersion_id}/{artifact_Id}-{appVersion_id}.{extension_id}"]
 
statuses = {
    200: "Website Available",
    301: "Permanent Redirect",
    302: "Temporary Redirect",
    404: "Not Found",
    500: "Internal Server Error",
    503: "Service Unavailable"
    }
    
for url in web_address:
    try:
        web_response = requests.get(url)
        print(url, statuses[web_response.status_code])
    
    except:
        print(url, statuses[web_response.status_code])          


            
        
        


    

