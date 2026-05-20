import random
import threading
import matplotlib.pyplot as plt

from npc import NPC
from city import City
from sim.generators.npc_generator import NPCGenerator
from sim.utils.logger import Logger
from cities import *
from professions import PROFESSIONS

class World:
    def __init__(self):
        self.lock = threading.Lock()
        self.logger = Logger()
        self.cities = [
            City(agricultural_config, "Agro"),
            City(industrial_config, "Indus"),
            City(commercial_config, "Comer"),
            City(marginal_config, "Marginal")
        ]
        city_population = {
            "Agro": 25,
            "Indus": 25,
            "Comer": 25,
            "Marginal": 25
        }
        self.tick = 0
        
        #rutas comerciales
        self.trade_routes = []
        self.update_trade_routes()
        
        #NPC's
        self.npcs = []
        
        generator = NPCGenerator()
        npc_id = 0

        for city in self.cities:
            target_population = city_population[city.name]

            for _ in range(target_population):
                npc = generator.create_npc(npc_id)
                npc.city = city
                city.npcs.append(npc)
                self.npcs.append(npc)

                npc_id += 1
        
        for city in self.cities:
            self.assign_jobs(city)
        
        for npc in self.npcs:
            for other in self.npcs:
                if npc.id != other.id:
                    npc.relationships[other.id] = random.uniform(-0.2,0.2)
        
        self.npc_history = {
            npc.id: {
                "money": [],
                "hunger": [],
                "happiness": [],
                "stress": []
            }
            for npc in self.npcs
        }
        
        #tiempo
        self.hour = 6
        self.day = 1
        self.stats = {
            "money": [],
            "hunger": [],
            "happiness": [],
            "stress": []
        }
    
    def assign_jobs(self, city):
        npcs = city.npcs
        total = len(npcs)

        distribution = city.jobs_distribution

        job_counts = {
            job: int(total * ratio)
            for job, ratio in distribution.items()
        }

        # Ajuste por redondeo
        while sum(job_counts.values()) < total:
            job_counts["unemployed"] += 1

        random.shuffle(npcs)

        index = 0
        for job, count in job_counts.items():
            for _ in range(count):
                if index >= total:
                    break
                npc = npcs[index]
                npc.profession = job
                npc.job = PROFESSIONS[job]
                index += 1
    
    def trade_between_cities(self):
        buyers, sellers = self.classify_cities()
    
        for buyer in buyers:
            seller = self.find_best_seller(buyer, sellers)
    
            if not seller:
                continue
            
            self.trade_food(buyer, seller)
    
    def update_trade_routes(self):
        self.trade_routes = []

        for city_a in self.cities:
            for city_b in self.cities:
                if city_a == city_b:
                    continue

                price_diff = city_b.cost_of_life["food_price"] - city_a.cost_of_life["food_price"]
                
                food_pressure = max(0, 50 - city_b.resources["food"])

                profit = (
                    price_diff +
                    food_pressure * 0.5
                )
                if price_diff > 3:
                    self.trade_routes.append({
                        "from": city_a,
                        "to": city_b,
                        "profit": profit
                    })
    
    def classify_cities(self):
        buyers = []
        sellers = []

        for city in self.cities:
            ratio = self.get_food_ratio(city)

            if ratio < 1.5:
                buyers.append(city)
            elif ratio > 3:
                sellers.append(city)

        return buyers, sellers

    def get_food_ratio(self, city):
        population = max(1, len(city.npcs))
        return city.resources["food"] / population

    def find_best_seller(self, buyer, sellers):
        best = None
        best_price = float("inf")

        for seller in sellers:
            if seller == buyer:
                continue

            transport_cost = 2  # o dinámico después
            price = seller.cost_of_life["food_price"] + transport_cost

            if price < best_price and seller.resources["food"] > 20:
                best_price = price
                best = seller

        return best
    
    def trade_food(self, buyer, seller):
        #condiciones básicas
        if seller.resources['food'] < 10:
            return
        if buyer.resources['food'] > 150:
            return
        
        #cantidad a transferir
        amount = min(20, seller.resources['food'] // 4)
        
        #Costo de transporte
        transport_cost = 2
        
        if amount <= 0:
            return
        
        #Precio basado en diferencia
        price = seller.cost_of_life['food_price'] + transport_cost
        
        #dinero toal del buyer(hay q mejorar)
        total_money = sum(n.money for n in buyer.npcs)
        
        if total_money < price * amount:
            # comprar menos en vez de cancelar
            amount = int(total_money / price)
        
        #Transferencia
        seller.resources['food'] -= amount
        buyer.resources['food'] += amount
        
        #pagar (distribuido)
        cost_per_npc = (price * amount) / len(buyer.npcs)
        
        for npc in buyer.npcs:
            npc.money -= cost_per_npc
        
        for npc in seller.npcs:
            npc.money += (price * amount) / len(seller.npcs)
        
        #Registro
        self.logger.log(
            f"Comercio: {seller.name} -> {buyer.name} | {amount} comida"
        )
    
    def update(self):
        self.tick += 1
        self.update_trade_routes()
        self.trade_between_cities()
        random.shuffle(self.npcs)
        
        self.logger.log(f"\n--- TICK {self.tick} | Día {self.day} Hora {self.hour} ---")
        
        self.busy_npcs = set()

        # 2. Mercado se resuelve DESPUÉS
        
        
        avg_money = sum(n.money for n in self.npcs) / len(self.npcs)
        avg_hunger = sum(n.hunger for n in self.npcs) / len(self.npcs)
        avg_happiness = sum(n.happiness for n in self.npcs) / len(self.npcs)
        avg_stress = sum(n.stress for n in self.npcs) / len(self.npcs)

        with self.lock:
            self.stats["money"].append(avg_money)
            self.stats["hunger"].append(avg_hunger)
            self.stats["happiness"].append(avg_happiness)
            self.stats["stress"].append(avg_stress)
        
        
        for npc in self.npcs:
            if npc.id in self.busy_npcs:
                continue
            
            npc.update(self)

            self.npc_history[npc.id]["money"].append(npc.money)
            self.npc_history[npc.id]["hunger"].append(npc.hunger)
            self.npc_history[npc.id]["happiness"].append(npc.happiness)
            self.npc_history[npc.id]["stress"].append(npc.stress)
        
        for city in self.cities:
            city.update()
        
        
        self.show_stats()

        self.advance_time()
    
    
    def advance_time(self):
        self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1
    
    def show_stats(self):
        total_money = sum(n.money for n in self.npcs)
        avg_hunger = sum(n.hunger for n in self.npcs) / len(self.npcs)

        self.logger.log(f"NPC's: {len(self.npcs)}")
        self.logger.log(f"Dinero total: {total_money}")
        self.logger.log(f"Hambre promedio: {avg_hunger:.2f}")
        
        for city in self.cities:
            workers = sum(1 for n in city.npcs if n.profession == "worker")
            unemployed = sum(1 for n in city.npcs if n.profession == "unemployed")

            self.logger.log(
                f"{city.name} | Población: {len(city.npcs)} | Trabajan: {workers} | Desempleados: {unemployed}"
            )