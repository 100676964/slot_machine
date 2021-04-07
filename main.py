import threading
import msvcrt
from wheel import reel
from game import *
# parameters............................................

mode = 'game'
number_of_reels = 3
number_of_symbols = 4
f_payout = lambda x: ((1/x) * number_of_reels*number_of_symbols)
number_of_runs = 10000
number_of_simulations = 1
# parameters............................................

def create_custom_reels(number_of_reels,number_of_symbols,stops):
    number_of_reels = int(input("How many reels: "))
    number_of_symbols = int(input("How many symbols: "))
    stops = int(input("How many stops(stop >= number of wheels): "))
    for i in range(number_of_reels):
        s = []
        for j in range(stops):
            s.append(int(input("Enter Reel "+str(i+1)+" Symbol "+str(j+1)+": ")))
        reels.append(reel(s))
        stops = len(s)
    return reels,stops,number_of_symbols

def user_input():
    while len(reels) > 0:
        c = msvcrt.getch().decode('ASCII')
        # print(c)a
        if  c == 'g':
            start_spinning(threads,reels)
            print("Start")
        if c == 's':
            stop_wheel(threads,reels)
        if c == 'q':
            stop_wheel(threads,reels,all=True)
            reels.clear()
        if c.isdigit() == True:
            print("hi")
            if int(c) == 0:
                update_play_lines(Inf)
            else:
                update_play_lines(int(c))

reels = []
stops = 0
if 'c' in mode:
    while True:
        try:
            reels,stops,number_of_symbols = create_custom_reels(number_of_reels,number_of_symbols,stops)
            break
        except:
            print("Invalid Input")        
else:
    for i in range(number_of_reels):
        reels.append(reel(number_of_symbols))
    stops = (number_of_symbols*(number_of_symbols + 1))/2

if stops >= number_of_reels and len(reels) > 1:
    
    threads = []
    results = [] 
    if 'game' in mode:
        threading.Thread(target=user_input).start()
        gui_interface(reels,results,threads,f_payout)
    elif 'sim' in mode:
        total_price_list = []
        temp = reels.copy() 
        for i in range(number_of_simulations):
            # os.system('cls')
            # update_play_lines(1)
            reels = temp.copy()
            reset()
            
            total_price_list.append(simulation(number_of_runs,reels,results,threads,f_payout))
            
            reels.clear()
        print(total_price_list)
        import matplotlib.pyplot as plt
        # plt.show() 
        # plt.figure()
        # plt.plot([4,5,6,7,8,9],[21773,14532,10090,7601,6044,4574])
        plt.show()
           
else:
    print("not enough symbols to make the wheel")




