__author__ = 'user'
global pirate_dest, dict_turn, occupied_dest,islands_pirates,types
from Pirates import *
import random,math
from random import shuffle
import math
global dict_list ,list_nodes,START_NODE_LOC,END_NODE_LOC,CELLS_HIGH,CELLS_WIDE
dict_list={}
list_nodes=[]
CELLS_HIGH=10#PirateGame.get_col_count()
CELLS_WIDE=10#PirateGame.get_row_count()
START_NODE_LOC=(0,0)
END_NODE_LOC=(0,0)
global stack_mode
global amout_campers
how_to_move=False
occupied_dest = []
types={}
dict_turn = {}
pirate_dest = {}

islands_pirates={}


def do_turn(game):
   
    initials(game)
    # Give orders to my drones
    handle_drones(game)
    
    # Give orders to my pirates
    handle_pirates(game)
    
    # Give orders to my decoy
    handle_decoy(game)


def initials(game):
    global pirate_dest,types,CELLS_WIDE,CELLS_HIGH
    global dict_turn, occupied_dest,islands_pirates
    global stack_mode
    global amout_campers
    occupied_dest = []
    CELLS_HIGH=game.get_row_count()-1
    CELLS_WIDE=game.get_col_count()-1
    dict_turn[game.get_turn()] = []
    islands_pirates={}
    
    for pirate in range(len(game.get_all_my_pirates())):
        pirate_dest[str(pirate)] = None
        types[pirate]=""
    # for i in game.get_my_living_pirates():
    #    dict_turn[game.get_turn()].append((i.location,i.id))
    for enemy in game.get_all_enemy_pirates():
        if not enemy.is_alive():
            dict_turn[game.get_turn()].append((-1, -1))
        else:
            dict_turn[game.get_turn()].append(enemy.location)
    #game.debug(str(dict_turn[game.get_turn()]))
    #attacker = get_closest_pirate_to_enemy_city(game)
    #enemy_threat_drones = Edrones_around_enemy_city(game, 26, game.get_enemy_cities()[0])
    try:
        cities=game.get_my_cities()+game.get_neutral_cities()
        islands=sorted(game.get_not_my_islands(),key=lambda x: cities[0].distance(x),reverse=True)
        for isl in islands:
            try:
                list_p=sorted(game.get_my_living_pirates(),key=lambda p:p.distance(isl))
                islands_pirates[isl]=[]
                for pirate in list_p:
    
                    islands_pirates[isl].append(pirate)
    
            except:
                game.debug("error")
        #game.debug("islands dest "+str(islands_pirates))
        '''if pirate_dest[str(pirate.id)]==None and (not pirate.id==attacker.id or len(enemy_threat_drones) > 0) :
                        pirate_dest[str(pirate.id)]=isl
                        break'''
    except:
        islands=[]
    #for i in types.keys():
    #    types[i]=""
def try_attack(pirate, game):
    
    for enemy in game.get_enemy_living_aircrafts():
         if pirate.in_attack_range(enemy):
            # Fire!
            game.attack(pirate, enemy)
            # Print a message

            # Did attack
            return True
    return False
    
def try_decoy(pirate, game):
    # Check if the player can decoy a pirate
    if (pirate.owner.turns_to_decoy_reload == 0 and (len(game.get_enemy_cities())!=0 or len(game.get_neutral_cities())>0))  :
        # Whoosh
        game.decoy(pirate)
        # print a message
        game.debug('pirate ' + str(pirate) + ' decoys itself')
        # Did decoy
        return True

    # Didnt decoy
    return False
    
    
def move(game,pirate,destination,**smartmove):

   
            
    
    sail_options = game.get_sail_options(pirate, destination)
    
    check=False
    if ('smartmove' in smartmove):
        sail_options = smart_move_pirate(game,destination, sail_options)
        check=True

    pirate_has_dest(pirate.id, destination)
    # Set sail!
    if destination==get_most_valuable_island(game) and len(game.get_neutral_cities())!=0 and len(game.get_all_islands())>=3 and pirate.distance(destination)>7 :
        if check :
            game.set_sail(pirate, sail_options[0])
        else:
            game.set_sail(pirate, sail_options[len(sail_options)-1])
    else:
        game.set_sail(pirate, sail_options[0])
    # Print a message
    #game.debug('pirate ' + str(pirate) + ' sails to ' + str(sail_options[0]))

