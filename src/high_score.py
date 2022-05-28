from datetime import datetime
import pandas as pd

class HighScores:

    def __init__(self) -> None:
        self.path = 'resources/high_scores.csv'
        try:
            self.df = pd.read_csv(self.path, index_col=0)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['name', 'datetime', 'player_level', 'score'])
            self.save()

    def add(self, name, level, score):
        dt = pd.to_datetime(datetime.now())
        new_row = pd.DataFrame(
            {'name': name, 'player_level': level, 'datetime': dt, 'score': score},
            index=[len(self.df)]
        )
        self.df = pd.concat([self.df, new_row], axis=0).reset_index(drop=True).sort_values('score')
        self.save()

    def save(self):
        self.df.to_csv(self.path)
