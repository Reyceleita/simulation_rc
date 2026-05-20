import random

class City:
    def __init__(self, config, name="City"):
        self.name = name
        self.type = config["type"]
        self.treasury = 0
        
        #Poblacion
        self.npcs = []
        
        #Empleo
        self.jobs_distribution = config["jobs"]
        
        #recursos
        self.resources = {
            "food": 200
        }
        
        #Bonus de produccion según ciudad
        self.production_bonus = {
            "food": 2.5 if self.type == "agricultural" else 0.8,
            "goods": 1.5 if self.type == "industrial" else 0.7
        }
        
        #Economía
        self.cost_of_life = config["cost_of_life"].copy()
        self.base_prices = self.cost_of_life.copy()
        
        self.economic_factor = config.get("economic_factor", 1.0)
        
        #Cultura
        self.culture = config["culture"]
        
        #Estres base
        self.base_stress = config["base_stress"]
        
        #Historial
        self.history = {
            "food": [],
            "goods": [],
            "prices": [],
            "population": [],
            "employed": [],
            "unemployed": [],
            "hunger": [],
            "money": [],
            "stress": [],
            "happiness": []
        }
    
    def update(self):
        self.collect_taxes()
        self.adjust_prices()
        self.record_history()
    
    def collect_taxes(self):
        if not self.npcs:
            return
        
        subsidy = self.treasury * 0.3
        per_npc = subsidy / len(self.npcs)
        
        for npc in self.npcs:
            npc.money += per_npc
        
        self.treasury -= subsidy
    
    def get_employment_stats(self):
        employed = len([n for n in self.npcs if n.job != "unemployed"])
        unemployed = len(self.npcs) - employed
        return employed,unemployed
    
    def adjust_prices(self):
        food = self.resources["food"]
        population = len(self.npcs)

        ratio = food / max(1, population)

        base_price = self.base_prices["food_price"]

        multiplier = max(0.5, min(2.5, 2 - ratio * 0.4))

        self.cost_of_life["food_price"] = int(base_price * multiplier)
    
    def record_history(self):
        self.history["prices"].append(self.cost_of_life["food_price"])

        self.history["population"].append(len(self.npcs))
        
        self.history["food"].append(self.resources["food"])

        employed = len([n for n in self.npcs if n.profession != "unemployed"])
        unemployed = len(self.npcs) - employed

        self.history.setdefault("employed", []).append(employed)
        self.history.setdefault("unemployed", []).append(unemployed)
        #self.history["unemployed"].append(unemployed)

        # 🔥 NUEVO: métricas sociales
        if self.npcs:
            avg_hunger = sum(n.hunger for n in self.npcs) / len(self.npcs)
            avg_money = sum(n.money for n in self.npcs) / len(self.npcs)
            avg_stress = sum(n.stress for n in self.npcs) / len(self.npcs)
            avg_happiness = sum(n.happiness for n in self.npcs) / len(self.npcs)
        else:
            avg_hunger = avg_money = avg_stress = avg_happiness = 0

        self.history.setdefault("hunger", []).append(avg_hunger)
        self.history.setdefault("money", []).append(avg_money)
        self.history.setdefault("stress", []).append(avg_stress)
        self.history.setdefault("happiness", []).append(avg_happiness)