This is a project for the course Complex System Simulation of the master Computational Science.

In this project the flee module (https://github.com/djgroen/flee-release) is used to simulate migration flows of refugees in conflict areas. The two main goals of the project were trying to improve the accuracy of the model and to answer the research question: "What network properties are important for the equal distribution of refugees over the different campsites".

#### Increasing the accuracy
In an attempt to increase the accuracy both forming of groups and the possibility for agents to have different speeds are added. 4 different variations of flee files are in the flee directory:  fleeOriginal.py, fleeOriginalSpeed.py, fleeGroups.py, fleeGroupsSpeed.py. 

Experiments can be tested by the examples of Burundi and Mali datasets. In order to test them, the desired file from above four should be renamed as flee and Mali.py or Burundi.py should be run.

Note for Mali dataset: for running  fleeGroups.py, fleeGroupsSpeed.py files comment line 42 and uncomment 41. While keep them vice versa in case of running fleeOriginal.py, fleeOriginalSpeed.py 

#### Answer the RQ
To answer the research question random planar graphs are generated and it's properties are analysed. When experiment.py is run 10 random graphs are simulated, the analysis of these graphs is visible when plot.py is run. All plots are saved in the 'figures' folder. Interesting figures are: n_camps.png, tot_degree_type0, tot_degree_type1, smallcorr2, phase and phase2.
The validation plot of the graphs and their properties is made in the jupyter file plot_function. There the validation is made of the data used in the project.