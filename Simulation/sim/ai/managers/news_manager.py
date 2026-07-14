"""
news_manager.py
"""

from datetime import datetime
from threading import Thread
import time
import random

from sim.ai.data.topics import TOPICS
from sim.ai.models.news import News
from sim.ai.ollama_client import OllamaNewsGenerator



class NewsManager:

    INTERVAL = 90

    def __init__(self, world):
        
        self.world = world

        self.generator = OllamaNewsGenerator()

        self.news = []

        self.last_generation = time.time()

        self.generating = False

        self.next_id = 1

    # ---------------------------------------------------------

    def update(self):

        now = time.time()

        if now - self.last_generation < self.INTERVAL:
            return

        if self.generating:
            return

        self.last_generation = now

        self.generating = True

        Thread(
            target=self._generate_news,
            daemon=True
        ).start()

    # ---------------------------------------------------------

    def _generate_news(self):

        try:

            topic = random.choice(TOPICS)

            history = [
                n.title
                for n in self.news
            ]

            title = self.generator.generate(
                topic,
                history
            )

            news = News(

                id=self.next_id,

                title=title,

                source="El Heraldo Económico",

                created_at=datetime.now()

            )

            self.news.append(news)

            self.next_id += 1

            if len(self.news) > 50:
                self.news.pop(0)

            print(title)

        finally:

            self.generating = False

    # ---------------------------------------------------------

    def latest(self):

        if not self.news:
            return None

        return self.news[-1]

    # ---------------------------------------------------------

    def history(self):

        return self.news