def handle_decoy(game):
    decoy = game.get_myself().decoy
    game.debug("do we have a decoy: "+str(decoy))
    try:
        closest_enemy=sorted(game.get_enemy_living_pirates(),key=lambda x:x.distance(decoy))
    except:
        closest_enemy=[]
    if len(closest_enemy)!=0:
        if closest_enemy[0].distance(decoy)<15:
            destination = closest_enemy[0]
            #if  destination not in occupied_dest:
            #occupied_dest.appdeend(destination)
            move(game,decoy,destination)
            return
            
    # if we have a decoy
    try:
        closest_islands = sorted(game.get_not_my_islands(), key=lambda isl: decoy.distance(isl))
    except:
        closest_islands=[]
    lst1=closest_islands#game.get_enemy_living_pirates()
    if len(lst1)==0:
        if len(game.get_enemy_living_pirates())>0:
            lst1=game.get_enemy_cities()
        else:
            lst1=game.get_enemy_cities()
    
    dist_from=decoy
    if len(game.get_my_cities())>0:
        dist_from=game.get_my_cities()[0]
    if decoy:
        enemies=sorted(lst1,key=lambda x: x.distance(dist_from))
        for i in enemies:
            destination = i
            #if  destination not in occupied_dest:
            #occupied_dest.appdeend(destination)
            move(game,decoy,destination)
            break


