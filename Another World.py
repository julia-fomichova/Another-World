class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ""
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

class World: 
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        ''' takes in a string that is a noun representing an obect that the 
            player wants to look at, returns None, prints the name and 
            description of the noun
            Effects: reads in a string, prints to the screen
            
            look: World Str -> None '''
        lo_inventory = list((map(lambda x: x.name, self.player.inventory)))
        lo_contents = list((map(lambda x: x.name, self.player.location.contents)))
        if noun == "me":
            self.player.look()
        elif noun == "here":
            self.player.location.look()           
        elif noun in lo_inventory:
            self.player.inventory[lo_inventory.index(noun)].look()
        elif noun in lo_contents:
            self.player.location.contents[lo_contents.index(noun)].look()
        else:
            print(self.msg_look_fail)
            
    def inventory(self):
        ''' takes in nothing, returns None, prints a formatted list containing
            the names of the things that the plater is carrying currently
            Effects: reads in nothing and prints to the screen
            
            inventory: World -> None '''
        if self.player.inventory == []:
            print(self.msg_no_inventory)
        else:
            print('Inventory: {0}'.format(
                ', '.join(map(lambda x: x.name, self.player.inventory))))
            
    def take(self, noun):
        ''' takes in a string that is a noun representing an object that the
            player wants to pick up, returns None, if the noun is an object in 
            the player's room, mutates the World so that the object is removed
            from the player's room and added to their inventory and prints
            "Taken.", otherwise prints "You can't take that."
            Effects: reads in a string and prints to the screen
            
            take: World Str -> None '''
        things_location = list(map(lambda x: x.name, \
                                   self.player.location.contents))
        things_carrying = list(map(lambda x: x.name, self.player.inventory))        
        if noun in things_location:
            self.player.inventory.append\
                (self.player.location.contents[things_location.index(noun)])
            self.player.location.contents.pop(things_location.index(noun))
            print(self.msg_take_succ)
        else:
            print(self.msg_take_fail)            
            
    def drop(self, noun):
        ''' takes in a string that is a noun representing an object that the
            player wants to drop, returns None, if the noun is an object in 
            the player's room, mutates the World so that the object is added
            to the player's room and removed from their inventory and prints
            "Dropped.", otherwise prints "You aren't carrying that."
            Effects: reads in a string and prints to the screen
            
            drop: World Str -> None '''
        things_location = list(map(lambda x: x.name, \
                                   self.player.location.contents))
        things_carrying = list(map(lambda x: x.name, self.player.inventory))
        if noun in things_carrying:  
            self.player.location.contents.append\
                (self.player.inventory[things_carrying.index(noun)])
            self.player.inventory.pop(things_carrying.index(noun))
            print(self.msg_drop_succ)
        else:
            print(self.msg_drop_fail)
                    
    def go(self, noun):
        ''' takes in a string that is a noun representing an exit that the
            player wants to go through, returns None. If the noun is an exit in 
            the player's current room and the player is carrying an item in 
            their inventory (the key), then it mutates the World so that the 
            player is moved to the destination and looks at the new room. If 
            the exit exists but the player is not carrying the key, it prints
            a message. Otherwise, it prints "You can't go that way."
            Effects: reads in a string and prints to the screen
            
            take: World Str -> None 
            requires: no room contains two exits with the same names'''
        exit_names = list(map(lambda x: x.name, self.player.location.exits)) 
        if noun in exit_names:
            exit = self.player.location.exits[exit_names.index(noun)]
            if exit.key == None or exit.key in self.player.inventory:
                self.player.location = exit.destination
                self.player.location.look()
            else:
                print(exit.message)
        else:
            print(self.msg_go_fail)
                
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print(self.msg_verb_fail)

    def save(self, fname):
        ''' Consumes a single file name in the form of a string and writes the
            the complete game in all to the file. 
            Effects: writes to a text file
            
            save: World Str -> None
            required: file uses specified format'''
        file = open(fname, "w")
        
        # Thing
        room_contents = []
        for room in self.rooms:
            room_contents += room.contents
        lo_things = self.player.inventory + room_contents
        for thing in lo_things:
            file.write("thing #" + str(thing.id) + " " + thing.name \
                       + "\n" + thing.description + "\n")
        
        # Room
        for room in self.rooms:
            room_contents = room.contents
            lo_content_ids = list(map(lambda x: x.id, room_contents))
            content_str = ""
            for each_id in lo_content_ids:
                content_str += "#" + str(each_id)
            file.write("room #" + str(room.id) + " " + room.name \
                       + "\n" + room.description + "\n" + "contents " + \
                       content_str + "\n")
            
        # Player
        player_inventory = []
        for items in self.player.inventory:
            player_inventory += ["#" + str(items.id)]
        file.write("player #" + str(self.player.id) + " " + self.player.name + \
                   "\n" + self.player.description + "\n" + "inventory " + \
                   " ".join(player_inventory) + "\n" + "location #" + \
                   str(self.player.location.id) + "\n")
        
        # Exit
        lo_exit = []
        formatted_exits = []
        formatted_rooms = []
        
        for room in self.rooms:
            lo_exit += [[room.id, room.exits]]                         
        for room in lo_exit:
            for exit in room[1]:
                if exit.key == None:
                    file.write("exit #" + str(room[0]) + " #" + \
                               str(exit.destination.id) + " " + \
                               exit.name + "\n") 
                else:
                    file.write("keyexit #" + str(room[0]) + " #" + \
                               str(exit.destination.id) + " " + \
                               exit.name + "\n")
                    file.write("#" + str(exit.key.id) + " " + exit.message + \
                               " \n")
        file.close()         
                        
