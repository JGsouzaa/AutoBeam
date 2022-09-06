#Instance of application and object references
Robotapp = RobotApplicationClass()
project = Robotapp.Project
preferences = project.Preferences
structure = project.Structure
bars = structure.Bars
labels = structure.Labels
selections = structure.Selections
cases = structure.Cases
obj = structure.Objects
results = structure.Results
nodes_serv = results.Nodes
r_Bars = results.Bars
force_serv = r_Bars.Forces

bar_col = RobotBarCollection(bars.GetAll())
cas_col = IRobotCaseCollection(cases.GetAll())

