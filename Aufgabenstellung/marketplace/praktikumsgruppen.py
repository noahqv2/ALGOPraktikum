    # Definiert die Klassen Praktikumsgruppen und SetNode, implementiert als Dictionary

# marketplace.users erbt von marketplace.user und marketplace.user erbt von marketplace.praktikumsgruppen (folglich erbt users auch praktikumsgruppen)
# Strukturiert ist marketplace.praktikumsgruppen > marketplace.user > marketplace.users

# Die Nutzer des Marketplaces sind in einem Dictionary gespeichert.

class SetNode:
    """
    TODO for students: die Klasse user.User erbt von SetNode. diese Klasse wird eigentlich erst in Praktikum 3 benötigt.
    für Praktikum 1 und 2 müsste User nicht von dieser Klasse erben
    Class representing a node in a disjoint set (union-find) structure.

    Attributes:
        _parent (SetNode): The parent node in the union-find structure.
        _weight (int): The weight (number of nodes) of the (sub-)tree rooted in the current node.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new SetNode.
        """
        # TODO: werden nur für Praktikum 3 benötigt
        self._parent = self  # parent Knoten des SetNode Objekts. self bedeutet, dass der Knoten ein Wurzelknoten ist
        self._weight = 1  # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist
        
    _praktikumsgruppe = None

    # *** PUBLIC SET methods ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

    # *** PUBLIC methods to return class properties ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden


class Praktikumsgruppen(dict):
    """
    In Praktikum 1 und 2: Dictionary containing all students. Die Klasse user.Users erbt von dieser Klasse.
    In Praktikum 3: Class representing a collection of disjoint sets for grouping users into practical groups.

    Methods:
        find(node): Finds the root of the set containing the node, with path compression.
        find_byid(user_id, return_id=False): Finds the root of the set containing the user by ID.
        union(user_id1, user_id2): Unions the sets containing the two users.
        create_groups(user_ids, groupnumbers): Creates groups from the provided user IDs and group numbers.
        get_groupmembers(user_id): Gets the members of the group containing the user.
        print_ds(): Prints the disjoint set structure.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new Praktikumsgruppen object.
        """
        super().__init__()
        self._groups = {}
    # *** PUBLIC methods ***

    # TODO in Praktikum 3: implement find(node), find_byid(user_id, return_id=False) and
    #  union(user_id1, user_id2)

    # die Methode existiert nur aus Kompatibilitätsgründen und wird im 3. Praktikum implementiert
    def find_byid(self, user_id, return_id=False):
        """
        Finds the root of the set (Praktikumsgruppe) containing the user by ID.

        Args:
            user_id (str): The ID of the user.
            return_id (bool): Whether to return the ID of the root node (True) or the root node itself (False, default).

        Returns:
            SetNode or str: The root node or its ID, depending on return_id.
        """

        return user_id

    def create_groups(self, user_ids, groupnumbers):
        """
        Creates groups from the provided user IDs and group numbers.

        Args:
            user_ids (list): A list of user IDs.
            groupnumbers (list): A list of group numbers corresponding to the user IDs.
        """

        for user_id, group_number in zip(user_ids, groupnumbers):
            self._groups.setdefault(group_number, []).append(user_id)

#        print(self._groups) #DEBUG
#        new_userid_list = []
#        for group_id, group_members in self._groups.items():
#            print(group_members)
#            if "nasemota" in group_members:
#                for member in group_members:
#                    new_userid_list.append(member)
#                break
#        print (new_userid_list)

    # *** PUBLIC GET methods ***

    def get_groupmembers(self, user_id):
        """
        Gets the members of the group containing the user.
        f(n) is in O(n)

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of user IDs in the same group.
        """
        new_userid_list = []                                    # +1
        for group_num,group_members in self._groups.items():    # +3        } 115 & 116 n-mal
            if user_id in group_members:                        # +5        }
                for member in group_members:                    # +1        } group_members hat genau 4 mitglieder
                    new_userid_list.append(member)              # +1*4      }
                break                                           # +1
        return new_userid_list                                  # +1


    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
