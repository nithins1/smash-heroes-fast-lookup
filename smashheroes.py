import requests
from termcolor import colored
import os
import argparse

parser = argparse.ArgumentParser(description="Print Smash Heroes stats for any player.")
parser.add_argument("-c", "--compact", action="store_true", help="only print overall level and prestige count")
args = parser.parse_args()

width, height = 80, 24
try:
    width, height = os.get_terminal_size()
except:
    pass

try:
    f = open('key.txt', 'r+')
except:
    print("Could not open key.txt, check that the file exists in the current directory.")
    exit(1)

api = f.read().rstrip()
if not api:
    api = input(colored("You need an API key to access the Hypixel API.\n"
                        "Connect to mc.hypixel.net, type /api, and copy the key.\n"
                        "Then paste it here: ", "magenta"))
    f.write(api)
    f.close()

while True:
    print("-" * width)
    username = input("USERNAME: ")
    if not username:
        break # Exit when no username given
    url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
    try:
        response = requests.get(url)
    except:
        print("Unable to connect to Mojang API. Your internet is probably down.")
        break

    if response.status_code == 204:
        print("Mojang API call returned no content. Check username spelling.")
        continue
    elif response.status_code >= 500:
        print("Mojang API call resulted in server error.")
        break
    elif response.status_code != 200:
        print("Mojang API call resulted in unknown error.")
        break

    uuid = response.json()['id']
    url = f'https://api.hypixel.net/player?key={api}&uuid={uuid}'
    response = requests.get(url)

    if response.status_code == 403:
        print("Hypixel API call resulted in 403 Forbidden Error. Your API key is probably invalid.")
        break
    elif response.status_code >= 500:
        print("Hypixel API call resulted in server error.")
        break

    json = response.json()
    if json['player'] is None:
        print(username + " has never connected to Hypixel")
        continue
    elif 'stats' not in json['player'].keys():
        print("No Hypixel stats for " + username)
        continue
    elif 'SuperSmash' not in json['player']['stats'].keys():
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

    if args.compact:
        total_prestiges = 0
        for name in class_names:
            if "pg_" + name in smash_json.keys():
                total_prestiges += smash_json["pg_" + name]
        print("PRESTIGES: " + str(total_prestiges))
    else:
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
