# Status: FINAL, dgaida2, 15.10.2024

# definiert die Klasse Users.
# Users ist eine Menge von disjunkten Mengen (nur für drittes Praktikum) von der Klasse User,
# damit man Users in Praktikumsgruppen einsortieren kann. Für das erste und zweite Praktikum ist die Klasse
# Praktikumsgruppe lediglich ein Dictionary
# in der Klasse werden die csv-Dateien user.csv und friends.csv gelesen.

import csv
import marketplace.user
import marketplace.praktikumsgruppen
import osmnx as ox
map_graph = ox.graph.graph_from_address('Gummersbach, Steinmüllerallee 1, Germany', dist=5000,network_type='bike')
origin_point = (50.985108, 7.542490)  # Breiten- und Längengrad
destination_point = (51.022255, 7.562705)
origin = ox.distance.nearest_nodes(map_graph, origin_point[1], origin_point[0])
destination = ox.distance.nearest_nodes(map_graph, destination_point[1], destination_point[0])
shortest_path = ox.routing.shortest_path(map_graph, origin, destination, weight='length')

import networkx as nx


class Users(marketplace.praktikumsgruppen.Praktikumsgruppen):
    # *** CONSTRUCTORS ***
    def __init__(self, csvfile, *args):
        self.users={}
        #self.parent=self

        #self.weight=1
        super().__init__()

        self._read_users_from_csvfile(csvfile)

        self._read_friends_csv('friends.csv')


        # erstelle Praktikumsgruppen als Menge disjunkter Mengen bzw. als dictionary (1. und 2. Praktikum)

        super().create_groups(list(self.users.keys()), self._groupnumbers)

    # *** PUBLIC SET methods ***

    # *** PUBLIC methods ***
    def get_user(self,user_id):
        return self.users.get(user_id)

    def add(self, user_id, password, name_family="", name_first="", gps_coord=(None, None), address=""):
        """
        Adds the given user with the user_id to the dictionary that the Users parent class Praktikumsgruppen is
        inheriting from
        :param user_id: user id of user
        :param password: password of user
        :param name_family: family name of user
        :param name_first: first name of user
        :param gps_coord: Tuple with Längen- und Breitengrad des erfundenen Wohnorts des Nutzers
        :param address: String mit Adresse die zu GPS Koordinaten gehört
        """
        self.users[user_id] = marketplace.user.User(user_id, password, name_family, name_first, gps_coord, address)


    def calc_distance_between_users(self, user_id1, user_id2):
        # TODO for students: calculate distance between gps coordinates of user1 and user2 using a map and an
         # algorithm that calculates the shortest distance on the map
        distance=0.0
        if map_graph is None:
            print("Graph konnte nicht geladen werden")
            return None
        try:
            user1 = self.users.get(user_id1)
            user2 = self.users.get(user_id2)
            if not user1 or user2:
                print("one or both not found")
                return 10000

            #point1 = user1.gps_coord or (ox.geocode(user1.address) if user1.address else None)
            point1=user1.gps_coord
            if point1 is None and user1.address:
                point1 = user1.gps_coord

            if point1 is None:
                print("could not get coordinates point1")
                return 10000
            #point2 = user2.gps_coord or (ox.geocode(user2.address) if user2.address else None)
            point2 = user2.gps_coord
            if point2 is None and user2.address:
                point2 = user2.gps_coord

            if point2 is None:
                print("could not get coordinates for point2")
                return 10000
            node1=ox.distance.nearest_nodes(map_graph, point1[1], point1[0])
            node2=ox.distance.nearest_nodes(map_graph, point2[1], point2[0])
            route=nx.shortest_path(map_graph, node1,node2,weight='length')
            print(route)
            distance=nx.path_weight(map_graph, route, weight='length')
            print(distance)
            return distance
        except Exception as e:
            print(f"error:{e}")
        # TODO for students: replace this naive implementation of distance manhattan with distance gotten
        #  from graph algorithm
        #distance=nx.path_weight(map_graph, route,)

        #distance = sum(abs(a - b) for a, b in zip(user1.gps_coords(), user2.gps_coords()))

        return distance

    # *** PUBLIC GET methods ***

    def get_name_of_user(self, user_id):
        node = self[user_id]
        return node.name()

    def num_users(self):
        return len(self.users.keys())

    def password_valid(self, user_id, password):
        return self.users.get(user_id).password_valid(password)

    def get_user_pretty_print_for_list(self, user_id):
        return (self.users.get(user_id).pretty_print() + "\t in Praktikumsgruppe repräsentiert durch: " +
                self.find_byid(user_id, True))

    def get_friends_andgroupmembers_pretty_print(self, user_id):
        """
        Returns list of friends and group members for the given user_id that is shown on GUI.

        :param user_id: usually the current user id
        :return:
        """
        friends = self.users.get(user_id).friends()

        friend_names = [self.get_user_pretty_print_for_list(friend) for friend in friends]

        group_members = self.get_groupmembers(user_id)
        
        if group_members is None:
            return friend_names

        # entferne mich selbst aus der Gruppe, da ich ja weiß, dass ich (user_id) in der Gruppe bin
        group_members.remove(user_id)

        group_members_pp = [self.get_user_pretty_print_for_list(member) for member in group_members]

        return friend_names + group_members_pp

    def get_mutual_friends(self, user_id):
        """

        :param user_id: usually the current user id
        :return: dictionary with friends of the friends of given user_id together with the information with how
        many friends of user_id these friends are friends with
        """
        friends = self.users.get(user_id).friends()
        mutual_friends_count = {}

        for friend in friends:
            friend_friends = self.users.get(friend).friends()
            for mutual_friend in friend_friends:
                if mutual_friend != user_id and mutual_friend not in friends:
                    if mutual_friend in mutual_friends_count:
                        mutual_friends_count[mutual_friend] += 1
                    else:
                        mutual_friends_count[mutual_friend] = 1

        return mutual_friends_count

    def suggest_friends(self, user_id, num_common_friends=2, distance_threshold=0.1, pretty_print=True):
        """
        Suggests users to the given user_id that
        (1) are friends with at least num_common_friends friends of user_id or
        (2) that live nearby the given user_id (closer as distance_threshold) and are friends of friends of friends...
        (see are_users_connected())

        :param user_id: usually the current user id
        :param num_common_friends: only suggest users that are at least friends with two of the user_ids friends
        :param distance_threshold: only suggest users that live closer to the given user_id as this threshold value
        :param pretty_print: if True, then call pretty_print() on all suggested friends before returning them
        :return: list of suggested friends. the first part of the list should contain common friends, ordered
        so that users with maximum number of common friends appear first. the second part of the list should
        contain all users that live close by, again sorted, so that the direct neighbour comes first.
        """
        mutual_friends_count = self.get_mutual_friends(user_id)
        # TODO for students: Implement this method by filling the list suggested_friends
        suggested_friends = []
        close_and_connected_friends = []
        #print("mututal_friend_count")
        #print( mutual_friends_count)
        #print(f"printing self.keys {self.keys()}")
        for other_user_id in self.users:
            if other_user_id == user_id:
                continue
            if distance_threshold > self.calc_distance_between_users(other_user_id, user_id):
                if self.are_users_connected(user_id, other_user_id):
                    close_and_connected_friends.append(other_user_id)
            elif other_user_id in mutual_friends_count:
                if mutual_friends_count[other_user_id] >= num_common_friends:
                    suggested_friends.append(other_user_id)
                #print(f"inside elif{suggested_friends}")
            else:
                print(f"friend {other_user_id} in mutual friends list.\n")

        friends_and_group_members = self.get_friends_andgroupmembers_pretty_print(user_id)

        # Extract user IDs from pretty printed strings if necessary
        friends_and_group_member_ids = []
        if friends_and_group_members and isinstance(friends_and_group_members[0],
                                                    str):  # Check if it's a list of strings
            import re  # Needed to import re for regex
            for member_str in friends_and_group_members:
                match = re.search(r"GM-ID: (\w+)", member_str)  # Extract GM-ID using regex
                if match:
                    friends_and_group_member_ids.append(match.group(1))
        else:  # if it is not a string, then it is a list of user_ids
            friends_and_group_member_ids = friends_and_group_members

        # Filter suggested friends
        suggested_friends_filtered = []
        for friend_id in suggested_friends:
            if isinstance(friend_id, str):
                match = re.search(r"GM-ID: (\w+)", friend_id)  # Extract GM-ID using regex
                if match:
                    friend_id = match.group(1)
                else:
                    continue  # if it is not a valid string, then continue
            if friend_id not in friends_and_group_member_ids:
                suggested_friends_filtered.append(friend_id)

        # Filter close and connected friends
        close_and_connected_friends_filtered = []
        for friend_id in close_and_connected_friends:
            if isinstance(friend_id, str):
                match = re.search(r"GM-ID: (\w+)", friend_id)  # Extract GM-ID using regex
                if match:
                    friend_id = match.group(1)
                else:
                    continue  # if it is not a valid string, then continue
            if friend_id not in friends_and_group_member_ids:
                close_and_connected_friends_filtered.append(friend_id)

        if pretty_print:
            suggested_friends_filtered = [self.users.get(friend).pretty_print() for friend in suggested_friends_filtered]
            close_and_connected_friends_filtered = [self.users.get(friend).pretty_print() for friend in close_and_connected_friends_filtered]

        return suggested_friends_filtered + close_and_connected_friends_filtered
        #return suggested_friends + close_and_connected_friends

    def are_users_connected(self, user_id1, user_id2, degree=3):
        """
        :param user_id1: a user that we are searching a friend for
        :param user_id2: another user, where we want to check whether it is somehow friends with user_id1 over some
        other shared friends
        :param degree: only look for possible friend connections up to this degree of friendship
        :return: True, if user_id1 and user_id2 are friends over some edges up to the given degree, else False
        """

        if user_id1 not in self.users or user_id2 not in self.users:
            print("returning false")
            return False
        # TODO for students: Implement this method


        all_users= set()
        all_users.add(user_id1)
        all_users.add(user_id2)

        queue= [user_id1]
        visited= {user_id1}
        current_degree = 0
        while queue and current_degree <= degree:
            next_level = []
            for user in queue:
                friends=self.get_mutual_friends(user)
                for friend in friends:
                    if friend not in visited:
                        all_users.add(friend)
                        next_level.append(friend)
                        visited.add(friend)
            queue=next_level
            current_degree += 1

        for user in all_users:
            friends=self.get_mutual_friends(user)
            for friend in friends:
                if friend in all_users:
                    self.union(user, friend)

       # print(f"printing return inside are_users_connected {self.find(parent, user_id1)==self.find(parent, user_id2)}")
        return self.find( user_id1)==self.find( user_id2)

    # *** PUBLIC STATIC methods ***

    def find(self,parent):
        return super().find(parent)

    def union(self,parent,weight):
        super().union(parent,weight)




    # *** PRIVATE methods ***

    def _read_users_from_csvfile(self, csvfile):
        """
        Read the given csvfile that contains all students that want to do the Praktikum in this semester
        including their GM-ID, Names and number of their Praktikumsgruppe

        :param csvfile: csv file that has to be created at the beginning of the semester containing all students
        in this semester
        """
        with open(csvfile, newline='', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            # Skip header row
            next(csvreader)

            # private member variable containing the Praktikumsgruppe number of the students in the order that the
            # students are read from the csv file
            self._groupnumbers = []

            for row in csvreader:
                user_id, name_family, name_first, password, groupnum, gps_coords, address = row
                # macht aus String wieder das Tuple mit long und lat Koordinaten
                gps_coords = eval(gps_coords)
                self.add(user_id, password, name_family, name_first, gps_coords, address)
                self._groupnumbers.append(groupnum)

    def _read_friends_csv(self, file_path):
        """
        Funktion, um die friends.csv-Datei einzulesen und ein Dictionary zu erstellen
        :param file_path: path to friends.csv file
        """
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Überspringe die Header-Zeile
            for row in csvreader:
                user_id = row[0]
                friends = row[1].split(', ')
                #self[user_id].friends_add_list(friends)
                user=self.users.get(user_id)
               # for friend in friends:  # gehe alle Freunde durch und füge user_id ebenfalls als Freund hinzu
                #    self[friend].friends_add(user_id)
                if user:
                    user.friends_add_list(friends)
                    for friend in friends:
                        friend_user = self.users.get(friend)
                        if friend_user:
                            friend_user.friends_add(user_id)
                        else:
                            print("")
                else:
                    print("")


    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
