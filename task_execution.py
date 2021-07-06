"""
Calls the functions and data structures defined in task_planning.py

Program will ask user for input on how many red/green/blue parts are in the bin and tray 
as well as how many are desired in the kit.

The output is the planned actions to achieve the desired goal state.
"""

from planning.task_planning import initialize, plan

if __name__ == "__main__":
    
    initialize()
    plan()
