import random
from faker import Faker

from sim.core.Npc_AI.schedules.worker import WorkerSchedule
from sim.core.Npc.npc import NPC
from professions import PROFESSIONS, get_random_profession

# Generador de datos colombianos
fake = Faker("es_CO")


class NPCGenerator:

    def create_npc(self, npc_id):
        npc = NPC(npc_id)

        # Nombre del NPC
        npc.name = fake.name()

        # Ajustar personalidad coherente
        npc.personality = self.generate_personality()

        # Asignar profesión
        profession_name = get_random_profession()
        npc.schedule = WorkerSchedule()
        npc.profession = profession_name
        npc.job = PROFESSIONS[profession_name]

        # Ajustar personalidad según profesión
        if profession_name == "worker":
            npc.personality["discipline"] += 0.2
        elif profession_name == "merchant":
            npc.personality["greed"] += 0.3
        elif profession_name == "unemployed":
            npc.personality["stress"] = 0.6

        # Ajustar estado inicial coherente
        npc.money = random.randint(50, 150)
        npc.hunger = random.randint(10, 40)
        npc.energy = random.randint(60, 100)

        return npc

    def generate_personality(self):
        base = random.random()

        return {
            "greed": self.clamp(base + random.uniform(-0.2, 0.2)),
            "sociability": self.clamp(random.random()),
            "risk": self.clamp(random.random()),
            "discipline": self.clamp(base + random.uniform(-0.3, 0.3)),
            "empathy": self.clamp(random.random()),
            "impulsiveness": self.clamp(1 - base + random.uniform(-0.2, 0.2)),
        }

    @staticmethod
    def clamp(value):
        return max(0, min(1, value))