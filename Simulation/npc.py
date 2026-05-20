import random

class NPC:
    def __init__(self, npc_id):
        self.id = npc_id
        self.money = random.randint(20, 100)
        self.hunger = random.randint(0, 50)
        self.city = None
        self.travel_target = None
        self.travel_timer = 0
        self.trade_route = None
        self.metabolism = random.uniform(0.7, 1.4)
        self.hunger_threshold = random.randint(35, 75)
        self.cargo = {
            "food": 0
        }
        
        self.relationships ={}

        self.personality = {
            "greed": random.random(),
            "sociability": random.random(),
            "risk": random.random(),
            "discipline": random.random(),
            "empathy": random.random(),
            "impulsiveness": random.random(),
        }

        # 🗓 RUTINA BASE
        self.schedule = {
            "morning": "work",
            "afternoon": "work",
            "evening": "socialize",
            "night": "rest"
        }

        self.memory_short = {
            "worked": 0,
            "socialized": 0,
            "rested": 0,
            "ate": 0,
        }

        self.memory_emotional = {
            "job_satisfaction": 0.5,
            "social_satisfaction": 0.5,
            "life_satisfaction": 0.5
        }

        self.energy = 100
        self.happiness = 50
        self.stress = 25
        self.satiety = 0
        
        self.inventory = {
            "food": random.randint(1, 3),
            "goods": 0
        }

    def get_time_block(self, hour):
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"

    def update(self, world):
        self.hunger += 1 * self.metabolism
        self.energy -= 2
        self.satiety = max(0, self.satiety - 2)
        self.happiness *= 0.995

        self.decay_memory()

        for k in self.memory_emotional:
            self.memory_emotional[k] *= 0.995
        

        self.decide(world)
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.energy = max(0, min(100, self.energy))
        self.stress += self.city.base_stress * 0.5
        self.stress = max(0, min(100, self.stress))
        self.satiety = max(0, min(100, self.satiety))
        
    def decay_memory(self):
        for key in self.memory_short:
            self.memory_short[key] *= 0.8

    def decide(self, world):
        drives = self.calcule_drives(world)

        # 🔥 RUTINA + PERSONALIDAD
        time_block = self.get_time_block(world.hour)
        planned_action = self.schedule[time_block]

        # disciplina → sigue rutina
        if self.hunger < 70:  # no seguir rutina si está muy mal
            drives[planned_action] += 0.5 * self.personality["discipline"]

        # impulsividad → rompe rutina
        for k in drives:
            noise = random.uniform(-0.2, 0.2) * self.personality["impulsiveness"]
            drives[k] += noise

        action = max(drives, key=drives.get)

        world.logger.log(f"[Día {world.day} Hora {world.hour}] NPC {self.id}: {action}")

        self.execute(action, world)

    def calcule_drives(self, world):
        drives = {}
        culture = self.city.culture
        hour = world.hour
        food_available = self.city.resources["food"]

        # =========================
        # 🍔 COMER (PRIORIDAD REAL)
        # =========================
        if self.satiety < 30:
            if self.hunger > self.hunger_threshold:
                drives["eat"] = (
                    ((self.hunger - self.hunger_threshold) / 100) * 8
                )
            else:
                drives["eat"] = 0.2
        else:
            drives["eat"] = 0

        # =========================
        # 🛒 COMPRAR (CONTROLADO)
        # =========================
        
        food_ratio = self.city.resources["food"] / max(1, len(self.city.npcs))

        desired_food = 5

        drives["buy_food"] = (
            max(0, desired_food - self.inventory["food"]) * 0.8
        )

        # =========================
        # 💼 TRABAJO (RESPUESTA A HAMBRE)
        # =========================        
        if hour in self.job["work_hours"]:
            drives["work"] = (
                1.0 +
                self.personality["discipline"] * 0.7 +
                (1 - self.money / 200) +
                (self.hunger / 100) * 4  # 🔥 CLAVE
            )
        else:
            drives["work"] = 0


        # cultura
        drives["work"] += culture["discipline"] * 0.3

        if self.profession == "unemployed":
            drives["work"] = 0

        if self.money < 30:
            drives["work"] += 2
        # =========================
        # 🧑‍🤝‍🧑 SOCIAL
        # =========================
        if 18 <= hour <= 22:
            drives["socialize"] = (
                self.personality["sociability"] * 0.8 +
                self.memory_emotional["social_satisfaction"]
            )
        else:
            drives["socialize"] = 0.2 * self.personality["sociability"]

        if self.relationships:
            avg_relation = sum(self.relationships.values()) / len(self.relationships)
        else:
            avg_relation = 0

        drives["socialize"] += avg_relation * 0.5
        drives["socialize"] += culture["sociability"] * 0.3

        # =========================
        # 😴 DESCANSO
        # =========================
        if hour >= 22 or hour <= 5:
            drives["rest"] = 1.5 + (100 - self.energy)/100
        else:
            drives["rest"] = (100 - self.energy)/50
        
        # ==============================
        #   Trader
        #===============================
        if self.profession == "trader":
            best_route = None
            best_profit = 0

            for route in world.trade_routes:
                if route["profit"] > best_profit:
                    best_profit = route["profit"]
                    best_route = route

            if best_route:
                self.trade_route = best_route

                # 🔥 comprar en ciudad origen
                if self.city == best_route["from"] and self.cargo["food"] == 0:
                    drives["trade_buy"] = best_profit * 1.5

                # 🔥 viajar con carga
                elif self.cargo["food"] > 0 and self.city != best_route["to"]:
                    drives["travel"] = best_profit * 2

                # 🔥 vender en destino
                elif self.city == best_route["to"] and self.cargo["food"] > 0:
                    drives["trade_sell"] = best_profit * 2

            else:
                drives["trade_buy"] = 0
                drives["trade_sell"] = 0

        return drives
    
    def update_emotions(self, action):
        if action == "work":
            self.memory_emotional["job_satisfaction"] += (
                0.05 * self.personality["discipline"]
            )
        elif action == "socialize":
            self.memory_emotional["social_satisfaction"] += (
                0.02 * self.personality["sociability"]
            )

        if self.hunger >= 80:
            self.memory_emotional["life_satisfaction"] -= 0.05

    def clamp_memory(self):
        for k in self.memory_emotional:
            self.memory_emotional[k] = max(0, min(1, self.memory_emotional[k]))
    
    def choose_social_target(self, world):
        candidates = [
            npc for npc in world.npcs
            if npc.id != self.id and npc.id not in world.busy_npcs
        ]

        if not candidates:
            return None

        weighted = []
        for npc in candidates:
            relation = self.relationships.get(npc.id, 0)
            weight = 1 + relation

            if self.personality["impulsiveness"] > 0.7:
                weight += abs(relation) * 0.5

            weighted.append((npc, max(0.1, weight)))

        return self.weighted_choice(weighted)
    
    def social_interaction(self, other, world):
        compatibility = (
            (self.personality["sociability"] + other.personality["sociability"]) / 2 +
            (self.personality["empathy"] + other.personality["empathy"]) / 2
        )

        outcome = compatibility + random.uniform(-0.5, 0.5)

        if outcome > 0.7:
            change = 0.1
            tipo = "amigable"
            self.happiness += 2
        elif outcome < 0.3:
            change = -0.1
            tipo = "conflicto"
            self.stress += 1
        else:
            change = 0.02
            tipo = "neutral"

        # asegurar existencia
        self.relationships.setdefault(other.id, 0)
        other.relationships.setdefault(self.id, 0)

        self.relationships[other.id] += change
        other.relationships[self.id] += change

        # clamp
        self.relationships[other.id] = max(-1, min(1, self.relationships[other.id]))
        other.relationships[self.id] = max(-1, min(1, other.relationships[self.id]))

        # 🔥 PRINT CLAVE
        world.logger.log(
            f"   🤝 NPC {self.id} → NPC {other.id} | {tipo} ({change:+.2f}) | relación: {self.relationships[other.id]:.2f}"
        )

        return change
    
    def weighted_choice(self, actions):
        total = sum(weight for _, weight in actions)
        r = random.uniform(0, total)

        upto = 0
        for item, weight in actions:
            if upto + weight >= r:
                return item
            upto += weight

        return actions[-1][0]

    def execute(self, action, world):

        if self.hunger > 85:
            if self.city.resources["food"] > 0:
                self.city.resources["food"] -= 1
                self.hunger -= 25
        elif action == "eat":
            if self.inventory["food"] > 0:
                self.inventory["food"] -= 1
                food_value = random.randint(20, 35)
                self.hunger -= food_value
                self.satiety += 20
                self.happiness += 2
                self.energy += 5
                self.stress -= 1
                self.memory_short["ate"] += 1
            else:
                self.hunger += 5
                self.stress += 0.5
        elif action == "work":
            base_income = self.job["base_salary"]

            efficiency = (
                1 +
                self.personality["discipline"] * 0.5 -
                self.stress / 200
            )

            # 🔥 NUEVO: FACTORES FÍSICOS
            physical_factor = (
                0.85 +
                (self.energy / 100) * 0.1 +
                (1 - self.hunger / 100) * 0.05
            )

            efficiency *= physical_factor

            # 💰 DINERO
            income = int(base_income * self.city.economic_factor * efficiency)
            self.money += income

            # 🌾 PRODUCCIÓN REAL
            produces = self.job.get("produces")
            base_output = self.job.get("base_output", 0)

            if produces:
                bonus = self.city.production_bonus.get(produces, 1.0)

                produced = (
                    base_output *
                    efficiency *
                    bonus *
                    random.uniform(0.9, 1.1)
                )

                whole = int(produced)

                if random.random() < (produced - whole):
                    whole += 1

                produced = whole

                self.city.resources[produces] += produced

            self.stress += self.job["stress_gain"]
            self.memory_short["worked"] += 1
        elif action == "socialize":
            target = self.choose_social_target(world)
        
            if target:
                world.busy_npcs.add(self.id)
                world.busy_npcs.add(target.id)
        
                interaction_result = self.social_interaction(target, world)
        
                world.logger.log(f"NPC {self.id} interactúa con NPC {target.id} ({interaction_result:+.2f})")
        
                self.memory_short["socialized"] += 1
                self.energy -= 5
                self.happiness += 4
                self.stress -= 3
        elif action == "rest":
            self.energy += 15
            self.stress -= 0.2
            self.hunger += 2
            self.memory_short["rested"] += 1
        elif action == "buy_food":
            amount = min(3, self.city.resources["food"])
            price = self.city.cost_of_life["food_price"]
            
            cost = amount * price
        
            if self.money >= cost:
                self.money -= cost
                self.city.treasury += cost

                self.city.resources["food"] -= amount
                self.inventory["food"] += amount
        elif action == "travel" and self.profession == "trader":
            if not self.trade_route:
                return
        
            self.travel_timer += 1
        
            if self.travel_timer >= 3:
                if self in self.city.npcs:
                    self.city.npcs.remove(self)
        
                # decidir destino según estado
                if self.cargo["food"] > 0:
                    self.city = self.trade_route["to"]
                else:
                    self.city = self.trade_route["from"]
        
                self.city.npcs.append(self)
        
                self.travel_timer = 0
        elif action == "trade_buy":

            city_food = self.city.resources["food"]

            if city_food <= 0:
                return

            price = self.city.cost_of_life["food_price"]

            amount = min(
                50,
                city_food,
                int(self.money / price)
            )

            if amount <= 0:
                return

            cost = amount * price

            self.money -= cost

            self.city.resources["food"] -= amount

            self.cargo["food"] += amount
        elif action == "trade_sell":

            self.city.resources["food"] += self.cargo["food"]

            self.cargo["food"] = 0

        self.update_emotions(action)
        self.clamp_memory()