def handle_pirates(game):
    global stack_mode
    global amout_campers
    decoyed_this_turn = False #decoy
    global pirate_dest,occupied_dest,types,islands_pirates
    try:
        cities_to_defend_or_attack=game.get_my_cities()
        if len(cities_to_defend_or_attack)==0:
            cities_to_defend_or_attack=game.get_neutral_cities()#game.get_enemy_cities()
            if len(cities_to_defend_or_attack)==0:
                cities_to_defend_or_attack=game.get_enemy_cities()
    except:
        cities_to_defend_or_attack=game.get_enemy_cities()
    try:
        enemy_threat_drones =game.get_enemy_living_drones()
    except:
        enemy_threat_drones=[]
    try:
        pirates=game.get_my_living_pirates()
        pirates.sort(key=lambda  x:x.distance(cities_to_defend_or_attack[0]))  #pirates.sort(key=lambda  x:x.distance(sorted(game.get_not_my_islands(),key=lambda isl: isl.distance(x))[0]))
    except:
        if len(game.get_my_living_pirates())==0:
            pirates=[]
        else:
            pirates=game.get_my_living_pirates()
    
    base_campers = []
    closest_piratesfrom_home = pirates
    closest_piratesfrom_enemy_home = pirates
    
    
    
    threat_drones_to_cities={}
    try:
        
        
        for city in (game.get_enemy_cities()+game.get_neutral_cities()):
            enemy_threat_drones = Edrones_around_enemy_city(game, 35, city)
            threat_drones_to_cities[city]=enemy_threat_drones
        """
        else:
            threat_drones_to_cities[] = Edrones_around_enemy_city(game, 35, game.get_enemy_cities()[0])
            enemy_threat_drones=sorted(enemy_threat_drones,key=lambda x:game.get_enemy_cities()[0].distance(x))
        """
        
    except:
        pass
    
    try:
        
        base_campers = get_enemylist_in_island_radius(game, cities_to_defend_or_attack[0],6)  # list of ships around our base(Can be empty)
    except:
        base_campers=[]
    amout_campers=len(base_campers)
    try:
        closest_piratesfrom_home = sorted(game.get_my_living_pirates(), key=lambda x: x.distance(game.get_my_cities()[0]))
    except:
        closest_piratesfrom_home = sorted(game.get_my_living_pirates(), key=lambda x: x.distance(cities_to_defend_or_attack[0]))
    try:
        closest_piratesfrom_enemy_home = sorted(game.get_my_living_pirates(), key=lambda x: x.distance(game.get_enemy_cities()[0]))
    except:
        closest_piratesfrom_enemy_home = sorted(game.get_my_living_pirates(), key=lambda x: x.distance(cities_to_defend_or_attack[0]))
    try:
        pirates_to_defend= sorted(game.get_my_living_pirates(), key=lambda x: x.distance(threat_drones_to_cities[0][0])+x.distance(closest_city_to_drone(True,enemy_threat_drones[0])[0]))
    except:
        pirates_to_defend=closest_piratesfrom_enemy_home
    
    #game.debug("campers: " + str(len(base_campers)))
    game.debug("All Dest:" + str(pirate_dest))
    try:
        closest_islands = sorted(game.get_not_my_islands(), key=lambda isl: pirate.distance(isl))
    except:
        closest_islands=[]

    #types are given here
    enemy_living_p=game.get_my_living_pirates()
    count_was_capture=0
    difference_islands=len(game.get_enemy_islands())-len(game.get_my_islands())
    count_defenders=1
    if game.get_my_score()-game.get_enemy_score()>=8  and difference_islands<=2:
        count_defenders=0
    #if game.get_max_drones_count()-5<=len(game.get_enemy_living_drones()):
    #    count_defenders=len(game.get_my_living_pirates())-1
    count_capturers=0
    count_attackers=0
    
    troll_map=False
    
    #count_capturers=len(game.get_not_my_islands())
    difference_islands=len(game.get_enemy_islands())-len(game.get_my_islands())
    if amout_campers>=2:
        stack_mode=True
    else:
     
        stack_mode=False
        
      
    
    if difference_islands>0:
        count_capturers=difference_islands+len(game.get_my_islands())
    if len(game.get_enemy_living_drones())==0:
        count_defenders=0
    #if len(game.get_enemy_living_drones())>12:
    #    count_defenders=2

    count1=0
    not_my_isl_num=len(game.get_not_my_islands())
    
    for p in pirates_to_defend:
        
        if p.id == closest_piratesfrom_home[0].id and len(base_campers) >0:
            types[p.id]="defend home"
            #continue
        
        if count1>=count_defenders  or (len(game.get_neutral_cities())!=0 and len(game.get_enemy_cities())>0) :
            
            continue
        count1+=1
        if (len(game.get_enemy_cities())<=2 or len(game.get_neutral_cities())!=0) and len(game.get_enemy_living_drones())>0 :
            types[p.id]="defender"
            continue
      
        #if count1==2:
        #    types[p.id]="attack drone"
        
        
    most_important_island=get_most_valuable_island(game)
    for isl in islands_pirates.keys():
        
        if isl not in occupied_dest:
            #if count>count_capturers:
            #    break
            for p in islands_pirates[isl]:
                
                if len(game.get_all_islands())>=len(game.get_all_my_pirates()) and game.get_enemy_score()==0 and game.get_my_score()==0 and game.get_turn()>40:#if p.distance(isl)<7 and game.get_turn()<5 and not len(game.get_my_living_pirates())>4:
                    troll_map=True
                if types[p.id]!="capture" and types[p.id]!="defender" and types[p.id]!="defend home":
                    if troll_map :
                        types[p.id]="capture most valuable"
                        break
                    
                    
                    elif isl==most_important_island and isl in game.get_not_my_islands() :
                        if p.distance(isl)<=10:
                            count_capturers+=1
                            types[p.id]= "capture most valuable"
                            break
                        else:
                            count_capturers+=1
                            types[p.id]="capture"
                            break
                    
                    count_capturers+=1
                    types[p.id]="capture"
                    
                    break
                
    try:
        
        pirates_to_check1=pirates
    except:
        pirates_to_check1=sorted(pirates,key=lambda x:x.distance(sorted(enemy_living_p,key=lambda p:p.distance(x))[0]))
    count_defenders=1
    count=0
    for i in pirates_to_check1:
        
        #game.debug("line nothing")
        if types[i.id]=="":
            #game.debug("dayumm")
            if not count_capturers>=not_my_isl_num:
                
                    types[i.id]="capture"
                    count_capturers+=1
            
            elif difference_islands>1:
                if not decoyed_this_turn and try_decoy(i, game):
                    game.debug("line 330")
                    decoyed_this_turn = True
                    types[i.id]="d"
                    continue
                types[i.id]="capture any"
            elif count_attackers>=len(enemy_living_p):
                types[i.id]="capture any near"
            elif difference_islands<-1: #we lead capturing
                types[i.id]="attack pirate any"
           
            elif difference_islands<0: #we lead capturing
                if not decoyed_this_turn and try_decoy(i, game):
                    game.debug("line 342")
                    decoyed_this_turn = True
                    types[i.id]="d"
                else:
                    if (len(game.get_enemy_cities())<=2 or len(game.get_neutral_cities())!=0) and len(game.get_enemy_living_drones())>0 and count<count_defenders :
                        
                        types[p.id]="defender"
                        count=count+1
                           
                    else:
                        types[i.id]="attack pirate any"
            
            elif count_capturers>=not_my_isl_num:
                
                
                
               
                if len(game.get_enemy_living_pirates())>=count_attackers+1: #need more attacker
                    count_attackers+=1
                    types[i.id]="attack pirate"
                else:
                    types[i.id]="attack drone"

            
            else:
                types[i.id]="attack drone"
    if len(game.get_my_cities())==0 and len(game.get_neutral_cities())==0: #if we do not have a city, dont capture
        for p in pirates:
            
           
            if types[p.id]=="capture" or types[p.id]=="capture any" or types[p.id]=="capture most valuable" or types[i.id]=="capture any near":
                types[p.id]="defender"
                
    #count_attackers=len(pirates)-count_defenders-count_capturers
    game.debug(str(types))
    pirate_to_run=game.get_my_living_pirates()
    if len(game.get_not_my_islands())>0:
        pirate_to_run=sorted(game.get_my_living_pirates(),key=lambda p: p.distance(closests_islands_from_pirate(game,p)[0]))
    #if game.get_enemy_score()<10:
    #    return
    for pirate in pirate_to_run:
       
        try:
            closest_islands = sorted(game.get_not_my_islands(), key=lambda isl: pirate.distance(isl))
        except:
            closest_islands=[]
        got_it=False
    
        if types[pirate.id]=="d":
            continue
        if try_attack(pirate,game):
          continue
       
        if types[pirate.id]=="capture":
           
            islands_to_sort=sorted(islands_pirates,key=lambda isl: isl.distance(islands_pirates[isl][0]))
            for isl in islands_to_sort:
                for p in islands_pirates[isl]:
                   
                    if isl not in occupied_dest and p.id==pirate.id :
                        destination=isl
                        #game.debug("zabidoge")
                        move(game,pirate,destination)
                        got_it=True
                    break
                if got_it:
                    break
            if len(closest_islands)>0 and not got_it:
                #game.debug(str(closest_islands))
                for i in closest_islands:
                    if i not in occupied_dest:
                        destination=i
                        #occupied_dest.append(destination)
                        move(game,pirate,destination)
                        got_it=True
                        break
                if not got_it:
                    isl_with_enemies=closest_islands
                    isl_with_enemies.sort(key=lambda isl: len(count_enemies_in_range(game, isl, 8))+isl.distance(pirate),reverse=True)
                    #move(game,pirate,isl_with_enemies[0])
                    move(game,pirate,closests_islands_from_pirate(game,pirate)[0])
            elif not got_it:
                types[pirate.id]="attack pirate"
        elif types[pirate.id]=="capture any":
            
            
            for i in closest_islands:
                    #if i not in occupied_dest
                   
                    destination=i
                    #occupied_dest.append(destination)
                    move(game,pirate,destination)
                    got_it=True
                    break      
        elif types[pirate.id]=="capture any near":
           
            
            for i in sorted(closest_islands,key=lambda isl:isl.distance(sorted(game.get_my_cities(),key=lambda city:city.distance(isl))[0])):
                    #if i not in occupied_dest:
                    destination=i
                    #occupied_dest.append(destination)
                    move(game,pirate,destination)
                    got_it=True
                    break
                
        elif types[pirate.id]=="capture most valuable":   
            destination=get_most_valuable_island(game)
            if destination==None:
                x=sorted(game.get_all_islands(),key=lambda x:x.distance(pirate))
                destination=x[0]
           
            move(game,pirate,destination)
            got_it=True
        elif types[pirate.id]=="attack pirate any":
            
            enemies=sorted(game.get_enemy_living_pirates(),key=lambda x: x.distance(pirate))
            if pirate.distance(enemies[0])<10:
                if not decoyed_this_turn and try_decoy(pirate, game) :
                    game.debug("line 454")
                    decoyed_this_turn = True
                    continue
                
            for i in enemies:
                destination = i
                #if  destination not in occupied_dest:
                if i.location!=i.initial_location:
                    occupied_dest.append(destination)
                    move(game,pirate,destination)
                    break
            continue
        if types[pirate.id]=="defender":
            
            for city in threat_drones_to_cities.keys():
               
                if len(threat_drones_to_cities[city])!=0:
                   
                    for i in threat_drones_to_cities[city]:
                        destination = i
                        if  destination not in occupied_dest:
                            occupied_dest.append(destination)
                            move(game,pirate,destination)
                            break
                    break
        if types[pirate.id]=="attack drone":
            drones=sorted(enemy_threat_drones,key=lambda x: x.distance(pirate))
            
            for i in drones:
                destination = i
                if  destination not in occupied_dest:
                    occupied_dest.append(destination)
                    move(game,pirate,destination)
                    break
        if types[pirate.id]=="attack pirate":
           
            enemies=sorted(game.get_enemy_living_pirates(),key=lambda x: x.distance(pirate))
            if pirate.distance(enemies[0])<10:
                if not decoyed_this_turn and try_decoy(pirate, game):
                    game.debug("line 493")
                    decoyed_this_turn = True
                    continue
            for i in enemies:
                destination = i
                if  destination not in occupied_dest:
                    occupied_dest.append(destination)
                    move(game,pirate,destination)
                    break
            continue
       
        if types[pirate.id]=="defend home":
            if len(game.get_my_cities())>0:
                move(game,pirate,game.get_my_cities()[0],smartmove= 'YES')
            else:
                if len(game.get_neutral_cities())>0:
                    move(game,pirate,game.get_neutral_cities()[0],smartmove= 'YES')
 
            continue
