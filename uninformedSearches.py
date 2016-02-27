import pprint
from copy import deepcopy


class Graph:
    """
    Graph Class represents all variations of the Graph Data Structure in the form of a dictionary
    Weighted/Uniform paths, Directed/Bi-directional Graphs
    Ex: Directed path from node 'A' to 'B' with path cost 'c' is represented as follows:
            Graph = {
                        'A' : [('B', c)]
                    }
    """

    def __init__(self, graph_dict={}):
        """
        Initializes the dictionary
        :param graph_dict: A predefined dictionary mapping can be provided as an input.
                            In default case an empty dictionary is initialized.
        """
        self.__graph_dict = graph_dict

    def create_node(self, nodeID):
        """
        To create a new node on the graph.
        Inserts the new node as a key to the graph and initializes it to an empty list.
        :param nodeID: Identifier of the new node.
        """
        if nodeID.title() not in self.__graph_dict.keys():
            self.__graph_dict[nodeID.title()] = []

    def create_arc(self, origin, destination, cost=1):
        """
        Inserts a directed(uni-directional) path from origin to destination to the graph.
        :param origin: Identifier of the origin node
        :param destination: Identifier of the origin node
        :param cost: Cost of the path. By default the cost is initialized to 1.
        """
        if origin.title() not in self.__graph_dict:
            self.create_node(origin.title())
        if destination.title() not in self.__graph_dict[origin.title()]:
            self.__graph_dict[origin.title()].append((destination.title(), int(cost)))

    def create_edge(self, origin, destination, cost=1):

        """
        Inserts a bi-directional path from origin to destination to the graph.
        :param origin: Identifier of one node.
        :param destination: Identifier of the other node.
        :param cost: Cost of the path. By default the cost is initialized to 1.
        """
        if origin not in self.__graph_dict:
            self.create_node(origin)
        if destination not in self.__graph_dict:
            self.create_node(destination)

        self.create_arc(origin, destination, cost)
        self.create_arc(destination, origin, cost)

    def get_graph_nodes(self):
        """
        :return: Returns a list of all the nodes in the Graph
        """
        return deepcopy(list(self.__graph_dict.keys()))

    def get_graph_dict(self):
        """
        :return: Returns the entire Graph as a dictionary
        """
        return deepcopy(self.__graph_dict)


class Node:
    """
    Node class is the atomic part of a tree.
    """
    def __init__(self, node_identifier, parent=None, edge_cost=0):
        """
        self.__total_path_cost is cost from the root node to the current node.
        :param node_identifier: Identifier of the node
        :param parent: Reference to the parent node.
        :param edge_cost: Is the path cost from parent to current node.
        """
        self.__node_identifier = node_identifier
        self.__parent = parent
        try:
            self.__total_path_cost = int(parent.get_total_cost()) + edge_cost
        except AttributeError:
            self.__total_path_cost = int(edge_cost)

    def get_node_identifier(self):
        """
        :return: Returns the node identifier
        """
        return self.__node_identifier

    def get_parent(self):
        """
        :return: Returns reference to the parent of the current node
        """
        return self.__parent

    def add_child_node(self, child_node_identifier, cost_to_reach_child_node):
        """
        :param child_node_identifier: Identifier of the child node
        :param cost_to_reach_child_node: Path cost from parent to child node
        :return: Returns the reference of the child node generated
        """
        child_node = Node(child_node_identifier, self, cost_to_reach_child_node)
        return child_node

    def get_total_cost(self):
        """
        :return: Returns the total path cost from root node to current node.
        """
        return self.__total_path_cost


def read_file_data(file_name):
    """
    Reads path data from text. Each path is present line after line in the input file.
    A sample route is represented as follows: Arad,Zerind,75
    :param file_name:
    :return: Returns a list of routes. Each route is returned as a list of 3 items.
                route: ['city1', 'city2', 'path cost']
    """
    file_reference = open(file_name, 'r')
    file_data = []
    while True:
        edge = file_reference.readline()
        if edge:
            file_data.append(edge.strip().split(','))
        else:
            file_reference.close()
            break
    return file_data


