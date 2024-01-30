import requests
import json
import mysql.connector

#This script will grab data from the first row in the database that matches the ID.
#It will do it for rows with and without pings, maintaining your pings and settings for your ping and non pings assuming that they are uniform.

#This script supports forms, and while it will not add shadow pokemon, it will add legendary and other typically not obtainable mons in the wild.

#This will endlessly increase your UID count and a better method should be used to reuse the values?

db_config = {
    'host': 'yourdbiphere',
    'user': 'yourusernamehere',
    'password': 'yourpasswordhere',
    'database': 'yourdatabasehere'
}

#Get ID and Form data
master_data_url = "https://raw.githubusercontent.com/WatWowMap/Masterfile-Generator/master/master-latest-react-map.json"
response = requests.get(master_data_url)
master_data = response.json()



#I have selected all, but there are specific leagues you can also choose from here:
#https://github.com/pvpoke/pvpoke/tree/master/src/data/training/analysis
league_dict = {
    'GL': 'https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/training/analysis/all/1500.json',
    'UL': 'https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/training/analysis/all/2500.json'
    #'ML': 'https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/training/analysis/all/10000.json'
}

#Webhook or channel ID
gl_webhook = 'YourWebhookHere'
ul_webhook = 'YourWebhookHere'
ml_webhook = ''


