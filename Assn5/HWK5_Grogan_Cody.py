import numpy as np

class Simulation:
    def __init__(self, initial_blob: int, initial_hawk: int, food_count: int):
        self.food_count = food_count
        self.initial_blob = initial_blob
        self.initial_hawk = initial_hawk
        
        self.food_spot_array = []
    
    
class Blob:
    def __init__(self):
        self.is_dead = False
        self.is_pregnant = False
    
    def eat(self, food: float):
        if food == 0.0:
            self.is_dead = True 
        elif food < 1.0:
           self.is_dead = np.random.uniform(0.0, 1.0) < food
        elif food > 1.0 and food < 2.0:
            self.is_pregnant = np.random.uniform(0.0, 1.0) < (food-1.0)
        elif food >= 2.0:
            self.is_pregnant = True
        
class Hawk:
    def __init__(self):
        self.is_dead = False
        self.is_pregnant = False
    
    


if __name__ == "__main__":
    sim = Simulation()
    