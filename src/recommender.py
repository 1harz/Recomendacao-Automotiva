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

    def build_user_item_matrix(self, df):
        pass

    def update_matrix(self, new_rating):
        pass

    def get_cold_start_recommendations(self):
        return ['popular_item_1', 'popular_item_2']

    def recommend(self, user_id: int):
        return self.get_cold_start_recommendations()
