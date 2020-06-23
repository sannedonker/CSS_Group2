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

def get_properties(locations, camps, conflicts):
    """
    Get properties of the networks
    """
    distances = []
    for location in locations:
        links = location.links
        for link in links:
            distances.append(link.distance)
            # print(link.startpoint.name, link.endpoint.name, link.distance)

    # print maxium, minimum and average weight of the links
    print("max dist", max(distances))
    print("min dist", min(distances))
    print("av dist", (sum(distances) / 2) / len(distances))

    # perform Dijkstra algorithm for all camp - conflict combinations
    paths = []
    for camp in camps:
        for conflict in conflicts:
            path = dijkstra(locations, camp, conflict)
            paths.append(path)

    # print average shortes path length and diameter
    print("av path", sum(paths) / len(paths))
    print("diameter", max(paths))
