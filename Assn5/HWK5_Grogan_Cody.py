import numpy as np
import random
from matplotlib import pyplot as plt
import os

class Simulation:
    def __init__(self, creatures: list, food_count: int, fight, food_limit: bool):
        self.food_count = food_count
        self.creatures = creatures
        self.fight = fight
        self.food_limit = food_limit
        
    def simulateDay(self):
        shuffled_creatures = self.creatures.copy()
        random.shuffle(shuffled_creatures)

        food_list = [Food() for i in range(self.food_count)]

        for creature in shuffled_creatures:
            self.allocateCreatures(food_list, creature)
        
        for food in food_list:
            if len(food.interested_creatures) == 1:
                food.interested_creatures[0].eat(2.0)
            elif len(food.interested_creatures) > 1:
                self.fight(food.interested_creatures)
        
        self.updateCreatures()
    
    def allocateCreatures(self, food_list, creature):
        avail_food = [food for food in food_list if food.available]

        if len(avail_food) > 0:
            target_food = random.choice(avail_food)
            target_food.interested_creatures.append(creature)
            if self.food_limit:
                if len(target_food.interested_creatures) == 2:
                    target_food.available = False
                elif len(target_food.interested_creatures) > 2:
                    creature.eat(0.0)
        else:
            creature.eat(0.0)
    
    def updateCreatures(self):
        for creature in self.creatures:
            if creature.is_dead:
                self.creatures.remove(creature)
            elif creature.is_pregnant:
                self.creatures.append(creature.__class__())
                creature.is_pregnant = False


class Fight1:
    def __init__(self, creatures):

        contestant1 = creatures[0]
        contestant2 = creatures[1]

        contestant1_type = contestant1.__class__.__name__
        contestant2_type = contestant2.__class__.__name__

        if contestant1_type == "Dove" and contestant2_type == "Dove":
            contestant1.eat(1.0)
            contestant2.eat(1.0)
        elif contestant1_type == "Dove" and contestant2_type == "Hawk":
            contestant1.eat(0.5)
            contestant2.eat(1.5)
        elif contestant1_type == "Hawk" and contestant2_type == "Dove":
            contestant1.eat(1.5)
            contestant2.eat(0.5)
        else:
            contestant1.eat(0.0)
            contestant2.eat(0.0)

class Fight2:
    def __init__(self, creatures):
        self.contestants = creatures

        hawks = [creature for creature in creatures if creature.__class__.__name__ == "Hawk"]
        doves = [creature for creature in creatures if creature.__class__.__name__ == "Dove"]
        dove_count = len(doves)
        hawk_count = len(hawks)
        
        if hawk_count == 0:
            food = 2.0/dove_count
            for creature in self.contestants:
                creature.eat(food)

        elif hawk_count == 1:
            food = 1.0/dove_count
            for creature in self.contestants:
                if creature.__class__.__name__ == "Hawk":
                    creature.score += 1
                    creature.eat(1.0)
                else:
                    creature.eat(food)

        else:
            matchup_hawks = hawks.copy()
            random.shuffle(matchup_hawks)
            while len(matchup_hawks) > 1:
                hawk1 = matchup_hawks.pop()
                hawk2 = matchup_hawks.pop()
                if hawk1.score > hawk2.score:
                    hawk1.score += 1
                    matchup_hawks.append(hawk1)
                    hawk2.is_dead = True
                elif hawk2.score > hawk1.score:
                    hawk2.score += 1
                    matchup_hawks.append(hawk2)
                    hawk1.is_dead = True
                else:
                    hawk1.is_dead = True
                    hawk2.is_dead = True

            if len(matchup_hawks) == 1:
                matchup_hawks[0].eat(2.0 if dove_count == 0 else 1.0)
                dove_food = 1.0
            else:
                dove_food = 2.0
            
            for dove in doves:
                dove.eat(dove_food/dove_count)
            
                  
                
            
             
    
class Dove:
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
        self.score = 0
    
    def eat(self, food: float):
        if food == 0.0:
            self.is_dead = True 
        elif food < 1.0:
           self.is_dead = np.random.uniform(0.0, 1.0) < food
        elif food > 1.0 and food < 2.0:
            self.is_pregnant = np.random.uniform(0.0, 1.0) < (food-1.0)
        elif food >= 2.0:
            self.is_pregnant = True


class Food:
    def __init__(self):
        self.available = True
        self.interested_creatures = []
    
    
def print(creature_counts, days, title, saveFile):
    x = np.arange(0, days, 1)
    blobs = [i[0] for i in creature_counts]
    hawks = [i[1] for i in creature_counts]
    y = np.vstack([blobs, hawks])
    fig, ax = plt.subplots()
    ax.stackplot(x, y)
    ax.set_xlabel("Day")
    ax.set_ylabel("Number of Creatures")
    ax.set_title(title)

    fig.savefig(saveFile)


def VanillaSim(doves, hawks, title):
    save_file = os.path.join(os.path.dirname(__file__),"Figures",  f"VanillaSim_D_{doves}_H_{hawks}.png")
    creatures = [Dove() for i in range(doves)] + [Hawk() for i in range(hawks)]
    food_count = 100
    sim = Simulation(creatures, food_count, Fight1, True)
    DAY_COUNT = 100
    creature_counts = []
    
    for i in range(DAY_COUNT):
        sim.simulateDay()
        doves = 0
        hawks = 0

        for creature in sim.creatures:
            if creature.__class__.__name__ == "Dove":
                doves += 1
            else:
                hawks += 1
        
        creature_counts.append((doves, hawks))
    
    print(creature_counts, DAY_COUNT, title, save_file)

def ComplexSim(doves, hawks, title):
    save_file = os.path.join(os.path.dirname(__file__),"Figures",  f"ImprovedSim_D_{doves}_H_{hawks}.png")
    creatures = [Dove() for i in range(doves)] + [Hawk() for i in range(hawks)]
    food_count = 20
    sim = Simulation(creatures, food_count, Fight2, False)
    DAY_COUNT = 100
    creature_counts = []
    
    for i in range(DAY_COUNT):
        sim.simulateDay()
        doves = 0
        hawks = 0

        for creature in sim.creatures:
            if creature.__class__.__name__ == "Dove":
                doves += 1
            else:
                hawks += 1
        
        creature_counts.append((doves, hawks))
    
    print(creature_counts, DAY_COUNT, title, save_file)



if __name__ == "__main__":
    VanillaSim(1, 0, "Vanilla Simulation: 1 Dove, 0 Hawks")
    VanillaSim(0, 1, "Vanilla Simulation: 0 Doves, 1 Hawk")
    VanillaSim(20, 1, "Vanilla Simulation: 20 Doves, 1 Hawk")
    ComplexSim(1, 0, "Improved Simulation: 1 Dove, 0 Hawks")
    ComplexSim(0, 1, "Improved Simulation: 0 Doves, 1 Hawk")
    ComplexSim(20,1, "Improved Simulation: 20 Doves, 1 Hawk")
    plt.show()
    