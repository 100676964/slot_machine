import time
import random

class reel:
    def __init__(self, arg,resistance = 5) -> None:
        self.reel = []
        self.stop = False
        self.a = resistance
        if isinstance(arg,int):
            for i in range(arg):
                for j in range(i+1):
                    self.reel.append(i+1)
                    random.shuffle(self.reel)
        elif isinstance(arg,list):
            self.reel = arg
        # print(self.reel)    
    
    def spin(self,initial_speed,mode = 0):
        delta = 0
        delta_distance = 0
        start = time.time()
        a = self.a
        while initial_speed > 0 and self.stop is not True:
            temp = list.copy(self.reel)
            if mode == 0:
                
                start = time.time()
            
                delta_distance += initial_speed*delta
                for i in range(len(self.reel)):
                    self.reel[i] = temp[(i + int(delta_distance))%len(self.reel)]
                delta_distance -= int(delta_distance)
                initial_speed -= a*delta
                
                
                
                time.sleep(0.01)
                delta = time.time() - start 
                
                
                
                
            else:
                delta_distance += (1/2)*a*(initial_speed/a)**2                    
                for i in range(len(self.reel)):
                    self.reel[i] = temp[(i + int(delta_distance))%len(self.reel)]
                delta_distance -= int(delta_distance)
                initial_speed -= a*(initial_speed/a)

        # print(self.reel)
        # print(str(delta_distance)) 
        
# reel(5)
# reel(5)
# reel(5)
# reel(5)
# speed = 20
# test1 = reel(3)
# test1.spin(speed,mode=0)
# test2 = reel(3)
# test2.spin(speed,mode=1)
# print(test.reel)