def handle_drones(game):
    global list_nodes,START_NODE_LOC,END_NODE_LOC,CELLS_HIGH,CELLS_WIDE
    count = 0
    cities=[]
    global stack_mode
    global amout_campers
    # Go over all of my drones
    
    count_d=0
    """
    try:
        if len(game.get_all_islands)>=4:
            all_islands_by_rows=sorted(game.get_my_islands(),key=lambda x:x.location.row)
            top_island=all_islands_by_rows[0]
            buttom_island=all_islands_by_rows[len(all_islands_by_rows)-1]
        else:
            top_island=game.get_all_islands()[0]
            buttom_island=game.get_all_islands()[len(game.get_all_islands())-1]
    except:
        top_island=game.get_all_islands()[0]
        buttom_island=game.get_all_islands()[len(game.get_all_islands())-1]
    """
   
    #for drone in sorted(game.get_my_living_drones(),key=lambda x:x.distance(closest_city_to_drone(game,False,x)[0])):
   
    my_most_important_city=sorted(game.get_my_cities()+game.get_neutral_cities(),key= lambda city:city.value_multiplier,reverse=True)
    for drone in game.get_my_living_drones():
        count_d+=1
        amount_drones_in_range=get_drones_in_my_range_for_Stacking(game,drone)
        cities=sorted(game.get_my_cities()+game.get_neutral_cities(),key=lambda x:x.distance(drone)) #closest city
        
        
        if stack_mode:
            amount_drones_in_range=get_drones_in_my_range_for_Stacking(game,drone)
            if (amount_drones_in_range<5*amout_campers or amount_drones_in_range==game.get_max_drones_count() or len(game.get_my_living_drones())==game.get_max_drones_count())and drone.location==drone.initial_location:
                continue
    
    
    
        islands =sorted(game.get_neutral_cities(),key=lambda x:x.distance(drone))
        # Choose a destination
        if len(islands)==0:
            destination = cities[0]
        else:
           
            
            destination=islands[0]
            
            if (drone.distance(cities[0])+5<=drone.distance(destination) or (len(count_enemies_in_range(game,cities[0],10))<=1) and drone.distance(cities[0])-2<=drone.distance(destination) and game.get_col_count()<50) :
                destination=cities[0]
            
            if len(count_enemies_in_range(game,cities[0],10))>1:
                destination=islands[0]
                
           
        # Get sail options
        sail_options = game.get_sail_options(drone, destination)
        

       
        #random.shuffle((sail_options)
        # Set sail!
        #if stack_mode or amount_drones_in_range>amout_campers*2:
        #    game.set_sail(drone, sail_options[0])
        
        """elif count_d==1 and drone.distance(cities[0])<=10:
            START_NODE_LOC=drone.get_location()
            END_NODE_LOC=cities[0].get_location()

            for j in range(CELLS_HIGH):
                for i in range(CELLS_WIDE):
                    list_nodes.append(Node(j,i,game))#(Node(count%CELLS_WIDE,count/CELLS_WIDE))
            
            start=list_nodes[CELLS_WIDE*START_NODE_LOC.row+START_NODE_LOC.col]
            end=list_nodes[CELLS_WIDE*END_NODE_LOC.row+END_NODE_LOC.col]
            game.set_sail(drone,a_star(start,end,game)[0].GetPlace())
            game.debug("a *")
            continue"""
        
        if not stack_mode  or amount_drones_in_range<=amout_campers and drone.distance(my_most_important_city[0])>10 and drone.distance(destination)<game.get_attack_range() :
            x=game.get_drone_max_speed()
            down=Location(drone.location.row+x,drone.location.col)
            up=Location(drone.location.row-x,drone.location.col)
            left=Location(drone.location.row,drone.location.col-x)
            right=Location(drone.location.row,drone.location.col+x)
            loc=destination.get_location()
            my_loc=drone.get_location()
            
            
            
            """
            if drone.initial_location==top_island.location or drone.initial_location==buttom_island.location:
                if loc.col>=my_loc.col:
                    sail_options=[right,left,up,down]
                else:
                    sail_options=[left,right,down,up]
            """
            if loc.col<=my_loc.col:
                left_side=True
                right_side=False
            else:
                left_side=False
                right_side=True
                
                
            if loc.row<my_loc.row:
                down_side=True
                up_side=False
            elif loc.row>my_loc.row:
                down_side=False
                up_side=True
            else:
                down_side=False
                up_side=False
            
            
                                
            if str(game.get_opponent_name())==str(12109):
                if loc.col>=my_loc.col:
                        sail_options=[right,left,up,down]
                else:
                    sail_options=[left,right,down,up]
                """
                elif drone.distance(drone.initial_location)<5:
                enemy_pirate_locations=sorted(game.get_enemy_living_pirates(),key=lambda x:x.distance(drone))
                count_vertical=0
                count_side=0
               
                #now we count count_side
                for enemy in enemy_pirate_locations:
                    if abs(drone.location.col-my_loc.col)>abs(drone.location.col-my_loc.col):
                        if right_side and not down_side:
                            if enemy.location.row <=drone.location.row :
                               count_side+=1
                            else:
                                count_vertical+=1
                        else:
                            if enemy.location.row <=drone.location.row :
                               count_vertical+=1
                            else:
                                count_side+=1
                    else:
                        if right_side and not down_side:
                            if enemy.location.row <=drone.location.row :
                               count_side+=1
                            else:
                                count_vertical+=1
                        else:
                            if enemy.location.row <=drone.location.row :
                               count_vertical+=1
                            else:
                                count_side+=1
                if count_side>count_vertical:
                    if down_side:
                        sail_options=[up,down,left,right]
                    else:
                        sail_options=[down,up,left,right]
                else:
                    if right_side:
                        sail_options=[left,down,right,up]
                    else:
                        sail_options=[right,up,left,right]
                """   
            elif down_side:
                    if left_side:
                        """if abs(loc.col-my_loc.col)>abs(loc.row-my_loc.row):
                            sail_options=[right,up,down,left]
                        else:
                            sail_options=[up,right,down,left]
                        else:"""
                        sail_options=[up,left,right,down]
                    else:
                        sail_options=[up,right,left,down]
            elif up:
                    """if abs(loc.col-my_loc.col)>abs(loc.row-my_loc.row):
                        if loc.col>my_loc.col:
                            sail_options=[right,down,left,up]"""
                        #sail_options=[up,right,down,left]
                    if  left_side:
                         sail_options=[down,left,right,up]
                    else:
                        sail_options=[down,right,left,up]
            else:
                    
                    if right_side:
                        sail_options=[left,right,up,down]
                    else:
                        sail_options=[right,left,down,up]
                            
                    #sail_options=[Location(drone.location.row+1,drone.location.col),Location(drone.location.row-1,drone.location.col),Location(drone.location.row,drone.location.col+1),Location(drone.location.row,drone.location.col-1)]
            game.set_sail(drone, smart_move(game,sail_options,drone,destination))

        else:
            game.set_sail(drone, sail_options[0])

            
