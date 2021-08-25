import requests
from termcolor import colored
import os

width, height = os.get_terminal_size()

f = open('key.txt','r')
api = f.read().rstrip()

while True:
    print("-" * width)
    username = input("USERNAME: ")
    if not username:
        break
    url = f'https://api.mojang.com/users/profiles/minecraft/{username}?'
    try:
        response = requests.get(url)
        uuid = response.json()['id']
    except:
        print("Mojang API call failed. Check username spelling.")
        continue
    uuid = response.json()['id']

    #print(uuid) #7125ba8b1c864508b92bb5c042ccfe2b
    url = f'https://api.hypixel.net/player?key={api}&uuid={uuid}'
    response = requests.get(url)
    json = response.json()

    if 'SuperSmash' not in json['player']['stats'].keys():
        print("No smash data for " + username)
        continue
    smash_json = json['player']['stats']['SuperSmash']

    if 'class_stats' not in smash_json:
        print("No class stats for " + username + " (never played before)")
        continue
    class_names = smash_json['class_stats'].keys()

    print("OVERALL LEVEL: " + str(smash_json['smashLevel']) + "\n")
    prestiged_classes = set()
    print("PRESTIGES:")
    for name in class_names:
        if "pg_" + name in smash_json.keys():
            print(name + ": " + str(smash_json["pg_" + name]))
            prestiged_classes.add(name)
    print("\nLEVELS:")
    for name in class_names:
        if "lastLevel_" + name in smash_json.keys():
            msg = name + ": " + str(smash_json["lastLevel_" + name])
            if name in prestiged_classes:
                msg = colored(msg, "red")
            print(msg)


print("-" * width)
