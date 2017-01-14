global pirate_dest

pirate_dest = {}
for pirate in range(5):
    pirate_dest[str(pirate)] = None


def do_turn(game):
    initials(game)
    # Give orders to my pirates
    handle_pirates(game)
    # Give orders to my drones
    handle_drones(game)

def initials(game):
    global pirate_dest
    pass

    

def handle_drones(game):
    
    count =0
   # Go over all of my drones
    for drone in game.get_my_living_drones():
        
        
        count+=1
        if count < 1:
            
            continue
        # Choose a destination
        destination = get_closest_friendly_city(game,drone)
        # Get sail options
        sail_options = game.get_sail_options(drone, destination)
        # Set sail!
        game.set_sail(drone, sail_options[0])

def handle_pirates(game):
    global pirate_dest
    change_dest = False
    
    enemy_threat_drones = Edrones_around_enemy_city(game,11,game.get_enemy_cities()[0])
    base_campers = get_enemylist_in_island_radius(game,game.get_my_cities()[0],5)#list of ships around our base(Can be empty)
    game.debug("campers: "+str(len(base_campers)))
    # Go over all of my pirates
    for pirate in game.get_my_living_pirates():
        
        
        if len(base_campers)!=0:
            change_dest = True
            
        if len( enemy_threat_drones)!=0:
            change_dest=True
        game.debug("All Dest:"+str(pirate_dest))
        if pirate_dest[str(pirate.id)] !=None and change_dest == False:
            #Check if current pirate got a destination, and if he reached it
            if not try_attack(pirate,game):
            
                destination = pirate_dest[str(pirate.id)]
                
                sail_options = game.get_sail_options(pirate, destination)
                
                game.set_sail(pirate, sail_options[0])
                
                
                change_dest  = pirate_reaced_dest(game,pirate,destination)
                #If pirate reached his dest, change it
            continue
                
            
            
        
        # Try to attack, if you didnt - move to a island
        if not try_attack(pirate, game):
            # Choose destination
            destination = game.get_my_cities()[0]
            

            if len ( enemy_threat_drones)>1 and pirate.id ==get_closest_pirate_to_enemy_city(game).id :

                
                destination = enemy_threat_drones[0]

            elif len(base_campers)!=0 and pirate.id in base_campers:
                

                destination = game.get_my_cities()[0]
                
            elif get_closest_neutral_island(game,pirate) != None:
                
                destination = get_closest_neutral_island(game,pirate)
            
            elif get_closest_enemy_island(game,pirate)!=None:

                destination=get_closest_enemy_island(game,pirate)
                
                '''
            elif get_closest_enemy_drone(game,pirate) != None:
                    destination = get_closest_enemy_drone(game,pirate)                
            elif get_closest_neutral_island(game,pirate) != None:
                destination = get_closest_neutral_island(game,pirate)
        

                    
            elif game.get_my_living_drones():
                destination = get_closest_friendly_drone(game,pirate)
            elif game.get_enemy_living_pirates():
                destination = get_closest_enemy_pirate(game,pirate)
                '''
            # Get sail options
            

            sail_options = game.get_sail_options(pirate, destination)
            
            pirate_has_dest(pirate.id,destination)
            # Set sail!
            game.set_sail(pirate, sail_options[0])
            # Print a message
            game.debug('pirate ' + str(pirate) + ' sails to ' + str(sail_options[0]))
    
def try_attack(pirate, game):
    # Go over all enemies
    for enemy in game.get_enemy_living_aircrafts():
        # Check if the enemy is in attack range
        if pirate.in_attack_range(enemy):
            # Fire!
            game.attack(pirate, enemy)
            # Print a message

            # Did attack
            return True

    # Didnt attack
    return False
    
def get_closest_neutral_island(game, pirate):
    #Initial distance
    dist = 9999
    
    #If there are no neutral islands, return none
    if(not game.get_neutral_islands()):
        return None
        
    #Initial with the first neutral island
    isl = game.get_neutral_islands()[0]
    
    #Iterate through the neutral islands
    for island in game.get_neutral_islands():
        #Check if the distance is smaller than the initial distance
        if pirate.distance(island) < dist:
            #Set the new island and distance
            dist = pirate.distance(island)
            isl = island
    #Return the one found
    return isl
    
def get_closest_enemy_island(game,pirate):
    #Initial distance
    dist = 9999
    #If there are no enemy islands, return none
    if(not game.get_enemy_islands()):
        return None
    #Initial with the first enemy island
    isl = game.get_enemy_islands()[0]
    for island in game.get_enemy_islands():
        #Check if the distance is smaller than the initial distance
        if pirate.distance(island) < dist :
            
            #Set the new island and distance
            dist = pirate.distance(island)
            isl = island
    game.debug("get closest enemy island "+ str(isl))
    return isl
    
def get_closest_enemy_city(game,pirate):
    #Initial distance
    dist = 9999
    #If there are no neutral cities, return none
    if(not game.get_enemy_cities()):
        return None
    #Initial with the first enemy cities
    city = game.get_enemy_cities()[0]
    for cit in game.get_enemy_cities():
        #Check if the distance is smaller than the initial distance
        if pirate.distance(cit) < dist:
            #Set the new island and distance
            dist = pirate.distance(cit)
            city = cit
    return city
    