def list_my_closest_pirates_from_location(game, location):
    dest=[]
    if game.get_my_living_pirates():
        dest =sorted(game.get_my_living_pirates(), key=lambda x: location.distance(x))
        return dest
    return dest


def closests_islands_from_pirate(game,pirate):
    list1=[]
    if len(game.get_not_my_islands())>0:
    
        list1= sorted(game.get_not_my_islands(),key=lambda x: x.distance(pirate))
    return list1
    

def count_turns_enemy_were_in_radius(game, pirate, loc, radius, max1):
    global dict_turn
    max2 = max1
    try:
        """enemy_id = pirate.id
        enemies_in_range = count_enemies_in_range(game, loc, radius)
        if pirate in enemies_in_range:"""
        for i in range(1, max2):
            new_loc = dict_turn[game.get_turn() - i][pirate.id]
            #game.debug(new_loc)
            # if new_loc == Location(-1, -1):  # dead
            #    return i
            if not loc.distance(Location(new_loc.row, new_loc.col)) <= radius:
                return i
    except:
        game.debug("error homebase")
        return 0
    return max2  # max
        
def get_most_valuable_island(game):
    try:
        my_most_important_city=sorted(game.get_my_cities()+game.get_neutral_cities(),key= lambda city:city.value_multiplier,reverse=True)
        
        most_important_island_by_drone_creation=sorted(game.get_all_islands(),key=lambda x:x.turns_to_drone_creation)
        
       
     
        """
        are_all_the_Same_in_drone_creationg=False
        for isl in most_important_island_by_drone_creation:
            if isl!=most_important_island_by_drone_creation[0]:
                if isl.turns_to_drone_creation==most_important_island_by_drone_creation[0].turns_to_drone_creation:
                    are_all_the_Same_in_drone_creationg=True
                    break
        """
        if len(game.get_neutral_cities())!=0:
            islands_by_distance_from_city=sorted(game.get_all_islands(),key=lambda x:x.distance(game.get_neutral_cities()[0]))
            return islands_by_distance_from_city[0]
            
        else:
            islands_by_distance_from_city=sorted(game.get_all_islands(),key=lambda x:x.distance(game.my_most_important_city()[0]))
            
        if most_important_island_by_drone_creation[0] in game.get_my_islands():
            if len(islands_by_distance_from_city)==0:
                return None
            if islands_by_distance_from_city[0] in game.get_my_islands():
                return islands_by_distance_from_city[len(islands_by_distance_from_city)-1]
            else:
                
                return islands_by_distance_from_city[0]
        else:
            return most_important_island_by_drone_creation[0]
        
       
        
        
    except:
        
        return None