for var in league_dict:
    # Get the URL for the current league
    url = league_dict[var]
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print("URL cannot be found")
            break
    except Exception as e:
        print(f"An error occurred: {e}")
        # If an exception occurs, break out of the loop
        break
    
    poracle_monsters = response.json()
    if "GL" in var:
        print("Doing GL")
        target_id = gl_webhook
    if "UL" in var:
        print("Doing UL")
        target_id = ul_webhook
    if "ML" in var:
        target_id = ml_webhook

    pokemon_names = []
    form_names = []
    
    data = response.json()
    #Put everthing under "Performers" in an array, and store in variable.
    performers = data["performers"]
    
    
    #For each performer inside of the performers Array/Variable
    for performer in performers:

        #Split the pokemon name by spaces? This should contain anything with an underscore.
        pokemon_name = performer["pokemon"].split()[0] 


        #This will spit out mons in the format of mon_form if the form exists.
        if "_shadow" not in pokemon_name:
            if '_' in pokemon_name:
                split_values = pokemon_name.split('_')
                pokemon = split_values[0]
                pokemon_names.append(pokemon)
                form = split_values[1]
                form_names.append(form)
            else:
                mon = pokemon_name
                pokemon_names.append(pokemon_name)
                form = "0"
                form_names.append(form)

    #print("Pokemon Names:", pokemon_names, form_names)
    #print("Pokemon names:", pokemon_names)
    #print(str(len(pokemon_names)))
    #print("Form names   :", form_names)
    #print(str(len(form_names)))

    # Load JSON data
    pokemon_data = master_data["pokemon"]

    # Arrays to store Pokemon IDs and Form IDs
    pokemon_ids = []
    form_ids = []

    # Iterate through each Pokemon name
    for pokemon_name, form_name in zip(pokemon_names, form_names):
        # Search for the Pokemon in the JSON data
        #print("1.Printing pokemon_name and form_name")
        #print(pokemon_name, form_name)
        
        found_match = False  # Flag to track whether a match is found for the current Pokemon
        for key, value in pokemon_data.items():
            if value["name"].lower() == pokemon_name:
                # Store Pokemon ID
                #Print("2.Found the pokemon ID in data json")
                pokemon_ids.append(value["pokedexId"])

                # Check if the form matches the pre-existing form array
                if "0" in form_name:
                    # Print("3.Form is 0!")
                    form_ids.append("0")
                    break
                    
                else:
                
                    # Iterate through forms
                    forms_data = value["forms"]
                    for form_id, form_object in forms_data.items():
                        # For some reason pvpoke stores it as alolan instead of alola.
                        if "alolan" in form_name:
                            form_name = "alola"
                            #Print("3.1Form name matches, save it")
                            form_ids.append(str(form_id))
                            found_match = True
                            break
                        else:
                            if form_object.get("name", "").lower() == form_name.lower():
                                # Form name matches, save the form_id
                                #Print("3.2Form name matches, save it")
                                form_ids.append(str(form_id))
                                found_match = True
                                break

                    # No match found for the given form_name
                    if not found_match:
                        print(f"No matching form found for {form_name} in Pokemon with ID {key}")

                # Continue searching for other forms if no match is found
                if not found_match:
                    print(f"No matching Pokemon found for {pokemon_name}")
        



    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    #print("settings_row is of type:", type( settings_row))
    # Get the pre existing settings for ping and non ping.
    #cursor.execute("SELECT * FROM monsters WHERE id = %s AND ping = '' LIMIT 1", (target_id,))
    #settings_row = cursor.fetchall()
    #settings_row = list(settings_row[0]) if settings_row else []
    
    #cursor.execute("SELECT * FROM monsters WHERE id = %s AND ping != '' LIMIT 1", (target_id,))
    #ping_settings_row = cursor.fetchall()
    #ping_settings_row = list(ping_settings_row[0]) if ping_settings_row else []
    # Query to retrieve a row where 'id' matches 'target_id' and 'ping' is an empty string
    empty_ping_query = "SELECT * FROM monsters WHERE id = %s AND ping = '' LIMIT 1"

    # Query to retrieve a row where 'id' matches 'target_id' and 'ping' is not an empty string
    non_empty_ping_query = "SELECT * FROM monsters WHERE id = %s AND ping != '' LIMIT 1"

    # Execute the first query
    cursor.execute(empty_ping_query, (target_id,))
    settings_row = cursor.fetchall()
    settings_row = list(settings_row[0]) if settings_row else []
    
    
    #print("var")
    #print(var)
    #print("showing settings_row")
    #print(settings_row)
    # Execute the second query
    cursor.execute(non_empty_ping_query, (target_id,))
    ping_settings_row = cursor.fetchall()
    ping_settings_row = list(ping_settings_row[0]) if ping_settings_row else []




    #Delete old rows
    #delete_query = 'DELETE FROM monsters WHERE id = %s'
    #cursor.execute(delete_query, (target_id,))
    
    cursor.execute(f'DELETE FROM monsters WHERE id = %s', (target_id,))
    conn.commit()
    
    #print("What is the current webhook?")
    #print(target_id)
    #print("settings row")
   # print(settings_row[1])
    
    #I need a working if statement a non ping row doesnt exist.
    if settings_row:
        for pokemon_id, form_id in zip(pokemon_ids, form_ids):
            #print("Doing non ping")
            #print(pokemon_id)
            #print(len(settings_row))
            settings_row[3] = pokemon_id
            settings_row[17] = form_id
            settings_row[22] = None #Sending NULL to SQL so it will use a new UID.


            # Create a comma-separated string of placeholders for the columns in the INSERT INTO statement
            placeholders = ', '.join(['%s' for _ in range(len(settings_row))])  # Exclude the last element (uid)

            cursor.execute(f'''
                INSERT INTO monsters
                VALUES ({placeholders})
            ''', tuple(settings_row))
        # Commit the changes
            conn.commit()
        #print("Done non ping")

    if ping_settings_row:
        for pokemon_id, form_id in zip(pokemon_ids, form_ids):
            #print("Doing ping")
            #print(pokemon_id)
            #print(len(settings_row))
            ping_settings_row[3] = pokemon_id
            ping_settings_row[17] = form_id
            ping_settings_row[22] = None #Sending NULL to SQL so it will use a new UID.


            # Create a comma-separated string of placeholders for the columns in the INSERT INTO statement
            placeholders = ', '.join(['%s' for _ in range(len(ping_settings_row))])  # Exclude the last element (uid)

            cursor.execute(f'''
                INSERT INTO monsters
                VALUES ({placeholders})
            ''', tuple(ping_settings_row))
        # Commit the changes
            conn.commit()
        #print("Done ping")
    # Close the connection
    cursor.close()
    conn.close()
    print("END")
    #break