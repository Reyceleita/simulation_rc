class Logger:
    def __init__(self, filename="simulation_log.txt"):
        self.file = open(filename, "w", encoding="utf-8")

    def log(self, text):
        print(text)  # sigue mostrando en consola
        self.file.write(text + "\n")

    def close(self):
        self.file.close()