def retrace_path(dest_node):
    """
    Retraces path from current node to the root node.
    :param dest_node: THe node from which the path has to be retraced
    :return: returns a string of all cities travelled, along with the total path.
    """
    traced_route = []
    current_node = dest_node
    while current_node:
        traced_route.insert(0, current_node.get_node_identifier())
        current_node = current_node.get_parent()

    if traced_route:
        return str(', '.join(traced_route)) + '\nTotal Path cost: ' + str(dest_node.get_total_cost())
    else:
        return "Path could not be retraced."


def breadth_first_search(graph, origin, destination):
    """
    :param graph: A dictionary representing the graph of interest
    :param origin:
    :param destination:
    :return: Returns the path traversed from the origin to destination along with the cost of total path covered.
    """
    origin = origin.title()
    destination = destination.title()

    if origin == destination:
        return "Source and Destination cannot be same."

    graph_dict = graph.get_graph_dict()
    graph_nodes = graph.get_graph_nodes()
    if origin not in graph_nodes:
        return "Unable to find 'Source City' in the map."
    if destination not in graph_nodes:
        return "Unable to find 'Destination City' in the map."

    root = Node(origin)
    # print root.get_node_identifier(), root.get_parent()
    visited_nodes = dict(zip(graph_nodes, [False] * len(graph_nodes)))
    queue = [root]
    while queue:

        current_node = queue.pop(0)
        # print(current_node.get_node_identifier())
        # print(current_node.get_total_cost())

        if visited_nodes[current_node.get_node_identifier()]:
            continue
        else:
            visited_nodes[current_node.get_node_identifier()] = True

        if graph_dict[current_node.get_node_identifier()]:
            for child_id in graph_dict[current_node.get_node_identifier()]:
                child = current_node.add_child_node(*child_id)
                # print(child.get_node_identifier())
                # print(child.get_total_cost())
                # print('------------')
                # goal test when child is created
                if child.get_node_identifier() == destination:
                    return retrace_path(child)
                else:
                    # print([city.get_node_identifier() for city in queue])
                    if child not in [city.get_node_identifier() for city in queue] \
                            and not visited_nodes[child.get_node_identifier()]:
                        queue.append(child)

    return "Path not found"


def depth_first_search(graph, origin, destination):
    """
    :param graph: A dictionary representing the graph of interest
    :param origin:
    :param destination:
    :return: Returns the path traversed from the origin to destination along with the cost of total path covered.
    """
    origin = origin.title()
    destination = destination.title()

    if origin == destination:
        return "Source and Destination cannot be same."

    graph_dict = graph.get_graph_dict()
    graph_nodes = graph.get_graph_nodes()
    if origin not in graph_nodes:
        return "Unable to find 'Source City' in the map."
    if destination not in graph_nodes:
        return "Unable to find 'Destination City' in the map."

    root = Node(origin)
    # print root.get_node_identifier(), root.get_parent()
    visited_nodes = dict(zip(graph_nodes, [False] * len(graph_nodes)))
    stack = [root]

    while stack:
        current_node = stack.pop()
        # print(current_node.get_node_identifier())

        if visited_nodes[current_node.get_node_identifier()]:
            continue
        else:
            visited_nodes[current_node.get_node_identifier()] = True
        # print(current_node.get_node_identifier())
        # print(current_node.get_total_cost())

        if graph_dict[current_node.get_node_identifier()]:
            for child_id in graph_dict[current_node.get_node_identifier()]:
                child = current_node.add_child_node(*child_id)
                # print(child.get_node_identifier())
                # print(child.get_total_cost())
                # print('------------')
                # goal test when child is created
                if child.get_node_identifier() == destination:
                    return retrace_path(child)
                else:
                    if child not in [city.get_node_identifier() for city in stack] \
                            and not visited_nodes[child.get_node_identifier()]:
                        # if child not in [city.get_node_identifier() for city in stack]:
                        stack.append(child)

    return "Path not found"


