import threading
import time

from sim.api.dependences import get_world




class SimulationRunner:

    def __init__(self):
        
        self.world = get_world()

        self.running = False

        self.thread = None

        self.tick_rate = 1.0

    def start(self):
        print('INICIOOOO')

        if self.running:
            return

        self.running = True


        self.thread = threading.Thread(
            target=self.run_loop,
            daemon=True,
        )

        self.thread.start()

    def stop(self):

        self.running = False

    def run_loop(self):
        
        print('Rpppn loop')

        while self.running:

            try:

                self.world.update()

            except Exception as e:

                print(
                    f"Simulation Error: {e}"
                )

            time.sleep(self.tick_rate)