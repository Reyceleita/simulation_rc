import matplotlib.pyplot as plt
import networkx as nx

def plot_stats(world):
    plt.ion()

    while True:
        with world.lock:
            stats = world.stats.copy()

        plt.clf()
        plt.plot(stats["money"], label="Dinero")
        plt.plot(stats["hunger"], label="Hambre")
        plt.plot(stats["happiness"], label="Felicidad")
        plt.plot(stats["stress"], label="Estrés")

        plt.legend()
        plt.pause(0.5)

def plot_distribution(npcs):

    money = [npc.money for npc in npcs]
    hunger = [npc.hunger for npc in npcs]
    happiness = [npc.happiness for npc in npcs]
    stress = [npc.stress for npc in npcs]

    plt.figure()
    plt.hist(money, bins=10)
    plt.title("Distribución de dinero")
    plt.show()

    plt.figure()
    plt.hist(hunger, bins=10)
    plt.title("Distribución de hambre")
    plt.show()

    plt.figure()
    plt.hist(happiness, bins=10)
    plt.title("Distribución de felicidad")
    plt.show()

    plt.figure()
    plt.hist(stress, bins=10)
    plt.title("Distribución de estrés")
    plt.show()

def plot_npc(world, npc_id):

    data = world.npc_history[npc_id]

    plt.figure()
    plt.plot(data["money"], label="Dinero")
    plt.plot(data["hunger"], label="Hambre")
    plt.plot(data["happiness"], label="Felicidad")
    plt.plot(data["stress"], label="Estrés")

    plt.legend()
    plt.title(f"NPC {npc_id}")
    plt.show()

def plot_relationships(world):

    G = nx.Graph()

    for npc in world.npcs:
        G.add_node(npc.id)

        for other_id, value in npc.relationships.items():

            if abs(value) > 0.2:
                G.add_edge(npc.id, other_id, weight=value)

    pos = nx.spring_layout(G)
    edges = G.edges()

    weights = [G[u][v]['weight'] for u, v in edges]

    plt.figure()
    nx.draw(G, pos, with_labels=True, width=weights)
    plt.title("Red de relaciones")
    plt.show()

def plot_city(city):
    plt.figure(figsize=(10,6))

    plt.plot(city.history["food"], label="Comida")
    plt.plot(city.history["prices"], label="Precio comida")
    plt.plot(city.history["employed"], label="Empleados")
    plt.plot(city.history["unemployed"], label="Desempleados")

    plt.title(f"Ciudad: {city.name}")
    plt.legend()
    plt.show()

def plot_all_cities(world):
    plt.ion()

    while True:
        plt.clf()

        for i, city in enumerate(world.cities):
            plt.subplot(2, 2, i+1)

            plt.plot(city.history["food"], label="Food")
            plt.plot(city.history["prices"], label="Price")

            plt.title(city.name)
            plt.legend()

        plt.pause(0.5)