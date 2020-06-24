"""
Functions to get certain properties of a network
"""
from flee import flee_sanne

def dijkstra(locations, camp, conflict):
    """
    Dijkstra algortihm to find the shortest path between a camp and a conflict
    """
    goal_reached = False
    # print(camp, conflict)

    unvisited = locations.copy()
    tentative = {}
    for location in locations:
        if location.name == camp:
            visited = [location]
        elif location.name == conflict:
            tentative[location] = 10000
            goal = location
        else:
            tentative[location] = 10000
    current = visited[0]
    current_dist = 0

    while goal_reached == False:

        links = current.links
        for link in links:
            end = link.endpoint
            start = link.startpoint
            # print(start.name, end.name, link.distance)

            if start == current and (end in tentative.keys()):
                distance = link.distance + current_dist
                if distance < tentative[end]:
                    tentative[end] = distance
                if tentative[goal] < 10000:
                    goal_reached = True

        # update current node, tentative, visited and unvisited
        current = min(tentative, key=tentative.get)
        current_dist = tentative[current]
        if current != goal:
            tentative.pop(current)
        visited.append(current)
        unvisited.remove(current)

    return tentative[goal]

def get_properties(locations, camps, conflicts, connection):
    """
    Get properties of the networks
    """

    prop_dict = {}

    distances = []
    for location in locations:
        links = location.links
        for link in links:
            distances.append(link.distance)
            # print(link.startpoint.name, link.endpoint.name, link.distance)

    # print maxium, minimum and average weight of the links
    # print("max dist", max(distances))
    # print("min dist", min(distances))
    # print("av dist", (sum(distances) / 2) / len(distances))
    prop_dict["max_dist"] = [max(distances)]
    prop_dict["min_dist"] = [min(distances)]
    prop_dict["av_dist"] = [(sum(distances) / 2) / len(distances)]


    # perform Dijkstra algorithm for all camp - conflict combinations
    paths = []
    for camp in camps:
        for conflict in conflicts:
            path = dijkstra(locations, camp, conflict)
            paths.append(path)

    # print average shortes path length and diameter
    # print("av path", sum(paths) / len(paths))
    # print("diameter", max(paths))

    prop_dict["av_path"] = sum(paths) / len(paths)
    prop_dict["diameter"] = max(paths)

    locations2 = []
    for l in locations:
        locations2.append(l.name)
    camp_degree = cal_degree(camps, conflicts, locations2, connection, 'camp')

    conflict_degree = cal_degree(camps, conflicts, locations2, connection, 'con_zone')

    hub_degree = cal_degree(camps, conflicts, locations2, connection, 'hub')

    total_degree = [camp_degree[0], conflict_degree[0], hub_degree[0]]
    avg_degree = [camp_degree[1], conflict_degree[1], hub_degree[1]]
    # print('total degree is {}'.format(len(connection)/2))
    # print('total_degree for camp, conflict, hub = {}'.format(total_degree))
    # print('avg degree for camp, conflict, hub = {}'.format(avg_degree))

    prop_dict["tot_degree"] = [len(connection)/2]
    prop_dict["tot_degree_type"] = total_degree
    prop_dict["av_degree_type"] = avg_degree


    list_neighbors = list_of_neighbors(locations2, connection)
    clus_coef_out = clus_coef(list_neighbors, connection, locations2, camps, conflicts)
    avg_clus_coef = clus_coef_out[1:][:-1]
    clus_coef_tot = clus_coef_out[-1]

    # print('avg clus_coef for camp, conflict, hub = {}'.format(avg_clus_coef))

    prop_dict["clus_coef_type"] = avg_clus_coef
    prop_dict["clus_coef_tot"] = clus_coef_tot

    return prop_dict

# ============== PANS CODE ============================

# this is the vertices and nodes connection list: connection = e.export_graph(False)[1]

def cal_degree(camp, conflict, locations, connection, city_type):

    ''' This function calculate the number of degree for three categories of cities
    The output is a list where the first one is the total degree and the second one is the average degree'''


    if city_type == 'camp':
        num_link = 0
        checked = []
        for i in camp:
            checked.append(i)
            for j in connection:
                if i == j[0]:
                    if j[1] not in checked:
                        num_link += 1
        return num_link, num_link/len(camp)
    elif city_type == 'con_zone':
        num_link = 0
        checked = []
        for i in conflict:
            checked.append(i)
            for j in connection:
                if i == j[0]:
                    if j[1] not in checked:
                        num_link += 1
        return num_link, num_link/len(conflict)
    else:
        num_link = 0
        checked = []
        rest = [x for x in locations if x not in camp+conflict]
        for i in rest:
            checked.append(i)
            for j in connection:
                if i == j[0]:
                    if j[1] not in checked:
                        num_link += 1
        return num_link, num_link/len(rest)


def list_of_neighbors(locations,connection):
    ''' This function returns the list of neighbors of each nodes.
    The first element in each output list is the city and the following cities are its neighbors.'''

    list_neighbors = []
    for city in locations:
        neighbors = []
        neighbors.append(city)
        for list_vertices in connection:
            if city == list_vertices[0]:
                neighbors.append(list_vertices[1])
        list_neighbors.append(neighbors)

    return list_neighbors



def clus_coef(list_neighbors, connection, locations, camp, conflict):
    ''' This function calculates the average local clustering coefficients of each category.'''

    ind_clus_coef = []

    for l in list_neighbors:
        neighbors = 0  #number of links all neighbors have
        for neighbor in l[1:]:
            for list_vertices in connection:
                if neighbor == list_vertices[0]:
                    if list_vertices[1] != l[0]:
                        if list_vertices[1] in l[1:]:
                            neighbors += 1
        if len(l)-1 == 1 or len(l)-1 == 0:
            ind_clus_coef.append(0)
        else:
            num_pos_link = (len(l)-1) * (len(l) - 2)
            ind_clus_coef.append(neighbors/num_pos_link)

    clus_coef_camp = 0
    clus_coef_conflict = 0
    clus_coef_hub = 0
    clus_coef_tot = 0
    rest = [x for x in locations if x not in camp + conflict]

    for i in range(len(list_neighbors)):

        clus_coef_tot += ind_clus_coef[i]

        if locations[i] in camp:
            clus_coef_camp += ind_clus_coef[i]

        elif locations[i] in conflict:
            clus_coef_conflict += ind_clus_coef[i]

        else:
            clus_coef_hub += ind_clus_coef[i]

    print("Average clus coef total: ", clus_coef_tot / len(locations))
    av_clus_tot = clus_coef_tot / len(locations)

    return ind_clus_coef, clus_coef_camp/len(camp), clus_coef_conflict/len(conflict), clus_coef_hub/len(rest), av_clus_tot
