import networkx as nx
import matplotlib.pyplot as plt
import random
import pickle
from operator import itemgetter

from flee import flee
from flee import properties
import numpy as np


def resillience(g) :
    score = 0
    attempts = 100
    for i in range(attempts) :
        g2 = g.copy()
        con = 1
        count = 0
        while con == 1 :
            g2 = modification(g2, 1, delete=True)
            con = nx.algorithms.node_connectivity(g2)
            count += 1

        score += count / attempts

    return score


def modification(graph, leng, delete=True) :
    if delete :
        edges = list(graph.edges)
        chosen_edge = random.choice(edges)
        graph.remove_edge(chosen_edge[0], chosen_edge[1])

    else :
        nonedges = list(nx.non_edges(graph))
        chosen_nonedge = random.choice(nonedges)
        graph.add_edge(chosen_nonedge[0], chosen_nonedge[1], len=leng)
        b, f = nx.check_planarity(graph)
        if not b :
            graph.remove_edge(chosen_nonedge[0], chosen_nonedge[1])

    return graph


def create_graph(N, E) :
    # Mix it up
    N = int(np.random.normal(N, 2))
    E = int(np.random.normal(E, 2))

    G = nx.Graph()
    G.add_nodes_from(np.arange(N))
    G_nodes = list(G.nodes())

    #     mu, sigma = 40., 1.5 # mean and standard deviation

    link_lengths = np.random.lognormal(2, 1, E) + 30

    for i in range(E) :
        G.add_edge(random.choice(G_nodes), random.choice(G_nodes), len=link_lengths[i])

    b = False
    while not b :
        mu = np.random.lognormal(2, 1) + 30
        G = modification(G, mu, delete=True)
        b, f = nx.check_planarity(G)

    G.remove_nodes_from(list(nx.isolates(G)))
    # Delete non-edges

    b = False
    for i in range(int(np.random.normal(10, 2))):
        mu = np.random.lognormal(2, 1) + 30
        G = modification(G, mu, delete=False)

    nx.draw(G, with_labels=True, font_weight='bold')

    print("Is planar - ", nx.check_planarity(G))

    return G


def lst_to_dict(lst) :
    res_dct = {lst[i][0] : lst[i][1] for i in range(0, len(lst), 1)}
    return res_dct


def location_types(graph, distr) :
    dict = {}

    degree_dict = lst_to_dict(list(G.degree))

    sorted_degree_dict = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)

    L = len(sorted_degree_dict)

    for i in range(L) :

        if i in np.arange(0, round(L * distr[0]), 1) :
            dict[sorted_degree_dict[i][0]] = "default"

        if i in np.arange(round(L * distr[0]), round(L * distr[0]) + round(L * distr[1]), 1) :
            dict[sorted_degree_dict[i][0]] = "conflict"

        if i in np.arange(round(L * distr[0]) + round(L * distr[1]), L, 1) :
            dict[sorted_degree_dict[i][0]] = "camp"

    nx.set_node_attributes(G, dict, "Location_type")

    return G


def make_model(g) :
    e = flee.Ecosystem()

    locations = []
    camp_loc = []
    camp_name = []

    for nr, n in enumerate(G2.nodes()) :

        style = G2.nodes[n]['Location_type']
        locations.append(e.addLocation(str(n), movechance=style, capacity=1, pop=1_000_000))

        if style == 'conflict' :
            e.add_conflict_zone(str(n))
        if style == 'camp' :
            camp_loc.append(nr)
            camp_name.append(str(n))

    # Add edges and their corresponding length
    for node0, node1 in g.edges:
        e.linkUp(str(node0), str(node1), g.edges[(node0, node1)]['len'])

    return e, locations, camp_name, camp_loc


def flow_for_fraction_release_in_t_limit(camp_name, FIXED_CAPACITY, t_limit, FRACTION ):
    return int(((len(camp_name) * FIXED_CAPACITY) / t_limit) * FRACTION)

