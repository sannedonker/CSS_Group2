from flee import flee_sanne
from datamanager import handle_refugee_data
from datamanager import DataTable
import numpy as np
import outputanalysis.analysis as a
import sys
import matplotlib.pyplot as plt
import pickle
# import datetime
from flee import properties


"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

def sort_groups(new_refs, size_param):

    size_dist = False
    if "normal" in size_param:
      args = size_param.split("_")
      dist = args[0]
      mu = float(args[1])
      sigma = float(args[2])
      size_dist = True
    else:
      g_size = round(float(size_param))

    # mu, sigma = 2., 0.5
    groups_n = 0
    group_sizes = []
    while new_refs > 0:

        # set the g_size based on the underlying dist
        if size_dist:
            g_size = 0
            while g_size < 1:
                if dist == "lognormal":
                    g_size = int(np.random.lognormal(mu, sigma, 1)[0])
                else:
                    g_size = int(np.random.normal(mu, sigma, 1)[0])

        if new_refs > g_size:
            new_refs -= g_size
        else:
            g_size = new_refs
            new_refs = 0

        group_sizes.append(g_size)
        groups_n += 1


    return groups_n, group_sizes


# def dijkstra(locations, camp, conflict):
#     goal_reached = False
#     # print(camp, conflict)
#
#     unvisited = locations.copy()
#     tentative = {}
#     for location in locations:
#         if location.name == camp:
#             visited = [location]
#         elif location.name == conflict:
#             tentative[location] = 10000
#             goal = location
#         else:
#             tentative[location] = 10000
#     current = visited[0]
#     current_dist = 0
#
#     while goal_reached == False:
#
#         links = current.links
#         for link in links:
#             end = link.endpoint
#             start = link.startpoint
#             # print(start.name, end.name, link.distance)
#
#             if start == current and (end in tentative.keys()):
#                 distance = link.distance + current_dist
#                 if distance < tentative[end]:
#                     tentative[end] = distance
#                 if tentative[goal] < 10000:
#                     goal_reached = True
#
#         # update current node, tentative, visited and unvisited
#         current = min(tentative, key=tentative.get)
#         current_dist = tentative[current]
#         if current != goal:
#             tentative.pop(current)
#         visited.append(current)
#         unvisited.remove(current)
#
#     return tentative[goal]


#Burundi Simulation


def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2015-05-01")

