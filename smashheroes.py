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
        break # Exit when no username given
    url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
    try:
        response = requests.get(url)
        uuid = response.json()['id']
    except:
        print("Mojang API call failed. Check username spelling.")
        continue
    uuid = response.json()['id']
    url = f'https://api.hypixel.net/player?key={api}&uuid={uuid}'
    response = requests.get(url)

    if response.status_code == 403:
        print("403 Forbidden Error. Your API key is probably invalid.")
        break

    json = response.json()
    if 'SuperSmash' not in json['player']['stats'].keys():
        print("No smash data for " + username)
        continue
    smash_json = json['player']['stats']['SuperSmash']

    if 'smashLevel' not in smash_json:
        print("Smash level 0. No stats available.")
        continue

    if 'class_stats' not in smash_json:
        print("No class stats for " + username + " (never played before)")
        continue
    class_names = smash_json['class_stats'].keys()

    print("OVERALL LEVEL: " + colored(smash_json['smashLevel'], attrs=['bold']) + "\n")
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