def get_enemylist_in_island_radius(game, island, radius):
    # Return a list with pirates around island (or city) within certain radius
    global dict_turn

    enemy_around_island = []
    for pirate in game.get_enemy_living_pirates():
        if pirate.distance(island) <= radius:
            if count_turns_enemy_were_in_radius(game, pirate, island, radius, 6) > 5:
                enemy_around_island.append(pirate.id)

    #game.debug("Found: " + str(len(enemy_around_island)) + " Enemy Around: " + str(island))
    return enemy_around_island



def get_drones_in_my_range_for_Stacking(game,drone):
    #how many drones in my drone range
    count=0
    for d in game.get_my_living_drones():
        if d!=drone:
            if drone.distance(d)<5 :
                count+=1
        else:
            continue
    return count
    

def pirate_has_dest(pirate_id, dest):
    global pirate_dest,occupied_dest
    pirate_dest[str(pirate_id)] = dest
    occupied_dest.append(dest)


def pirate_reaced_dest(game, pirate, dest):
    global pirate_dest, occupied_dest


    # game.debug("Pirate num:" +str(pirate.id)+" in:"+str(pirate.location)+" try to get: "+str(dest))
    for island in game.get_all_islands():


        if dest.location==island.location and ilsand.in_control_range(pirate):
            #Sail only to the start of the island - not all the way to the center
            pirate_dest[str(pirate.id)] = None

            occupied_dest.remove(dest)
            game.debug("Pirate in island control")
            return True

    if pirate.location == dest.location:
        pirate_dest[str(pirate.id)] = None
        game.debug("Pirate Reached")
        """occupied2=occupied_dest
        for i in occupied_dest:
            if i.location==dest.location:
                continue
            occupied2.append(i)
        occupied_dest=occupied2"""
        occupied_dest.remove(dest)
        return True
    return False


