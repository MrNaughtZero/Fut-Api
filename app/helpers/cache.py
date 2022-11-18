from app import cache

class DeleteCache:
    def __init__(self):
        self.cache_list = []
        self.update_players_cache()

    def update_players_cache(self):
        for k in cache.cache._cache:
            if "players" or "players/" in k:
                cache.delete(k)
                    


    