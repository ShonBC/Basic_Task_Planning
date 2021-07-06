"""
Defines all functions and data structures
"""

# Initialize robot, bin, and kit states
robot = {'left_arm': True, 'right_arm': True, 'robot_location': 'home'}
bin_status = None
kit_status = None
goal = None

# If kit is True then the kit is complete
kit_complete = False

def initialize(): 
    """Take user inputs to initialize environment
    """

    global robot, bin_status, kit_status, goal

    while True:
        
        '''
        Take user input to initialize the bin state. If user inputs a number larger than 10 for 
        any color part, prompt to enter a new number.
        '''
        div_steps()

        red_bin, green_bin, blue_bin = [int(x) for x in input('How many red/green/blue parts in the bins? ').split()]

        if 0 <= red_bin <= 10 and 0 <= green_bin <= 10 and 0 <= blue_bin <= 10:
            pass
        else:

            print('Please enter a number less or equal to 10.')
            continue

        # Take user input to initialize the tray state
        red_tray, green_tray, blue_tray = [int(x) for x in input('How many red/green/blue parts currently in the kit tray? ').split()]

        '''
        Take user input to define the desired number of parts to be placed in the kit tray. 
        If user inputs a number larger than parts available in the bin for any color part, 
        prompt the user that not enough parts are available and exit the program.
        '''
        red_goal, green_goal, blue_goal = [int(x) for x in input('How many red/green/blue parts desired in the kit tray? ').split()]
        
        end = False
        if red_goal > red_bin + red_tray:
            print(f'Not enough red parts for kitting: {red_goal} needed, {red_bin} available.')
            end = True

        if green_goal > green_bin + green_tray:
            print(f'Not enough green parts for kitting: {green_goal} needed, {green_bin} available.')
            end = True

        if blue_goal > blue_bin + blue_tray:
            print(f'Not enough blue parts for kitting: {blue_goal} needed, {blue_bin} available.')
            end = True
        
        if end:
            print('...exiting.')
            exit()
        else:
            break  
     
    bin_status = {'red': red_bin, 'green': green_bin, 'blue': blue_bin}
    kit_status = {'red': red_tray, 'green': green_tray, 'blue': blue_tray, 'complete': kit_complete}
    goal = {'red': red_goal, 'green': green_goal, 'blue': blue_goal}

def div_steps(): 
    """ Prints '=' to show the divide between program steps
    """

    print('=' * 60)

def pick(empty_gripper: str, color_part: str): 
    """ This action allows one arm to pick up a part from a bin

    Args:
        empty_gripper (str): If true then gripper is empty, if false then gripper is holding a part.
        color_part (str): String describing the color part to pick.
    """
    
    if robot['robot_location'] == 'at_bin' and robot[empty_gripper] == True and bin_status[color_part] > 0 and kit_complete == False:
        robot[empty_gripper] = False
        bin_status[color_part] -= 1
        print(f'Pick {color_part} part with {empty_gripper}')

def place(empty_gripper: str, color_part: str): 
    """ This action places a part in the kit tray.

    Args:
        empty_gripper (str): If true then gripper is empty, if false then gripper is holding a part.
        color_part (str): String describing the color part to pick.
    """
    
    robot[empty_gripper] = True
    kit_status[color_part] += 1
    print(f'Place {color_part} part with {empty_gripper}')    

def move_to_bin():
    """ This action moves the robot next to the bins.
    """
    
    div_steps()
    robot['robot_location'] = 'at_bin'
    print('move_to_bin')

def move_to_tray():
    """ This action moves the robot next to the tray.
    """
    
    div_steps()
    robot['robot_location'] = 'at_tray'
    print('move_to_tray')

def kit_chk(color: str): 
    """ Check if kit has the desired number of parts.

    Args:
        color (str): Color of part to check.

    Returns:
        bool: If the kit contains the desired number of the specified color parts then return True.
    """

    global goal, kit_status

    if goal[color] == kit_status[color]:

        kit_complete = True

        return True

def plan():
    """Plan the robot actions to pick and place each color part into the kit.
    """

    div_steps()
    print('Generating a plan... \n')

    def grab_parts(color: str):
        """Pick and place parts until the desired number of the color part is in the kit.

        Args:
            color (str): Color of parts to generate plan for.
        """
        
        while kit_complete == False:
            
            if kit_chk(color): # Check if initial state is the goal state
                break

            move_to_bin()

            if goal[color] - kit_status[color] > 1:

                pick('left_arm', color)
                pick('right_arm', color)

            else:

                pick('left_arm', color)
            
            move_to_tray()

            if robot['left_arm'] == False and robot['right_arm'] == False:

                place('left_arm', color)
                place('right_arm', color)
            
            else:
                place('left_arm', color) 

    grab_parts('red')
    grab_parts('green')
    grab_parts('blue')

    div_steps()
    print('Summary:')
    print(f"The kit tray has {kit_status['red']} red part(s) -- the bin has {bin_status['red']} red part(s) left")
    print(f"The kit tray has {kit_status['green']} green part(s) -- the bin has {bin_status['green']} green part(s) left")
    print(f"The kit tray has {kit_status['blue']} blue part(s) -- the bin has {bin_status['blue']} blue part(s) left") 

if __name__ == "__main__":

    initialize()
    plan()
