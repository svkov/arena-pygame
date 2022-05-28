from datetime import datetime
import pandas as pd

class HighScores:

    def __init__(self) -> None:
        self.path = 'resources/high_scores.csv'
        try:
            self.df = pd.read_csv(self.path, index_col=0)
            self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['name', 'datetime', 'player_level', 'score'])
            self.save()

    def add(self, name, level, score):
        dt = pd.to_datetime(datetime.now())
        new_row = pd.DataFrame(
            {'name': name, 'player_level': level, 'datetime': dt, 'score': score},
            index=[len(self.df)]
        )
        self.df = pd.concat([self.df, new_row], axis=0) \
            .sort_values('score', ascending=False) \
            .reset_index(drop=True)
        self.save()

    def save(self):
        self.df.to_csv(self.path)

    def get_str(self):
        tmp_df = self.df.head(10).copy()
        tmp_df['date'] = tmp_df['datetime'].dt.strftime('%Y-%m-%d %H:%M')
        # tmp_df = tmp_df.set_index('date')
        tmp_df = tmp_df[['name', 'date', 'player_level', 'score']]
        return tmp_df.to_string(index=False)