if __name__ == "__main__":

  # When true simulation is not run but only the network properties are given
  # When false simulation is run
  GET_PROP = True

  # THIS WAS IN THE ORGINAL CODE (WITHOUT G_SIZE AS ARG)
  # if len(sys.argv)>1:
  #   if (sys.argv[1]).isnumeric():
  #     end_time = int(sys.argv[1])
  #     last_physical_day = int(sys.argv[1])
  #   else:
  #     end_time = 396
  #     last_physical_day = 396
  #     duration = flee_sanne.SimulationSettings.SimulationSettings.ReadFromCSV(sys.argv[1])
  #     if duration>0:
  #       end_time = duration
  #       last_physical_day = end_time
  # else:
  #   end_time = 396
  #   last_physical_day = 396

  """ Options for argv are int, lognormal_mu_sigma, normal_mu_sigma. Default = 1 """
  if len(sys.argv) > 1:
      size_param = sys.argv[1]
      # if type(sys.argv[1]) == int:
      #     g_size = sys.argv[1]
      # else:
      #     args = sys.argv[1].split("_")
      #     mu = args[1]
      #     sigma = args[2]
      #     if args[0] == "lognormal"
      #         g_size = int(np.random.lognormal(mu, sigma, 1)[0])
      #     else:
      #         g_size = int(np.random.lognormal(mu, sigma, 1)[0])
  else:
      size_param = 1



  end_time = 396
  last_physical_day = 396

  e = flee_sanne.Ecosystem()

  locations = []

  #Burundi
  locations.append(e.addLocation("Bujumbura", movechance="conflict", pop=497166))
  locations.append(e.addLocation("Bubanza", movechance="default"))
  locations.append(e.addLocation("Bukinanyana", movechance="default", pop=75750))
  locations.append(e.addLocation("Cibitoke", movechance="default", pop=460435))
  locations.append(e.addLocation("Isale", movechance="default"))

  locations.append(e.addLocation("Muramvya", movechance="default"))
  locations.append(e.addLocation("Kayanza", movechance="default"))
  locations.append(e.addLocation("Kabarore", movechance="default", pop=62303)) #This resides in Kayanza province in Burundi. Not to be confused with Kabarore, Rwanda.
  locations.append(e.addLocation("Mwaro", movechance="default", pop=273143))
  locations.append(e.addLocation("Rumonge", movechance="default"))

  locations.append(e.addLocation("Burambi", movechance="default", pop=57167))
  locations.append(e.addLocation("Bururi", movechance="default"))
  locations.append(e.addLocation("Rutana", movechance="default"))
  locations.append(e.addLocation("Makamba", movechance="default"))
  locations.append(e.addLocation("Gitega", movechance="default"))

  locations.append(e.addLocation("Karuzi", movechance="default"))
  locations.append(e.addLocation("Ruyigi", movechance="default"))
  locations.append(e.addLocation("Gisuru", movechance="default", pop=99461))
  locations.append(e.addLocation("Cankuzo", movechance="default"))
  locations.append(e.addLocation("Muyinga", movechance="default"))

  locations.append(e.addLocation("Kirundo", movechance="default"))
  locations.append(e.addLocation("Ngozi", movechance="default"))
  locations.append(e.addLocation("Gashoho", movechance="default"))
  locations.append(e.addLocation("Gitega-Ruyigi", movechance="default"))
  locations.append(e.addLocation("Makebuko", movechance="default"))

  locations.append(e.addLocation("Commune of Mabanda", movechance="default"))

  #Rwanda, Tanzania, Uganda and DRCongo camps
  locations.append(e.addLocation("Mahama", movechance="camp", capacity=49451, foreign=True))
  locations.append(e.addLocation("Nduta", movechance="default", capacity=55320, foreign=True)) # Nduta open on 2015-08-10
  locations.append(e.addLocation("Kagunga", movechance=1/21.0, foreign=True))
  locations.append(e.addLocation("Nyarugusu", movechance="camp", capacity=100925, foreign=True))
  locations.append(e.addLocation("Nakivale", movechance="camp", capacity=18734, foreign=True))
  locations.append(e.addLocation("Lusenda", movechance="default", capacity=17210, foreign=True))

  #Within Burundi
  e.linkUp("Bujumbura","Bubanza","48.0")
  e.linkUp("Bubanza","Bukinanyana","74.0")
  e.linkUp("Bujumbura","Cibitoke","63.0")
  e.linkUp("Cibitoke","Bukinanyana","49.0")
  e.linkUp("Bujumbura","Muramvya","58.0")
  e.linkUp("Muramvya","Gitega","44.0")
  e.linkUp("Gitega","Karuzi","54.0")
  e.linkUp("Gitega","Ruyigi","55.0")
  e.linkUp("Ruyigi","Karuzi","43.0")
  e.linkUp("Karuzi","Muyinga","42.0")
  e.linkUp("Bujumbura","Kayanza","95.0")
  e.linkUp("Kayanza","Ngozi","31.0") ##
  e.linkUp("Ngozi","Gashoho","41.0") ##
  e.linkUp("Kayanza","Kabarore","18.0")
  e.linkUp("Gashoho","Kirundo","42.0")
  e.linkUp("Gashoho","Muyinga","34.0")
  e.linkUp("Bujumbura","Mwaro","67.0")
  e.linkUp("Mwaro","Gitega","46.0")
  e.linkUp("Bujumbura","Rumonge","75.0")
  e.linkUp("Rumonge","Bururi","31.0")
  e.linkUp("Rumonge","Burambi","22.0")
  e.linkUp("Rumonge","Commune of Mabanda","73.0")
  e.linkUp("Commune of Mabanda","Makamba","18.0") # ??
  e.linkUp("Bururi","Rutana","65.0")
  e.linkUp("Makamba","Rutana","50.0") # ??
  e.linkUp("Rutana","Makebuko","46.0") # ??
  e.linkUp("Makebuko","Gitega","24.0") # ??
  e.linkUp("Makebuko","Ruyigi","40.0")
  e.linkUp("Ruyigi","Cankuzo","51.0")
  e.linkUp("Ruyigi","Gisuru","31.0")
  e.linkUp("Cankuzo","Muyinga","63.0")

  #Camps, starting at index locations[26] (at time of writing).
  e.linkUp("Muyinga","Mahama","135.0")
  e.linkUp("Kirundo","Mahama","183.0") #Shorter route than via Gashoho and Muyinga. Goes through Bugesera, where a transit centre is located according to UNHCR reports.
  e.linkUp("Gisuru","Nduta","60.0")
  e.linkUp("Commune of Mabanda","Kagunga","36.0")
  e.linkUp("Commune of Mabanda","Nyarugusu","71.0") #Estimated distance, as exact location of Nyarugusu is uncertain.

  e.linkUp("Kagunga","Nyarugusu","91.0", forced_redirection=True) #From Kagunga to Kigoma by ship (Kagunga=Kigoma)
  e.linkUp("Kirundo","Nakivale","318.0")
  e.linkUp("Kayanza","Nakivale","413.0")

  e.linkUp("Nduta","Nyarugusu","150.0", forced_redirection=True) #distance needs to be checked.

  if GET_PROP is True:

      # links that are added later in the simulation
      e.linkUp("Bujumbura","Lusenda","53.0") #Only added when the refugee inflow starts at Lusenda, on 30-07-2015
      e.remove_link("Nduta","Nyarugusu")
      e.linkUp("Nduta","Nyarugusu","150.0") #Re-add link, but without forced redirection

      camps = ["Mahama", "Nduta", "Nyarugusu", "Nakivale", "Lusenda"]
      conflicts = ["Bujumbura", "Burambi", "Mwaro", "Bukinanyana", "Cibitoke", "Kabarore", "Gisuru"]
      connections = e.export_graph(False)[1]
      properties.get_properties(locations, camps, conflicts, connections)

      print("If you want to run the simulation set 'GET_PROP' to False")
      quit()


  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="source_data/burundi2015", start_date="2015-05-01")

  # Correcting for overestimations due to inaccurate level 1 registrations in five of the camps.
  # These errors led to a perceived large drop in refugee population in all of these camps.
  # We correct by linearly scaling the values down to make the last level 1 registration match the first level 2 registration value.
  # To our knowledge, all level 2 registration procedures were put in place by the end of 2016.
  d.correctLevel1Registrations("Mahama","2015-10-04")
  d.correctLevel1Registrations("Nduta","2016-04-06")
  d.correctLevel1Registrations("Nyarugusu","2015-11-10")
  d.correctLevel1Registrations("Nakivale","2015-08-18")
  d.correctLevel1Registrations("Lusenda","2015-09-30")

  locations[26].capacity = d.getMaxFromData("Mahama", last_physical_day)
  locations[27].capacity = d.getMaxFromData("Nduta", last_physical_day)
  locations[29].capacity = d.getMaxFromData("Nyarugusu", last_physical_day)
  locations[30].capacity = d.getMaxFromData("Nakivale", last_physical_day)
  locations[31].capacity = d.getMaxFromData("Lusenda", last_physical_day)



  list_of_cities = "Time"

  for l in locations:
    list_of_cities = "%s,%s" % (list_of_cities, l.name)

  #print(list_of_cities)
  #print("Time, campname")
  print("Day,Mahama sim,Mahama data,Mahama error,Nduta sim,Nduta data,Nduta error,Nyarugusu sim,Nyarugusu data,Nyarugusu error,Nakivale sim,Nakivale data,Nakivale error,Lusenda sim,Lusenda data,Lusenda error,Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,retrofitted time,refugees in camps (simulation),refugee_debt,Total error (retrofitted)")


  #Set up a mechanism to incorporate temporary decreases in refugees
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only


  e.add_conflict_zone("Bujumbura")


  t_retrofitted = 0


  camp_names = ["Mahama", "Nduta", "Nyarugusu", "Nakivale", "Lusenda"]
  all_camp_data = {}
  all_camp_sim = {}
  all_errors = {}
  for i in camp_names:
      all_camp_data[i] = []
      all_camp_sim[i + "_sim"] = []
      all_errors[i + "_err"] = []

  total_err = []

  TEMP_END = 15
  for t in range(0,end_time):
  # for t in range(0, TEMP_END):

    t_data = t

    #Lusenda camp open on the 30th of July 2015
    if t_data == date_to_sim_days("2015-07-30"): #Open Lusenda
      locations[31].SetCampMoveChance()
      locations[31].Camp=True
      e.linkUp("Bujumbura","Lusenda","53.0") #Only added when the refugee inflow starts at Lusenda, on 30-07-2015

    if t_data == date_to_sim_days("2015-08-10"):
      locations[27].SetCampMoveChance()
      locations[27].Camp=True
      e.remove_link("Nduta","Nyarugusu")
      e.linkUp("Nduta","Nyarugusu","150.0") #Re-add link, but without forced redirection


    #Append conflict_zone and weight to list.
    #Conflict zones after the start of simulation period
    if t_data == date_to_sim_days("2015-07-10"): #Intense fighting between military & multineer military forces
      e.add_conflict_zone("Kabarore")

    elif t_data == date_to_sim_days("2015-07-11"): #Intense fighting between military & mulineer military forces
      e.add_conflict_zone("Bukinanyana")

    elif t_data == date_to_sim_days("2015-07-15"): #Battles unidentified armed groups coordinately attacked military barracks
      e.add_conflict_zone("Cibitoke")

    elif t_data == date_to_sim_days("2015-10-26"): #Clashes and battles police forces
      e.add_conflict_zone("Mwaro")

    elif t_data == date_to_sim_days("2015-11-23"): #Battles unidentified armed groups coordinate attacks
      e.add_conflict_zone("Gisuru")

    elif t_data == date_to_sim_days("2015-12-08"): #Military forces
      e.add_conflict_zone("Burambi")

    #new_refs = d.get_new_refugees(t)
    new_refs = d.get_new_refugees(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_new_refugees(t, FullInterpolation=True)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0

    group_n, group_sizes = sort_groups(new_refs, size_param)

    # TODO: DIT MOET IK NOG FIXEN WANT HIER GAAN NOG DINGEN FOUT
    # Here we use the random choice to make a weighted choice between the source locations.
    speed_bool = sys.argv[3]
    # print(speed_bool)
    e.add_agents_to_conflict_zones(group_n, group_sizes) #, speed_bool)

    #Propagate the model by one time step.
    # print(t)
    e.evolve()

    # e.printInfo()

    # add simulated data to dictionary
    for i in e.locations:
        if i.name in camp_names:
            all_camp_sim[i.name + "_sim"].append(i.numAgents)

    #Validation/data comparison
    mahama_data = d.get_field("Mahama", t) #- d.get_field("Mahama", 0)
    nduta_data = d.get_field("Nduta", t) #-d.get_field("Nduta", 0)
    nyarugusu_data = d.get_field("Nyarugusu", t) #- d.get_field("Nyarugusu", 0)
    nakivale_data = d.get_field("Nakivale", t) #- d.get_field("Nakivale", 0)
    lusenda_data = d.get_field("Lusenda", t) #- d.get_field("Lusenda", 0)

    for i in camp_names:
        all_camp_data[i].append(eval((i + "_data").lower()))

    errors = []
    abs_errors = []
    loc_data = [mahama_data, nduta_data, nyarugusu_data, nakivale_data, lusenda_data]
    camp_locations = [26, 27, 29, 30, 31]

    camps = []
    for i in camp_locations:
      camps += [locations[i]]
    # camp_names = ["Mahama", "Nduta", "Nyarugusu", "Nakivale", "Lusenda"]



    camp_pops_retrofitted = []
    errors_retrofitted = []
    abs_errors_retrofitted = []

    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for c in camps:
      refugees_in_camps_sim += c.numAgents
    # t_retrofitted = d.retrofit_time_to_refugee_count(refugees_in_camps_sim, camp_names)

    # calculate errors
    for i in range(0,len(camp_locations)):
      camp_number = camp_locations[i]
      errors += [a.rel_error(locations[camp_number].numAgents, loc_data[i])]
      abs_errors += [a.abs_error(locations[camp_number].numAgents, loc_data[i])]

      # errors when using retrofitted time stepping.
      # TODO: T_RETROFITTED IS USED HERE BUT IS STILL INITIALIZED ON 0......
      # camp_pops_retrofitted += [d.get_field(camp_names[i], t_retrofitted, FullInterpolation=True)]
      camp_pops_retrofitted += [d.get_field(camp_names[i], t, FullInterpolation=True)]
      errors_retrofitted += [a.rel_error(camps[i].numAgents, camp_pops_retrofitted[-1])]
      abs_errors_retrofitted += [a.abs_error(camps[i].numAgents, camp_pops_retrofitted[-1])]


      # total_err.append(errors)
      all_errors[camp_names[i] + "_err"].append(a.abs_error(locations[camp_number].numAgents, loc_data[i]))
      # all_errors[camp_names[i] + "_err"].append(a.rel_error(locations[camp_number].numAgents, loc_data[i]))

    # output = "%s" % t
    #
    # for i in range(0,len(errors)):
    #   camp_number = camp_locations[i]
    #   output += ",%s,%s,%s" % (locations[camp_number].numAgents, loc_data[i], errors[i])
    #
    #
    # if refugees_raw>0:
    #   #output_string += ",%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw)
    #   output += ",%s,%s,%s,%s,%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw, t_retrofitted, refugees_in_camps_sim, refugee_debt, float(np.sum(abs_errors_retrofitted))/float(refugees_raw))
    # else:
    #   output += ",0,0,0,0,0,0,0"
    #   #output_string += ",0"
    #
    #
    # print(output)

# TODO: ADD AXIS AND TITLES
  # for i in camp_names:
  #     plt.title(i)
  #     plt.plot(all_camp_data[i])
  #     plt.plot(all_camp_sim[i + "_sim"])
  #     plt.savefig("plots/" + i + "_test1.png", dpi=300)
  #     plt.clf()
  #
  #     plt.title("Error between simulation and data of " + i)
  #     # print(all_errors[i + "_err"])
  #     # quit()
  #     plt.plot(all_errors[i + "_err"])
  #     plt.savefig("plots/" + i + "_test1_err.png", dpi=300)
  #     plt.clf()

  """ SAVE IN A PICKLE """
  """ Give g_size as first, run number as second and speed_bool as third arg """
  if len(sys.argv) > 2:
      pickle.dump(all_errors, open("error_abs_" + size_param + "_" + sys.argv[2] + "_" + sys.argv[3] + ".p", "wb"))
      print("at size_param: " + size_param + " and run: " + sys.argv[2])
  else:
      pickle.dump(all_errors, open("error_abs_" + size_param + datetime.time + ".p", "wb"))
