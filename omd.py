import numpy as np
from collections import Counter
from copy import copy
import time


def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'yes': True, 'no': False}
    while option not in options:
        print('Choose: {}/{}'.format(*options))
        option = input()
    
    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()

def step2_umbrella():
    options = ['cats', 'dogs']
    option = ''
    moral = 0
    company = Counter()
    while option.lower().strip() not in options:
        print('is it raining cats or dogs?')
        option = input()
    rains = np.random.randint(2)
    if rains:
        print("It's raining!")
        print(f"But {option} are jumping back up off the duck's umbrella straight into the sky..")
        moral += 1
    else:
        print("There's no rain and duck feels really stupid carrying that damn umbrella..")
        moral += -1
    
    step3_bar(moral, company)
   

def step2_no_umbrella():
    options = ['cats', 'dogs']
    option = ''
    moral = 0
    company = Counter()
    while option.lower().strip() not in options:
        print('Is it raining cats or dogs?')
        option = input()
    rains = np.random.randint(2)

    if rains:
        print(f"Whoa! there are {option} falling off from the sky!")
        print("Try to catch them all!")
        company = play_catch(who = option[:-1], rounds = 3)
        moral += len(company)
    else:
        print("There's no rain and duck feels really nice, not plodding along with heavy umbrella..")
        moral += 1
    
    step3_bar(moral, company)

def play_catch(who = 'dog', rounds = 1):

    if who == 'dog':
        F = '\N{DOG}'
    elif who == 'cat':
        F = '\N{TIGER}'
    else:
        raise ValueError('Unknown option')

    WIDTH = 5
    HEIGHT = 4
    
    S = '\N{DROPLET}'
    G = '\N{PALM TREE}'
    D = '\N{DUCK}'
    E = '\N{COLLISION SYMBOL}'
    
    S = '{symbol: ^{width}}'.format(symbol = S, width = 5)
    G = '{symbol: ^{width}}'.format(symbol = G, width = 5)
    D = '{symbol: ^{width}}'.format(symbol = D, width = 3)
    F = '{symbol: ^{width}}'.format(symbol = F, width = 3)
    E = '{symbol: ^{width}}'.format(symbol = E, width = 3)
    
    blue_sky = [S]*WIDTH
    ground = [G]*WIDTH
    
    options = {'left': -1, 'l':-1, 
               'right': 1, 'r': 1,
               'still':0, 's':0
               }
    
    catches = Counter()
    
    ground_init_pos = np.random.randint(WIDTH)
    ground_pos = ground_init_pos
  
    ground_row = ground[:ground_pos] + [D] + ground[ground_pos+1:]
    print('Move {} ({}) or {} ({}) or {} ({}) to catch!'.format(*options))
    
    for _ in range(rounds):
        top_init_pos = np.random.randint(WIDTH)
        falling_row = blue_sky[:top_init_pos] + [F] + blue_sky[top_init_pos+1:]
        
        for i in range(HEIGHT-1):
            scene = ['{s: ^{width}}'.format(s = ''.join(blue_sky), width = 40) for _ in range(HEIGHT - 1)]
            scene[i] = '{s: ^{width}}'.format(s = ''.join(falling_row), width = 40)
            scene = '\n'.join(scene +  ['{s: ^{width}}'.format(s = ''.join(ground_row), width = 38)])
            print(scene)
            option = ''
        
            while option.lower().strip() not in options:
                option = input()
            ground_pos = max(0,min(WIDTH-1, ground_pos + options[option]))
            ground_row = ground[:ground_pos] + [D] + ground[ground_pos+1:]
        
        if ground_pos == top_init_pos:
            scene = ['{s: ^{width}}'.format(s = ''.join(blue_sky), width = 40) for _ in range(HEIGHT - 1)]
            ground_row = copy(ground)
            ground_row[ground_pos] = E
            scene = '\n'.join(scene +  ['{s: ^{width}}'.format(s = ''.join(ground_row), width = 38)])
            print(scene)  
            print("It's a catch: + 1 more buddy to take to the pub!")
            catches[who] += 1
            ground_row[ground_pos] = D
        else:
            scene = ['{s: ^{width}}'.format(s = ''.join(blue_sky), width = 40) for _ in range(HEIGHT - 1)]
            ground_row = copy(ground)
            ground_row[ground_pos] = D
            ground_row[top_init_pos] = F
            scene = '\n'.join(scene +  ['{s: ^{width}}'.format(s = ''.join(ground_row), width = 38)])
            print(scene)  
            print("It's a miss!")
            if len(catches) == 0:
                print("You're risking going to the pub by yourself..")
            ground_row[ground_pos] = D
    return catches       

def step3_bar(moral = 0, company = Counter()):
    try:
        l = list(company.items())[0][1]
    except IndexError:
        l = 0   
    if l > 0:
        print('\n')
        print('The duck and ' + f'{l} {list(company.keys())[0]}' + 's'*bool(l > 1) + ' walk into a pub..')
        time.sleep(2)
        print(f"The duck says: '{l+1} appletini, pronto!")
        time.sleep(2)
        print("Words fail the barmen, utterly agaze, he stays silent for a while, then takes an umbrella and shoots himself")
    else:
        print('The duck walks into a pub..')
        time.sleep(2)
        print("'What would you like?', the barmen asks..'")    
        if moral > 0:
            print("The duck says: ")
            time.sleep(2)
            print("'..A glass of somewhat white..'")
            time.sleep(2)
            print("'..also a brush and dissolvent..'")
        else:
            print("'..Triple whiskey..'")
            time.sleep(2)
            print("'..and a gun..'")
            time.sleep(2)
            print("'..a spraying gun..")
            time.sleep(2)
            print("'..still gotta go paint that house in East Northampton after all..'")
    return None

if __name__ == '__main__':
    step1()
