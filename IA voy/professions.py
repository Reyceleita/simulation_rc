import random

PROFESSIONS = {
    "worker": {
        "base_salary": 15,
        "work_hours": range(6, 17),
        "food_cost": 5,
        "stress_gain": 1.0,
        "produces": "food",
        "base_output": 2,
    },
    "merchant": {
        "base_salary": 25,
        "work_hours": range(8, 20),
        "food_cost": 12,
        "stress_gain": 1.2,
        "produces": None,
        "base_output": 0,
    },
    "unemployed": {
        "base_salary": 2, #Subsidio
        "work_hours": [],
        "food_cost": 4,
        "stress_gain": 0.5,
        "produces": None,
        "base_output": 0,
    },
    "trader": {
        "base_salary": 5,
        "stress_gain": 0.3,
        "work_hours": list(range(6, 20)),
        "produces": None,
        "base_output": 0
    }
}

def get_random_profession():
    return random.choice(list(PROFESSIONS.keys()))