class DataRun:

    def __init__(self, data_full, fraction):
        self.data_full = data_full
        self.fraction = fraction

        self.happend = False
        self.time = self.occurance()

    def occurance(self):
        '''
        Checks if and when the phase change happens
        Also sets happend to true if it finds it

        :return: time fraction of occuance of phase change or 1 if didnt happen
        '''
        for n, i in enumerate(self.data_full):
            if not i == 0:
                self.happend = True
                return (n + 1) / len(self.data_full)

        return 1

class DataTest:

    def __init__(self, data_list, n_camp, nodes, links, proper = {}):
        self.data_list = data_list
        self.properties = proper
        self.n_camp = n_camp
        self.nodes = nodes
        self.links = links

        self.moment = self.phase_change()
        self.angle = self.slope()

    def phase_change(self):
        '''
        When did the phase change happen, at which fraction
        :return: the fraction at which it happend
        '''
        for d in self.data_list:
            if d.happend:
                return d.fraction

    def slope(self):
        '''
        calculate the sloop: is it causing a cascading effect or not
        :return: slope calculated by lin regression
        '''
        items = []
        for d in self.data_list:
            if d.happend:
                items.append(d.time)

        x = np.array(items)
        y = np.arange(len(items))

        big_x = x - x.mean()
        big_y = y - y.mean()

        return (big_x.dot(big_y)) / (big_x.dot(big_x))


### SETTINGS #####################################
N = 20  # number of nodes
E = 40 # number of links
locations_distribution = [0.55, 0.25, 0.2]  # 45% of locations are hubs, 35% - conflict zones, 20 % camps
TOTAL_TIME = 100 # days of simulation
FIXED_CAPACITY = 2_000 # capacity of single camp
FIXED_LIMIT = FIXED_CAPACITY * 0.99 # What is full
t_limit = 10 # Days to release all refugees
# FRACTION = 1 # How much of limit of refugees do wwe release

if __name__ == '__main__':
    all_data = []

    for test in range(1000):
        print("TEST NUMBER:", test)
        # Create Graph
        G = create_graph(N, E)
        G2 = location_types(graph=G, distr=locations_distribution)

        try:
            test_data = []
            for graph_test in range(1, 21):
                print("GRAPH TEST:", graph_test)
                FRACTION = 0.05 * graph_test

                # Make model and set flow
                e, locations, camp_name, camp_locations = make_model(G2)
                FIX_REFRUGEE_FLOW = flow_for_fraction_release_in_t_limit(camp_name, FIXED_CAPACITY, t_limit, FRACTION )

                # Determine capacity
                for nr in camp_locations :
                    locations[nr].capacity = FIXED_CAPACITY

                # reset refs
                refugee_debt = 0
                refugees_raw = 0

                # Start Simulating
                data_full = []
                for t in range(0, TOTAL_TIME) :
                    # Check amount of refugees
                    new = FIX_REFRUGEE_FLOW if t < t_limit else 0

                    # Add them
                    e.add_agents_to_conflict_zones(new)

                    # Track total amount of refs
                    refugees_raw += new

                    # Propagate the model by one time step.
                    e.evolve()

                    # Check for full camps
                    full = 0
                    for nr in camp_locations :
                        if locations[nr].numAgents > FIXED_LIMIT :
                            full += 1

                    # Save single data point
                    data_full.append(full)

                # Save single simulation
                test_data.append(DataRun(data_full, FRACTION))

            # Save entire test
            conflicts = []
            for conflict in e.conflict_zones :
                conflicts.append(conflict.name)

            prop = properties.get_properties(locations, camp_name, conflicts, e.export_graph(False)[1])
            prop['resillience'] = resillience(G2)

            print('properties:', prop)
            all_data.append(DataTest(test_data, len(camp_name), len(G2.nodes), len(G2.edges), prop))
            pickle.dump(all_data, open('output\\RUN_DATA_100_more_random.p', 'wb'))
        except:
            pass