def Edrones_around_enemy_city(game, radius, island):
    Edrones_around_islands = []
    for drone in game.get_enemy_living_drones():
        if drone.distance(island) <= radius:
            Edrones_around_islands.append(drone)

    game.debug("Found: " + str(len(Edrones_around_islands)) + " Drone Around: " + str(island))
    return sorted(Edrones_around_islands, key=lambda drone: drone.distance(island))#closest_city_to_drone(True,drone)))
    
def my_drones_in_range(game,radius,loc):
    my_drones =[]
    for drone in game.get_my_living_drones():
        if drone.distance(loc) <= radius:
            my_drones.append(drone)
    
    return sorted(my_drones, key=lambda drone: drone.distance(loc))


def count_enemies_in_range(game, location, radius):
    enemies = []
    for enemy in game.get_enemy_living_pirates():
        if enemy.distance(location) <= radius:
            enemies.append(enemy)
    if enemies!=[]:
        return sorted(enemies,key=lambda x:x.distance(location))
    return []
def check_in_map(game,loc):
    if loc.row >=game.get_row_count() or loc.col>=game.get_col_count():
        return False
    return True

def smart_move(game,sail_op,drone,dest):
    #Pirate can be a drone!!!
    options = sail_op#sail_options
    
    threat_level = {0:[],1:[],2:[],3:[]}

    for path in options:
        if not check_in_map(game,path):
            continue
        e_in_range = count_enemies_in_range(game, path, game.get_attack_range())
        count = len(e_in_range)
        if not e_in_range :
            threat_level[0].append(path)#0 means Best way

        else:
            if count ==1:
                threat_level[1].append(path)
            if count > 1:
                threat_level[2].append(path)


    cities=sorted(game.get_my_cities()+game.get_neutral_cities(),key=lambda x:x.distance(drone)) #closest city

    for i in range(4):
        if len(threat_level[i])>0:
            return sorted(threat_level[i],key=lambda x:x.distance(dest))[0]
            #return the lowest threat level option
