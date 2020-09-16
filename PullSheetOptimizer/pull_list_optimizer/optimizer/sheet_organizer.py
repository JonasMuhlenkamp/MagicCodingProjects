import csv
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    return text

def organize_sheet(set_list_filepath, filepath_to_process, export_filepath):

    sets = {}
    with open(set_list_filepath, mode="r", newline="") as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = -1

        for row in csv_reader:

            #Skip lines if not yet at the first line of data
            if line_count < 0:
                line_count += 1
                continue
            #Otherwise, grab the desired columns from the row
            else:

                sets.update({row[0]: row[2]})

    #jprint(sets)

    conditions = {1: {"condition": "Lightly Played", "key": 1}, 
                    2: {"condition": "Moderately Played", "key": 2}, 
                    3: {"condition": "Heavily Played", "key": 3}, 
                    4: {"condition": "Damaged", "key": 4}, 
                    5: {"condition": "Lightly Played Foil", "key": 5}, 
                    6: {"condition": "Moderately Played Foil", "key": 6}, 
                    7: {"condition": "Heavily Played Foil", "key": 7},
                    8: {"condition": "Damaged Foil", "key": 8},
                    9: {"condition": "Foreign", "key": 9},
                    10: {"condition": "Foreign Foil", "key": 10}
                }

    conditions = list(conditions.items()) 

    with open(filepath_to_process, mode="r") as csv_file:

        with open(export_filepath, mode="w", newline="") as data_file:

            fieldnames = ["quantity", "name", "set", "condition", "game", "condition_key", "set_key"]
            writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            writer.writeheader()
        
            csv_reader = csv.reader(csv_file, delimiter=",")

            #Start at -skip_rows so that the first line of data is id = 0
            line_count = -1

            #Iterate through the rows of the file
            for row in csv_reader:
                
                #Skip lines if not yet at the first line of data
                if line_count < 0:
                    line_count += 1
                    continue
                #Otherwise, grab the desired columns from the row
                else:
                    game = row[0] 
                    name = row[1]
                    quantity = row[6]
                    condition = row[2]
                    condition_key = 0
                    if str(condition).__contains__("-"):
                        if str(condition).__contains__("Foil"):
                            condition_key = 10
                        else:
                            condition_key = 9
                    
                    for cond in conditions:
                        if condition == cond[1]["condition"]:
                            condition_key = cond[1]["key"]
                    
                    #print(condition_key)
                
                    setname = row[4]
                    set_key = ""
                    if game == "Magic":
                        set_key = sets[setname]
                    #print(set_key)
                    if game != "Orders Contained in Pull Sheet:":
                        writer.writerow({"quantity": quantity, "name": name, "condition": condition, "set": setname, "game": game, "condition_key": condition_key, "set_key": set_key})


                    line_count += 1
