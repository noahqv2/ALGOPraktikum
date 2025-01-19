import threading
import random
import time
import marketplace.users


class Simulator:
    def __init__(self):
        self.stop_simulation = False

    def place_random_bids(self, auctions, current_user_id, num_auctions=10):
        if self.stop_simulation:
            return

        users = auctions.users()
       # user_ids = [
       #     user_id
       #     for user_id in users.users
       #     if (print(f"Checking User ID: {user_id}"), user_id != current_user_id)[1]
       #     # Prints and checks if the user_id is not current_user_id
       # ]
        #print(f"Final user_ids: {user_ids}")  # Print the final list

        user_ids = [user_id for user_id in users.users if user_id != current_user_id]

        auctions._place_random_bids(num_auctions, user_ids, True, current_user_id)

    def create_random_auctions(self, auctions, current_user_id):
        if self.stop_simulation:
            return

        user_ids = [user_id for user_id in auctions.users().users if user_id != current_user_id]
        #user_ids = [user_id for user_id in users.users if user_id != current_user_id]
        for _ in range(5):
            random_user = random.choice(user_ids)
            item_name = "Kartoffelschäler"
            description = ""
            value_min = 1
            auctions.add_new_auction(random_user, item_name, description, value_min)

    def randomly_rate_users(self, users: marketplace.users.Users, current_user_id):
        if self.stop_simulation:
            return

        rated_users= []
        user_ids = [user_id for user_id in users.users if user_id != current_user_id]

        for _ in range(35):
            random_user = random.choice(user_ids)
            stars = random.randint(1,5)
            users.users.get(random_user).rate_user(stars)
            rated_users.append(random_user)

        return rated_users
    def stop(self):
        self.stop_simulation = True