def recursive_dls(graph, current_node, destination, depth_limit):
    # print current_node.get_node_identifier(), depth_limit
    if current_node.get_node_identifier() == destination:
        return retrace_path(current_node)
    elif depth_limit == 0:
        return False
    else:
        graph_dict = graph.get_graph_dict()
        cutoff_occurred = False
        for child_id in graph_dict[current_node.get_node_identifier()]:
            child_node = current_node.add_child_node(*child_id)
            result = recursive_dls(graph, child_node, destination, depth_limit - 1)
            if not result:
                cutoff_occurred = True
            else:
                return result
        if cutoff_occurred:
            return False


def depth_limited_search(graph, origin, destination, depth_limit):
    """
    :param graph: A dictionary representing the graph of interest
    :param origin:
    :param destination:
    :param depth_limit: Maximum depth till which the tree can expand
    :return: Returns the path traversed from the origin to destination along with the cost of total path covered.
    """
    origin = origin.title()
    destination = destination.title()

    if origin == destination:
        return "Source and Destination cannot be same."

    graph_dict = graph.get_graph_dict()
    graph_nodes = graph.get_graph_nodes()
    if origin not in graph_nodes:
        return "Unable to find 'Source City' in the map."
    if destination not in graph_nodes:
        return "Unable to find 'Destination City' in the map."

    return recursive_dls(graph, Node(origin), destination, depth_limit)


def iterative_deepening_search(graph, origin, destination, step_size=1):
    """
    :param graph: A dictionary representing the graph of interest
    :param origin:
    :param destination:
    :param step_size: Size of the step to be taken.
    :return: Returns the path traversed from the origin to destination along with the cost of total path covered.
    """
    origin = origin.title()
    destination = destination.title()

    if destination == origin:
        return "Source and Destination cannot be same."

    graph_dict = graph.get_graph_dict()
    graph_nodes = graph.get_graph_nodes()
    if origin not in graph_nodes:
        return "Unable to find 'Source City' in the map."
    if destination not in graph_nodes:
        return "Unable to find 'Destination City' in the map."

    depth_limit = 0
    while True:
        path = depth_limited_search(graph, origin, destination, depth_limit)
        if path:
            return path
        else:
            # print "-------------------------"
            depth_limit += step_size


# Main program
if __name__ == "__main__":
    input_file_name = 'route_PA1.csv'
    input_data = read_file_data(input_file_name)
    # print(input_data)
    
    city_map = Graph()
    for route in input_data:
        city_map.create_edge(*route)
    
    # pprint.pprint(city_map.get_graph_dict())
    # pprint.pprint(city_map.get_graph_nodes())
    
    # bfs_route = breadth_first_search(city_map, 'Neamt', "Oradea")
    
    while True:
        print("\n\n-------------------------------------------------\n")
        origin_city = raw_input('Enter name of the city of origin: ')
        destination_city = raw_input('Enter name of the destination city: ')
        selected_search_algorithm = raw_input('Select an algorithm. (Enter option number)\n\
    1. Breadth First Search\n2. Depth First Search\n3. Iterative Deepening Search\nEnter your choice:\t ')
    
        if int(selected_search_algorithm) == 1:
            bfs_route = breadth_first_search(city_map, origin_city.strip().title(), destination_city.strip().title())
            print "\nBFS Route:\t" + bfs_route + "\n"
        elif int(selected_search_algorithm) == 2:
            dfs_route = depth_first_search(city_map, origin_city.strip().title(), destination_city.strip().title())
            print "\nDFS Route: \t" + dfs_route + "\n"
        elif int(selected_search_algorithm) == 3:
            step_size = raw_input('Enter step size for iterative deepening: ')
            ids_route = iterative_deepening_search(city_map, origin_city.strip().title(), destination_city.strip().title(), int(step_size))
            print "\nIterative Deep Search Route: \t" + ids_route + "\n"
        else:
            print "Select valid options\n"
    
        exit_key = raw_input("Do you want to continue (y/n): ")
        if exit_key.lower() != 'y':
            break
