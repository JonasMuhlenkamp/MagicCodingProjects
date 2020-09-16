#This program will create a list of all MTG sets in a specific order.  Expansions that rotated through Standard
#are sorted in reverse chronological order (i.e, Avacyn Restored, Dark Ascension, Innistrad), followed by
#all supplemental sets in alphabetical order.

#Note - some sets have errors in TCGplayer's database.  Currently (7/31/2020) there are 13 
#supplemental sets listed as non-supplemental, and 11 sets that have incorrect release date 
#information.  If a new set possesses a similar error, simply add an elif statement to the 
#appropriate tree following the pattern of the previous statements, and the set should be 
#placed in the correct location.

import requests
import json
import csv
import os
from collections import OrderedDict

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    return text

def update_set_list(export_filepath):

    print("Accessing TCGPlayer API...")

    PUBLIC_KEY = os.environ.get('TCG_PUBLIC_KEY')
    PRIVATE_KEY = os.environ.get('TCG_PRIVATE_KEY')

    #Set up the headers and keys for the post request 
    headers = {"User-Agent": "Nautilus", "From": "nautilus.application@gmail.com", "application": "x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials", "client_id": PUBLIC_KEY, "client_secret": PRIVATE_KEY}

    #Request the token
    response = requests.post("https://api.tcgplayer.com/token", headers=headers, data=data)
    response_dict = json.loads(response.text)

    #Save the token in the environment variables
    BEARER_TOKEN = response_dict["access_token"]
    expire_date = response_dict[".expires"]
    #os.environ['TCG_BEARER_TOKEN'] = BEARER_TOKEN
    print("Access to TCGPlayer database successful.  Current access token will expire on " + str(expire_date))
    print("Processing sets...")

    url = "https://api.tcgplayer.com/catalog/categories/1/groups?limit=100"

    headers = {"User-Agent": "Nautilus", "From": "nautilus.application@gmail.com", "accept": "application/json", "authorization": "bearer " + BEARER_TOKEN}

    response = requests.request("GET", url, headers=headers)
    response_dict = json.loads(response.text)

    sets_to_alpha = []
    sets_to_chrono = {}

    limit = response_dict["totalItems"]
    processed = 0
    chrono_count = 0
    supplementalCount = 0
    while processed < limit:
        
        for set in response_dict["results"]:

            name = set["name"]
            print(name)
            supplemental = set["isSupplemental"]

            #Problems with supplemental marking in database
            # JingHe Age Token Cards,2002-01-01,76
            # Global Series Jiang Yanggu & Mu Yanling,2018-06-22,20
            # Spellslinger Starter Kit,2018-10-05,18
            # Planeswalker Event Promos,2019-05-25,14
            # Promo Pack: Theros Beyond Death,2020-01-17,9
            # Ponies: The Galloping,2019-10-22,10
            # Promo Pack: Ikoria,2020-05-15,6
            # Commander 2020,2020-04-24,7
            # Promo Pack: Core Set 2021,2020-07-03,4
            # Double Masters,2020-08-07,1
            # Jumpstart,2020-07-17,2
            # Battlebond,2018-06-08,11
            # Commander 2019,2019-08-23,5   

            if name == "JingHe Age Token Cards":
                supplemental = True
            elif name == "Global Series Jiang Yanggu & Mu Yanling":
                supplemental = True
            elif name == "Spellslinger Starter Kit":
                supplemental = True
            elif name == "Planeswalker Event Promos":
                supplemental = True
            elif name == "Promo Pack: Theros Beyond Death":
                supplemental = True
            elif name == "Ponies: The Galloping":
                supplemental = True
            elif name == "Promo Pack: Ikoria":
                supplemental = True
            elif name == "Commander 2020":
                supplemental = True
            elif name == "Promo Pack: Core Set 2021":
                supplemental = True
            elif name == "Double Masters":
                supplemental = True
            elif name == "Jumpstart":
                supplemental = True
            elif name == "Battlebond":
                supplemental = True
            elif name == "Commander 2019":
                supplemental = True
            
            if supplemental == True:
                sets_to_alpha.append(set["name"])
                supplementalCount += 1
                #print(sets_to_alpha)
            else:
                
                #Problems in the TCG API database
                # Born of the Gods,1969-09-01,108
                # Magic 2014 (M14),1969-07-01,109
                # Dragon's Maze,1969-06-01,110
                # Magic 2013 (M13),1969-03-01,111
                # Avacyn Restored,1969-02-01,112
                # Dark Ascension,1969-01-01,113
                # Innistrad,1968-12-01,114
                # Magic 2012 (M12),1968-11-01,115
                # New Phyrexia,1968-10-01,116
                # Mirrodin Besieged,1968-09-01,117
                # Arabian Nights,1963-03-01,118

                release_date = str(set["publishedOn"])[:10]
                
                if name == "Born of the Gods":
                    release_date = "2014-02-07"
                elif name == "Magic 2014 (M14)":
                    release_date = "2013-07-19"
                elif name == "Dragon's Maze":
                    release_date = "2013-05-03"
                elif name == "Magic 2013 (M13)":
                    release_date = "2012-07-13"
                elif name == "Avacyn Restored":
                    release_date = "2012-05-04"
                elif name == "Dark Ascension":
                    release_date = "2012-02-03"
                elif name == "Innistrad":
                    release_date = "2011-09-30"
                elif name == "Magic 2012 (M12)":
                    release_date = "2011-07-15"
                elif name == "New Phyrexia":
                    release_date = "2011-05-13"
                elif name == "Mirrodin Besieged":
                    release_date = "2011-02-04"
                elif name == "Arabian Nights":
                    release_date = "1993-12-17"
                
                sets_to_chrono.update({chrono_count: {"name": name, "release_date": release_date}})
                chrono_count += 1
            processed += 1

        next_url = url + "&offset=" + str(processed)
        #print(next_url)
        response = requests.request("GET", next_url, headers=headers)
        response_dict = json.loads(response.text)

    sets_to_chrono = OrderedDict(sorted(sets_to_chrono.items(), key=lambda kv : kv[1]["release_date"], reverse=True))

    sets_to_alpha = sorted(sets_to_alpha)
    # print(chrono_count)
    # print(supplementalCount)
    #jprint(response_dict)

    with open(export_filepath, mode="w", newline="") as csv_file:

        fieldnames = ["name", "release_date", "set_key"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        chrono_sets = list(sets_to_chrono.items())
        
        i = 0
        for i in range(chrono_count):

            set_info = chrono_sets[i]
            writer.writerow({"name": set_info[1]["name"], "release_date": set_info[1]["release_date"], "set_key": i})
            
        i += 1
        for j in range(supplementalCount):

            set_info = sets_to_alpha[j]
            writer.writerow({"name": set_info, "release_date": "", "set_key": i + j})

    print("Sets processed.")