def get_closest_friendly_city(game,pirate):
    #Initial distance
    dist = 9999
    #If there are no cities in my hand, return none
    if(not game.get_my_cities()):
        return None
    #Initial with the first home city
    city = game.get_my_cities()[0]
    for cit in game.get_my_cities():
        #Check if the distance is smaller than the initial distance
        if pirate.distance(cit) < dist:
            #Set the new island and distance
            dist = pirate.distance(cit)
            city = cit
    return city
    
def get_closest_enemy_drone(game,pirate):
    #Initial distance
    dist = 9999
    #If there are no neutral cities, return none
    if(not game.get_enemy_living_drones()):
        return None
    #Initial with the first enemy living drone
    drone = game.get_enemy_living_drones()[0]
    for drn in game.get_enemy_living_drones():
        if pirate.distance(drn) < dist:
            #Set the new island and distance
            dist = pirate.distance(drn)
            drone = drn
    return drone
    
def get_closest_friendly_drone(game,pirate):
    #Initial distance
    dist = 9999
    #If there are no living drones, return none
    if(not game.get_my_living_drones()):
        return None
    #Initial with the first friendly living drone
    drone = game.get_my_living_drones()[0]
    for drn in game.get_my_living_drones():
        #Check if the distance is smaller than the initial distance
        if pirate.distance(drn) < dist:
            #Set the new island and distance
            dist = pirate.distance(drn)
            drone = drn
    return drone
    
def get_closest_enemy_pirate(game,pirate):
    #Initial distance
    dist = 9999
    #If there are no enemy living pirates, return none
    if(not game.get_enemy_living_pirates()):
        return None
    #Initial with the first enemy living pirate
    enpirate = game.get_enemy_living_pirates()[0]
    for prt in game.get_enemy_living_pirates():
        #Check if the distance is smaller than the initial distance
        if pirate.distance(prt) < dist:
            #Set the new island and distance
            dist = pirate.distance(prt)
            enpirate = prt
    return enpirate
    
def get_closest_pirate_to_enemy(game,enemy_pirate):
    #Initial distance
    dist = 9999
    #If there are no living pirates, return none
    if(not game.get_my_living_pirates()):
        return None
    #Initial with the first frinedly living pirate
    clpirate = game.get_my_living_pirates()[0]
    for prt in game.get_my_living_pirates():
        #Check if the distance is smaller than the initial distance
        if enemy_pirate.distance(prt) < dist:
            #Set the new island and distance
            dist = enemy_pirate.distance(prt)
            clpirate = prt
    return clpirate
    
def get_closest_pirate_to_city(game):
    
        #Initial distance
    dist = 9999
    #If there are no neutral cities, return none
    if(not game.get_my_living_pirates()):
        return None
    #Initial with the first enemy living drone
    city = game.get_my_cities()[0]
    prt = game.get_my_living_pirates()[0]
    for pirate in game.get_my_living_pirates():
        if pirate.distance(city) < dist:
            #Set the new island and distance
            dist = pirate.distance(city)
            prt = pirate
    game.debug("Closest pirate to my city: "+str(prt))
    return prt
    
def get_closest_pirate_to_enemy_city(game):
    
        #Initial distance
    dist = 9999
    #If there are no neutral cities, return none
    if(not game.get_my_living_pirates()):
        return None
    #Initial with the first enemy living drone
    city = game.get_enemy_cities()[0]
    prt = game.get_my_living_pirates()[0]
    for pirate in game.get_my_living_pirates():
        if pirate.distance(city) < dist:
            #Set the new island and distance
            dist = pirate.distance(city)
            prt = pirate
    game.debug("Closest pirate to enemy city: "+str(prt))
    return prt
    
    
    
def get_enemylist_in_island_radius(game,island,radius):
    #Return a list with pirates around island (or city) within certain radius
    enemy_around_island = []
    for pirate in game.get_enemy_living_pirates():
        if pirate.distance(island) <= radius:
            enemy_around_island.append(pirate.id)
            
    game.debug("Found: "+str(len(enemy_around_island))+" Enemy Around: "+str(island))
    return enemy_around_island
    
    
def pirate_has_dest(pirate_id,dest):
    global pirate_dest
    pirate_dest[str(pirate_id)]=dest
    
def pirate_reaced_dest(game,pirate,dest):
    global pirate_dest
    #game.debug("Pirate num:" +str(pirate.id)+" in:"+str(pirate.location)+" try to get: "+str(dest))
    if pirate.location == dest.location:
        pirate_dest[str(pirate.id)] = None
        game.debug("Pirate Reached")
        return True
    return False
    
def Edrones_around_enemy_city(game,radius,island):
    
    Edrones_around_islands= []
    for drone in game.get_enemy_living_drones():
        if drone.distance(island) <= radius:
            Edrones_around_islands.append(drone)
            
    game.debug("Found: "+str(len( Edrones_around_islands))+" Drone Around: "+str(island))
    return  Edrones_around_islands
    
    
    