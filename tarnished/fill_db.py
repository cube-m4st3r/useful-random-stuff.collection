import mysql.connector
import config
import json
import os
from db import get_json_req_attribute, get_json_scale_attribute

def init_database():
    global mydb

    mydb = mysql.connector.connect(
        host=config.botConfig["host"],
        user=config.botConfig["user"],
        password=config.botConfig["password"],
        port=config.botConfig["port"],
        database=config.botConfig["database"],
        charset='utf8mb4'
    )

    global cursor
    cursor = mydb.cursor(buffered=True)

    if mydb.is_connected():
        print("Database connection successful")
    else:
        print("Database connection failed")
        return
    
def fill_db_weapons():
    # read the JSON file
    with open('Data/weapons.json', 'r') as f:
        data = json.load(f)

    # iterate over the objects
    for weapon in data:
        weapon_name = weapon['name'].replace("'", "''")
        req_vigor = get_json_req_attribute(weapon, "Vig")
        req_mind = get_json_req_attribute(weapon, "Min")
        req_endurance = get_json_req_attribute(weapon, "End")
        req_strength = get_json_req_attribute(weapon, "Str")
        req_dexterity = get_json_req_attribute(weapon, "Dex")
        req_intelligence = get_json_req_attribute(weapon, "Int")
        req_faith = get_json_req_attribute(weapon, "Fai")
        req_arcane = get_json_req_attribute(weapon, "Arc")

        scl_vigor = get_json_scale_attribute(weapon, "Vig")
        scl_mind = get_json_scale_attribute(weapon, "Min")
        scl_endurance = get_json_scale_attribute(weapon, "End")
        scl_strength = get_json_scale_attribute(weapon, "Str")
        scl_dexterity = get_json_scale_attribute(weapon, "Dex")
        scl_intelligence = get_json_scale_attribute(weapon, "Int")
        scl_faith = get_json_scale_attribute(weapon, "Fai")
        scl_arcane = get_json_scale_attribute(weapon, "Arc")

        total_dmg = sum(attack['amount'] for attack in weapon['attack'])

        sql = f"INSERT INTO item VALUES (NULL,'{weapon_name}', {total_dmg}, {total_dmg * 6}, '{weapon['category']}', 'Weapon', {req_vigor}, {req_mind}, {req_endurance}, {req_strength}, {req_dexterity}, {req_intelligence}, {req_faith}, {req_arcane}, 1, {weapon['weight']}, '{weapon['image']}', '{scl_vigor}', '{scl_mind}', '{scl_endurance}', '{scl_strength}', '{scl_dexterity}', '{scl_intelligence}', '{scl_faith}', '{scl_arcane}' );"

        cursor.execute(sql)
        mydb.commit()

    print("Added weapons..")

def fill_db_armor():
    # read the JSON file
    with open('Data/armor.json', 'r') as f:
        data = json.load(f)

    # iterate over the objects
    for armor in data:
        armor_name = armor['name'].replace("'", "''")

        total_negation = sum(negation['amount'] for negation in armor['dmgNegation'])

        sql = f"INSERT INTO item VALUES (NULL,'{armor_name}', {total_negation}, {total_negation * 40}, '{armor['category']}', 'Armor', 0, 0, 0, 0, 0, 0, 0, 0, 1, {armor['weight']}, '{armor['image']}', '-', '-', '-', '-', '-', '-', '-', '-');"

        cursor.execute(sql)
        mydb.commit()

    print("Added armor..")

def fill_db_utils():
    with open('test.txt', 'r') as f:
        for line in f:
            if line.strip():
                cursor.execute(line)
                mydb.commit()
    print("Added utils..")

init_database()
fill_db_weapons()
fill_db_armor()
fill_db_utils()
print("Starting Tarnished..")
os.system("python3 TarnishedBot.py 1")