def load(fname):
    ''' Consumes a single file name in the form of a string.
        Builds the Python objects that are given in the text file consumed that 
        make up a world. That is, it creates a list of things in the world, 
        the player's room, the player itself, and all the exits. 
        Effects: reads in from a text file
        
        load: Str -> World
        requires: file uses specified format'''
    file = open(fname)  
    line = file.readline()
    lo_words = line.split()
    lo_things = []
    lo_thing_id = []
    lo_locations = []
    lo_rooms = []
    lo_room_id = []
    while lo_words[0] == "thing":
        thing_id = int(lo_words[1][1:])
        thing = Thing(thing_id)
        thing.name = " ".join(lo_words[2:])
        thing.description = file.readline()[:-1]
        lo_things += [thing]
        lo_thing_id += [thing_id]
        line = file.readline()
        lo_words = line.split()        
    while lo_words[0] == "room":
        room_id = int(lo_words[1][1:])
        room = Room(room_id)
        room.name = " ".join(lo_words[2:])
        room.description = file.readline()[:-1]
        room_contents_id = file.readline().split("#")[1:]
        room_contents = []
        for content_id in room_contents_id:
            room_contents += [lo_things[lo_thing_id.index(int(content_id))]]
        room.contents = room_contents
        lo_rooms.append(room)
        line = file.readline()
        lo_words = line.split()  
    for room in lo_rooms:
        lo_room_id += [room.id]    
    while lo_words != [] and lo_words[0] == "player":
        player_id = int(lo_words[1][1:])
        player = Player(player_id)
        player.name = " ".join(lo_words[2:])
        player.description = file.readline()[:-1]
        player_inventory_id = file.readline().split("#")[1:]
        player_inventory = []
        for inventory_id in player_inventory_id:
            player_inventory += \
                [lo_things[lo_thing_id.index(int(inventory_id))]]
        player.inventory = player_inventory
        player_location_id = int(file.readline()[:-1].split()[1][1:])
        player_location_index = lo_room_id.index(player_location_id)
        room = lo_rooms[player_location_index]
        player.location = room
        line = file.readline()
        lo_words = line.split()
    while lo_words != [] and \
          (lo_words[0] == "exit" or lo_words[0] == "keyexit"):
        if lo_words[0] == "exit":
            exit_name = lo_words[3]
            exit_id = int(lo_words[2][1:])
            exit_destination = lo_rooms[lo_room_id.index(exit_id)]
            exit = Exit(exit_name, exit_destination)
            exit_room_id = int(lo_words[1][1:])
            exit_room = lo_rooms[lo_room_id.index(exit_room_id)]
            exit_room.exits.append(exit)
        if lo_words[0] == "keyexit":
            exit_name = lo_words[3]
            exit_id = int(lo_words[2][1:])
            exit_destination = lo_rooms[lo_room_id.index(exit_id)]
            exit = Exit(exit_name, exit_destination)
            exit_room_id = int(lo_words[1][1:])
            exit_room = lo_rooms[lo_room_id.index(exit_room_id)]
            exit_room.exits.append(exit) 
            line = file.readline()
            low = line.split()
            exit.key = lo_things[lo_thing_id.index(int(low[0][1:]))]
            exit.message = " ".join(low[1:])
        line = file.readline()
        lo_words = line.split()    
    file.close()
    return World(lo_rooms, player)
    
def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)

testworld = makeTestWorld(False)
testworld_key = makeTestWorld(True)