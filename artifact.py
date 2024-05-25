from fastapi import FastAPI, HTTPException, Response, status, Depends
import requests
import json
from requests.auth import HTTPBasicAuth
from fastapi.params import Body
from typing import Optional
import re



app = FastAPI()

print("Test Connection for Artifact")

# artifact_url = input(" Enter Artifact component  Oneops url ") or 'https://oneops.prod.walmart.com/ukgrsps/assemblies/574888052/transition/environments/988438002/platforms/988438042/components/988438105/edit.json'


# local_var = input(" Enter Local variable Oneops url ") or 'https://oneops.prod.walmart.com/ukgrsps/assemblies/asda-user-lists/transition/environments/prod-canary/platforms/user-lists!1/variables.json'

# global_var = input(" Enter  Global variable  Oneops url ") or  'https://oneops.prod.walmart.com/ukgrsps/assemblies/asda-user-lists/transition/environments/988438002/variables.json'


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


self_initial_data= []
local_initial_data=[]
global_initial_data=[]
hard_local_global = []
group_id_data= []

hard_local_global.append(a)

hard_local_global.append(b)
d.split(':')
for element in d.split(':'):
    group_id_data.append(element)
    hard_local_global.append(element)



hard_local_global.append(c)
    
# print(hard_local_global)

for i  in range (len(hard_local_global)):
    if '$OO_LOCAL' in hard_local_global[i]:
        local_initial_data.append(hard_local_global[i])
    elif '$OO_GLOBAL'  in hard_local_global[i]:
        global_initial_data.append(hard_local_global[i])
    else : 
        self_initial_data.append(hard_local_global[i])


# print("local : ", local_initial_data)
# print("global : ", global_initial_data)   
# print()
modified_list = []
# initializing sub string
# sub_str = "com"
# # slicing off after length computation
# res = self_initial_data[:self_initial_data.index(sub_str) + len(sub_str)]

modified_list.append(self_initial_data)


# Function to extract the element between curly braces
def extract_element(value):
    match = re.search(r'\$\w+\{([^}]+)\}', value)
    if match:
        return match.group(1)
    else:
        return "No match found"

# Extract and print the element
# extracted_element_Local = extract_element(global_initial_data)
# print(global_initial_data)

for curly in range(len(local_initial_data)):
    modified_list.append(extract_element(local_initial_data[curly]))
# print(local_target_keys)

# global_target_keys = []
for curly in range(len(global_initial_data)):
    modified_list.append(extract_element(global_initial_data[curly]))

target_keys = [modified_list[0][0]] + modified_list[1:]
# print(target_keys)




# target_keys = [item for item in input("Enter the list variable like 1:repository 2:groupId 3:artifactId 4:appVersion 5:extension  respectively:  ").split()]


# global_taget_keys = [   .split()]

    

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
for target_key in target_keys:
        #print(f'Searching for {local_target_key} in Local variable.')
        try:
            value = search_value(local_data, target_key)
        except KeyError as e:
            print(e)
        else:
            #print(f' {local_target_key} :  {value}')
            local_result[target_key] = value
        
    
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




final_local =  [target_keys  for target_keys in local_result.values()]

final_global =  [target_keys  for target_keys in global_result.values()]

# print(final_global)
# print(final_local)

#########  url_id  ##############

if '$OO_LOCAL'  in local_result:
        url = extract_element(a)
        url_id = local_result[url]
elif '$OO_GLOBAL' in global_result:
    url = extract_element(a)
    if url in global_result:
        url_id = global_result[url]
else:
    
    sub_str = "com"
    # slicing off after length computation
    url_id = a[:a.index(sub_str) + len(sub_str)]        
# print(url_id)

#########  repository_id  ##############



if '$OO_LOCAL' in b:
    repo = extract_element(b)
    if repo in local_result:
        repository_id = local_result[repo]
elif '$OO_GLOBAL' in b:
    repo = extract_element(b)
    if repo in global_result:
        repository_id = global_result[repo]
else:
    repository_id = b

# print(repository_id)



#########  group_id ##############



if '$OO_LOCAL' in group_id_data[0]:
    groupid = extract_element(group_id_data[0])
    if groupid in local_result:
        modified_string = local_result[groupid]
elif '$OO_GLOBAL' in group_id_data[0]:
    groupid = extract_element(group_id_data[0])
    if groupid in global_result:
        modified_string = global_result[groupid]
else:
    modified_string = group_id_data[0]
group_Id = modified_string.replace('.', '/')   
# print(group_Id)


#########  artifact_id ##############
    

if '$OO_LOCAL' in group_id_data[1]:
    artifact = extract_element(group_id_data[1])
    if artifact in local_result:
        artifact_Id = local_result[artifact]
elif '$OO_GLOBAL' in group_id_data[1]:
    artifact = extract_element(group_id_data[1])
    if artifact in global_result:
        artifact_Id = global_result[artifact]
else:
    modified_string = group_id_data[1]
# print(artifact_Id)
#########  appversion_id ##############


if '$OO_LOCAL' in c:
    appversion = extract_element(c)
    if appversion in local_result:
        appVersion_id = local_result[appversion]
elif '$OO_GLOBAL' in c:
    appversion = extract_element(c)
    if appversion in global_result:
        appVersion_id = global_result[appversion]
else:
    appVersion_id = c
# print(appVersion_id)

#########  extension_id ##############

if '$OO_LOCAL' in group_id_data[2]:
    extension = extract_element(group_id_data[2])
    if extension in local_result:
        extension_id = local_result[extension]
elif '$OO_GLOBAL' in group_id_data[2]:
    extension = extract_element(group_id_data[2])
    if extension in global_result:
        extension_id = global_result[extension]
else:
    extension_id = group_id_data[2]

# print(extension_id)


if url_id ==  "https://mvn.ci.artifacts.walmart.com" or "mvn.artifacts.walmart.com" :

    web_address = [f"{url_id}/artifactory/{repository_id}/{group_Id}/{artifact_Id}/{appVersion_id}/{artifact_Id}-{appVersion_id}.{extension_id}"]

else :
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


            
        
        


    

