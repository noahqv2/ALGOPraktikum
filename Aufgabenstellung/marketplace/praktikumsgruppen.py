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
    def __init__(self,user_id):
        """
        Initializes a new SetNode.
        """
        # TODO: werden nur für Praktikum 3 benötigt
        self.user_id=user_id
        self.parent = self
        self.weight = 1
        
   # _praktikumsgruppe = None

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
    def create_groups(self, user_ids, groupnumbers):
        """
        Creates groups from the provided user IDs and group numbers.
        Args:
        user_ids (list): A list of user IDs.
        groupnumbers (list): A list of group numbers corresponding to the user IDs.
        """

        for user_id, group_number in zip(user_ids, groupnumbers):
            if user_id not in self._groups:
                self._groups[user_id] = SetNode(user_id)
        for user_id, group_number in zip(user_ids, groupnumbers):
                for other_user_id, other_group_number in zip(user_ids, groupnumbers):
                    if group_number == other_group_number and user_id != other_user_id:
                        self.union(user_id, other_user_id)
                # self._groups.setdefault(group_number, []).append(user_id)

    #        print(self._groups) #DEBUG
    #        new_userid_list = []
    #        for group_id, group_members in self._groups.items():
    #            print(group_members)
    #            if "nasemota" in group_members:
    #                for member in group_members:
    #                    new_userid_list.append(member)
    #                break
    #        print (new_userid_list)

    # TODO in Praktikum 3: implement find(node), find_byid(user_id, return_id=False) and
    #  union(user_id1, user_id2)
    def find(self, user_id):
       #node = self._groups[user_id]
       #if node.parent[user_id] == self:
       #    return node
       #node.parent=self.find(node.parent.user_id)
       #return node.parent



        if user_id not in self._groups:
            return None
        node=self._groups[user_id]
        root=node
        while root.parent != root:
            root=root.parent

        while node != root:
            next_node=node.parent
            node.parent=root
            node=next_node
        return root

    def union(self,user_id1, user_id2):
        root1 = self.find(user_id1)
        root2 = self.find(user_id2)

        if root1.weight < root2.weight:
            root1.parent = root2
            root2.weight += root1.weight
        else:
            root2.parent = root1
            root1.weight += root2.weight



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
        root_node = self.find(user_id)

        if root_node is None:
            return None

        if return_id:
            return root_node.user_id
        else:
            return root_node



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
        node = self._groups.get(user_id)
        if node is None:
            return []
        root = self.find(node)
        return [value.user_id for value in self._groups.values() if self.find(value)==root]


    # *** PUBLIC STATIC methods ***


    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***

















