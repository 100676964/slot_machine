import threading

from numpy.core.numeric import Inf
from wheel import reel
import random
from typing import List
import time
import os
import numpy as np

__price = 0
__game_count = 0
__num_of_line = Inf

def reset():
    global __game_count,__price
    __price = 0
    __game_count = 0

def start_spinning(threads:List[threading.Thread],reels:List[reel],mode = 0):
    global __game_count
    if check_game_status(threads) == 0 or check_game_status(threads) == 2:
        threads.clear()
        __game_count += 1  
        for i in range(len(reels)):
            reels[i].stop = False
            threads.append(threading.Thread(target=reels[i].spin, args = (random.randint(25,60),mode,)))
            threads[i].daemon = True
            threads[i].start()

def stop_wheel(threads:List[threading.Thread],reels:List[reel],all = False):
    if check_game_status(threads) == 1:
        for i in range(len(reels)):
            if threads[i].is_alive():
                reels[i].stop = True
                print("STOP")
                if all == False:
                    break

def check_game_status(threads:List[threading.Thread]):
    if len(threads) == 0:
        return 0      
    for i in threads:
        if i.is_alive():
            return 1
    return 2
    # 0 -> first game
    # 1 -> running
    # 2 -> finish

def check_results(reels:List[reel]):
    matrix = []
    for i in range(len(reels)):
        matrix.append(reels[i].reel)
    matrix = np.array(matrix)
    diag = []
    diag2 = []
    line = []
    
    for i in range(len(matrix)):
        diag.append(matrix[i][i])
        diag2.append(matrix[i][(len(matrix)-i-1)])
    # line 1 - n
    for i in range(len(reels)):
        for n in range(3,len(matrix[:,i])+1):
            for j in range(len(matrix[:,i])-n+1):    
                if (matrix[:,i][j:j+n] == matrix[:,i][j]).all():
                    line.append([i+1,matrix[:,i][j]])
    # lin d
    for n in range(3,len(matrix[:,i])+1):
        for j in range(len(matrix[:,i])-n+1):
            if (diag[j:j+n] == diag[j]).all():
                line.append([len(reels)+1,diag[j]])

    for n in range(3,len(matrix[:,i])+1):
        for j in range(len(matrix[:,i])-n+1):
            if (diag2[j:j+n] == diag2[j]).all():
                line.append([len(reels)+2,diag2[j]])

    line = np.array(line)
    return line

def update_price(amout):
    global __price
    __price += amout
    return __price
    
def update_play_lines(num):
    global __num_of_line
    __num_of_line = num

def gui_interface(reels:List[reel],results,threads:List[threading.Thread],fx):
    global __game_count,__price
    current_game = 0
    
    counter = 0
    start_time = time.time()
    elapsed = 0
    while len(reels) > 0:
        try:
            if elapsed != 0:
                if counter/elapsed < 25:
                    
                    os.system('cls')
                    print("FPS: "+str(int(counter/elapsed)))
                    if __num_of_line > len(reels)+2:
                        print("Payout Lines: "+str(len(reels)+2))
                    else:
                        print("Payout Lines: "+str(__num_of_line))
                    print("Game: "+str(__game_count))
                    print("Total Payouts: "+str(__price))
                    print("_________THE BIG GAME MACHINE_________")
                    print()

                
                    
                    for i in range(len(reels)):
                        if 19 - int((len(reels)*5)/2) > 0:
                            for k in range(19  - int((len(reels)*5)/2)):
                                print(' ',end='')
                        for j in range(len(reels)):
                            print(" |",end='')
                            for m in range(len(str(max(reels[j].reel)))-len(str(reels[j].reel[i]))):
                                print('0',end='') 
                            print(str(reels[j].reel[i])+"| ",end='')#str()
                        print()
                        

                
                    
                    if check_game_status(threads) == 2:
                        
                        if current_game != __game_count:
                            current_price = 0
                            results = check_results(reels)
                            for i in range(len(results)):
                                if results[i][0] <= __num_of_line:
                                    current_price +=  fx(results[i][1])
                            __price += current_price
                            current_game += 1
                            
                        if len(results) > 0:
                            print(results)
                            print(current_price)
                        else:
                            print("Nothing!")
                    counter += 1

            elapsed =  time.time() - start_time
            if elapsed >= 1:
                start_time = time.time()
                elapsed -= 0
                counter = 0
        except Exception as e:
            print(e)

        # input()

def simulation(number_of_runs,reels:List[reel],results,threads:List[threading.Thread],fx):
    global __game_count,__price
    price_list = []
    while __game_count < number_of_runs:
        __game_count += 1
        cp = 0
        for i in range(len(reels)):
            reels[i].spin(random.randint(25,60),mode=1)
        
        results = check_results(reels)
        results = check_results(reels)
        for i in range(len(results)):
            if results[i][0] <= __num_of_line:
                cp +=  fx(results[i][1])
                
        price_list.append(cp)
        __price += cp
        # if cp > 4:
        #     for i in range(len(reels)):
        #         for j in range(len(reels)):
        #             print(" |"+str(reels[j].reel[i])+"| ",end='')#str()
        #         print()
        #     input()
        
        print('game: '+str(__game_count)+'current_price: '+str(cp))
            
    # print('total price: '+str(__price))
    import matplotlib.pyplot as plt
    plt.figure()
    plt.hist(price_list,bins = 8)
    
    return __price