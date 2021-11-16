# Import libraries:
from IPython.display import Audio
import random

# define rooms and items

#GAME ROOM

game_room = {
    "name": "Game room",
    "type": "room",
}

couch = {
    "name": "couch",
    "type": "furniture",
}

piano = {
    "name": "piano",
    "type": "musical",
}


door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

#BEDROOM 1

bedroom1 = {
    "name": "Bedroom 1",
    "type": "room",
}

queenbed = {
    "name": "queen bed",
    "type": "furniture",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

#BEDROOM 2

bedroom2 = {
    "name": "Bedroom 2",
    "type": "room",
}

doublebed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "special",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

#defining door now becaise we need to define also the key after

door_d = {
    "name": "door d",
    "type": "door",
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

#LIVING ROOM


livingroom = {
    "name": "Living room",
    "type": "room",
}

diningtable = {
    "name": "dining table",
    "type": "furniture",
}

randomlist = random.sample(range(10, 99), 3)
password = [str(num) for num in randomlist]
password = " ".join(password)

paper = {
    "name": "a paper with the code: " + password,
    "type": "paper_code",
    "target": dresser,
}


outside = {
    "name": "Outside",
}

all_rooms = [game_room, bedroom1, bedroom2, livingroom]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related


object_relations = {
    "Game room": [couch, piano, door_a],
    "Bedroom 1": [queenbed, door_a, door_b, door_c],
    "Bedroom 2": [doublebed, dresser, door_b],
    "Living room": [diningtable, door_c, door_d],
    "piano": [key_a],
    "queen bed": [key_b],
    "double bed": [key_c],
    "dresser": [key_d],
    "dining table": [paper],
    "door a": [game_room, bedroom1],
    "door b": [bedroom1, bedroom2],
    "door c": [bedroom1, livingroom],
    "door d": [livingroom, outside],
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    sound_file = '/Users/msart/Desktop/IronHack/Module_1/Project/jaws_theame_song.mp3'
    display(Audio(sound_file, autoplay=True))
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'? ").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine? ").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'. ")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "special"):
                have_code = input("The dresser is locked and you need a special code: ")
                code_list = have_code.split()
                code = " ".join(code_list)
                if code == password:
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "You don't have the right code"
            elif(item["type"] == "musical"):
                music_code1 = input("The piano is locked. To opne, play three notes in the correct sequence: ")
                music_list1 = music_code1.split()
                music_code1 = " ".join(music_list1)
                if music_code1 == 'do':
                    music_code2 = input("You got the first note. Play the next one: ")
                    music_list2 = music_code2.split()
                    music_code2 = " ".join(music_list2)
                    if music_code2 == 're':
                        music_code3 = input("You got the second note. Play the next one: ")
                        music_list3 = music_code3.split()
                        music_code3 = " ".join(music_list3)
                        if music_code3 == 'mi':
                            item_found = object_relations[item["name"]].pop()
                            game_state["keys_collected"].append(item_found)
                            output += "You find " + item_found["name"] + "."
                        else:
                            output += "You played the wrong note"
                    else:
                        output += "You played the wrong note"
                else:
                    output += "You played the wrong note"
            elif(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break
        

    if(output is None):
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no' ").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()