def closest_city_to_drone(game,enemy,drone):
    try:
        if enemy:
            return sorted(game.get_enemy_cities()+game.get_neutral_cities(),key=lambda c:c.distance(drone))
        return sorted(game.get_my_cities()+game.get_neutral_cities(),key=lambda c:c.distance(drone))
    except:
        game.debug("error closest city")
        return None

def smart_move_pirate(game, dest,sail_op):
    options = sail_op#sail_options
    threat_level = {0:[],1:[],2:[],3:[]}
    
    for path in options:
        if not check_in_map(game,path):
            continue
        e_in_range = count_enemies_in_range(game, path, game.get_attack_range())
        count = len(e_in_range)
        if not e_in_range :
            threat_level[0].append(path)#0 means Best way

        else:
            if count ==1:
                threat_level[1].append(path)
            if count > 1:
                threat_level[2].append(path)



    for i in range(4):
        if len(threat_level[i])>0:
            return sorted(threat_level[i],key=lambda x:x.distance(dest))
            #return the lowest threat level option
            
class Node(object):
    
    x=0
    y=0
    g=0
    f=0
    h=0
    came_from=None
    neighbors=[]
    def __init__(self,x,y,game):
        self.neighbors=[]
        self.x=x
        self.y=y
        self.game=game
        self.g=1000
        
        if Location(x,y)==START_NODE_LOC or Location(x,y)==END_NODE_LOC:
            self.g=0
        self.h=math.sqrt(((END_NODE_LOC.row-self.x))**2+((END_NODE_LOC.col-self.y)**2))
        self.f=self.h+(self.g)
        self.came_from=None
    def GetPlace(self):
        return Location(self.x,self.y)
    def set_came_from(self,node):
        self.came_from=node
        self.g=math.sqrt(((node.x-self.x))**2+((node.y-self.y)**2))+node.g
        count_en=count_enemies_in_range(self.game,Location(self.x,self.y),5)
        if len(count_en)>0:
            self.g+=100*count_en[0].distance(self.GetPlace())
        self.f=self.h+(self.g)
        #self.game.debug("set came from")
        
        return True
    def __str__(self):
        return str((self.x,self.y))
    def get_came_from(self):
        return self.came_from
    def __lt__(self, other):
        return self.f<other.f
    def GetNeighbors(self):
        global list_nodes
        self.neighbors=[]
        y1=self.x #flipped because accidently i switched x with y
        x1=self.y
        if self.y>0:
            self.neighbors.append( list_nodes[y1*CELLS_WIDE+(x1-1)])

        if self.y>0:
            self.neighbors.append(list_nodes[(y1-1)*CELLS_WIDE+(x1)])

        if self.x<CELLS_HIGH-1:
            self.neighbors.append(list_nodes[(y1+1)*CELLS_WIDE+(x1)])
        if self.y<CELLS_WIDE-1:
            self.neighbors.append(list_nodes[(y1)*CELLS_WIDE+(x1+1)])
        return self.neighbors

def a_star(start,end,game):
    OpenSet=[start]
    ClosedSet=[]
    enemy_in_range=0
    while len(OpenSet)>0:
        current=OpenSet[0]

        if current==end:
            return path(current,start,game)

        OpenSet.remove(current)
        ClosedSet.append(current)
        current.GetNeighbors()
        #game.debug(current)
        for i in current.neighbors:
            #enemy_in_range=len(count_enemies_in_range(game,Location(i.y,i.x),5))
            
            if ClosedSet.__contains__(i)==True:
                continue


            elif OpenSet.__contains__(i)==False:

                if i.GetPlace()!=START_NODE_LOC:# and i.came_from==None:
                    
                    i.set_came_from(current)
                    #Arr2D[i.x][i.y]=[(200,100,20),1,1]
                insort_left(OpenSet,i)#OpenSet.insert(bisect.bisect_left(OpenSet,i),i) #insert to a sorted list --by f_score(lower)
            elif OpenSet.__contains__(i)==True :
                if i.GetPlace()!=START_NODE_LOC:# and i.came_from==None:
                    if i.g>(current.g+math.sqrt(((current.x-i.x))**2+((current.y-i.y)**2))):
                        OpenSet.remove(i)
                        i.set_came_from(current)
                        insort_left(OpenSet,i)#OpenSet.insert(bisect.bisect_left(OpenSet,i),i) #insert to a sorted list --by f_score(lower)
                    #Arr2D[i.x][i.y]=[(200,100,20),1,1]
    return []
def path(current,first,game):
    total_path=[current]
    
    while current!=first:
        print current
        total_path.insert(0,current)

        current=current.came_from
    game.debug(str(total_path[0]))
    return total_path
def insort_left(a, x, lo=0, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the left of the leftmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] < x: lo = mid+1
        else: hi = mid
    a.insert(lo, x)