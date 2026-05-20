import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Dashboard:
    def __init__(self, world):
        self.world = world

        self.root = tk.Tk()
        self.root.title("Simulación - Dashboard")

        # 🔥 más espacio
        self.fig, self.axes = plt.subplots(4, 3, figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_interval = 500

        self.update()

    def update(self):
        with self.world.lock:
            cities = list(self.world.cities)

        # limpiar todo
        for ax in self.axes.flat:
            ax.clear()

        for i, city in enumerate(cities):
            history = city.history

            if not history["hunger"]:
                continue

            # 🔥 últimos datos
            h = history["hunger"][-50:]
            m = history["money"][-50:]
            s = history["stress"][-50:]
            hp = history["happiness"][-50:]
            food = history["food"][-50:]
            price = history["prices"][-50:]
            emp = history["employed"][-50:]
            unemp = history["unemployed"][-50:]

            # fila base por ciudad
            row = i

            # 🧠 SOCIAL
            ax1 = self.axes[row][0]
            ax1.plot(h, label="Hunger")
            ax1.plot(s, label="Stress")
            ax1.plot(hp, label="Happy")
            ax1.set_title(f"{city.name} - Social")
            ax1.legend(fontsize=6)

            # 💰 ECONOMÍA
            ax2 = self.axes[row][1]
            ax2.plot(food, label="Food")
            ax2.plot(price, label="Price")
            ax2.plot(m, label="Money")
            ax2.set_title(f"{city.name} - Economy")
            ax2.legend(fontsize=6)

            # 👥 EMPLEO
            ax3 = self.axes[row][2]
            ax3.plot(emp, label="Emp")
            ax3.plot(unemp, label="Unemp")
            ax3.set_title(f"{city.name} - Jobs")
            ax3.legend(fontsize=6)

        self.canvas.draw()
        self.root.after(self.update_interval, self.update)

    def run(self):
        self.root.mainloop()