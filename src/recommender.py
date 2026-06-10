import pandas as pd

class RecommenderSystem:
    def __init__(self):
        pass

    async def load_data(self, csv_path: str):
        return pd.read_csv(csv_path)

    def clean_data(self, df):
        return df.dropna()

    def compute_cosine_similarity(self, matrix):
        pass
