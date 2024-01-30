# pvpoke-to-poracleDB

This script will pull the best pvp mons from pvpoke's github site, and place them into your database.
It ignores shadows, and will only have the correct form.

I am not much of a programmer, but I enjoy doing what I can to make things work.
If you have issues or suggestions, please let me know.

***Caution***
This will delete and override anything that uses the same ID that is placed in the webhook variables.
This detects if your entries have pings or no pings, but it assumes that everything with pings has the same settings, and everything that doesn't have pings has the same settings. It will grab your pre-existing settings, but only for the first entry.

# How to use:
Populate the webhook / channel lines (eg. gl_webook, ul_webhook, ml_webhook) and the db_config.
Run the script by typing `python3 pvpoke-to-poracledb.py`





# More details:
This script will pull data from pvpoke's github source for the current best pvp mons:
https://github.com/pvpoke/pvpoke/tree/master/src/data/training/analysis/all

It splits forms from mons, then uses a masterfile to match the names and form names to IDs.
https://raw.githubusercontent.com/WatWowMap/Masterfile-Generator/master/master-latest-react-map.json

