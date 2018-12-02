'''
Driver code for World Of Blocks
'''
import solver.Actions
from utils import Constants
import cocos
from solver.Solver import Solver
from solver.Blocks import Block
from solver.Blocks import Location
from solver.Blocks import State
from solver.Blocks import TableState
from solver.RobotArm import RobotArm
from game.Drawable import (Table, Title, LocationLabel, BlockSprite, RobotArmSprite,
    InitialStateLabel, GoalStateLabel, InitialStateEntry, GoalStateEntry)
import ctypes

'''
Before running the solver, we want input given from the user.
User gives input at command line and this reads in the information.
'''
def ask_for_user_states():
    print("Welcome to the World of Blocks AI Solver!")
    print("=========================================")
    print("Describe your initial state one block at a time, separated by commas.")
    print("Start with the block on the bottom and work your way upwards.")
    print("There are a total of four locations on the table, L1-L4.")
    print("L1 INITIAL STATE:")
    l1_init = input()
    l1_init_stack = create_stack(l1_init, Location.L1)
    print("L2 INITIAL STATE:")
    l2_init = input()
    l2_init_stack = create_stack(l2_init, Location.L2)
    print("L3 INITIAL STATE:")
    l3_init = input()
    l3_init_stack = create_stack(l3_init, Location.L3)
    print("L4 INITIAL STATE:")
    l4_init = input()
    l4_init_stack = create_stack(l4_init, Location.L4)

    print("Next, please input the GOAL STATE")
    print("L1 GOAL STATE:")
    l1_goal = input()
    l1_goal_stack = create_stack(l1_goal, Location.L1)
    print("L2 GOAL STATE:")
    l2_goal = input()
    l2_goal_stack = create_stack(l2_goal, Location.L2)
    print("L3 GOAL STATE:")
    l3_goal = input()
    l3_goal_stack = create_stack(l3_goal, Location.L3)
    print("L4 GOAL STATE:")
    l4_goal = input()
    l4_goal_stack = create_stack(l4_goal, Location.L4)

def create_stack(blocks, loc):
    blocks = blocks.strip() # Remove any whitespace
    symbols = blocks.split(",") # delimit by commas
    block_stack = []
    # Create blocks and add them to stack
    for symbol in symbols:
        block = Block(symbol)
        block_stack.append(block)
    
    if len(block_stack) > 0:
        for block in block_stack:
            if block == block_stack[0]: # Handle table block
                block_stack[0].state = State(None, None, False, True, loc)
            else:
                idx = block_stack.index(block) # Get the index of the block in the stack
                above_list = []
                count = 0
                while count < idx: # Build the above list
                    above_list.append(block_stack[count])
                    count += 1
                block.state = State(above_list, block_stack[idx - 1], False, False, loc)

        block_stack[-1].state.clear = True # Topmost block is always clear

    for block in block_stack:
        block.block_info()

    return block_stack


# Create some test states
def create_states_test():
    # Create some blocks
    block_a = Block("A")
    block_b = Block("B")
    block_c = Block("C")
    block_d = Block("D")

    # Make copies of the original location of A B and C
    block_a_copy = Block(block_a.symbol)
    block_b_copy = Block(block_b.symbol)
    block_c_copy = Block(block_c.symbol)
    block_d_copy = Block(block_d.symbol)
    
    # Give the blocks attributes to stack in order on L1, with A on top, B in the middle, C on table (initial state)
    ''' UNCOMMENT FOR L1 STACK -- THIS PROBABLY WON'T WORK UNTIL IT IS MODIFIED
    block_a.state = State([block_c, block_b], block_b, True, False)
    block_b.state = State([block_c], block_c, False, False)
    block_c.state = State([], None, False, True)
    '''

    ''' UNCOMMENT FOR SPREAD OUT STACK '''
    block_a.state = State([], None, True, True, Location.L1)
    block_b.state = State([], None, True, True, Location.L2)
    block_c.state = State([], None, False, True, Location.L3)
    block_d.state = State([block_c], block_c, True, False, Location.L3)
    

    # Set A at L4 on the table, with B on top, and C at L2 (goal state)
    block_a_copy.state = State([], None, False, True, Location.L4)                      # L4, On Table
    block_b_copy.state = State([block_a_copy], block_a_copy, True, False, Location.L4)  # L4, On A
    block_c_copy.state = State([], None, True, True, Location.L2)                       # L2, On Table
    block_d_copy.state = State([block_c_copy], block_c_copy, True, False, Location.L2)  # L2, On C

    # State we start with and state we end with
    # SET THE ORDER OF THE BLOCKS HERE IN THE STACK
    l1 = [block_a]
    l2 = [block_b]
    l3 = [block_c, block_d]
    l4 = []
    initial_state = TableState(l1, l2, l3, l4)
    l1 = []
    l2 = [block_c_copy, block_d_copy]
    l3 = []
    l4 = [block_a_copy, block_b_copy]
    goal_state = TableState(l1, l2, l3, l4)

    # Register these states to the robot arm
    RobotArm.get_instance().register_initial_state(initial_state)
    RobotArm.get_instance().register_goal_state(goal_state)

    # Create the solver, register it to RobotArm, and solve
    solver = Solver(RobotArm.get_instance().get_initial_state(),
                    RobotArm.get_instance().get_goal_state())
    RobotArm.get_instance().register_solver(solver)
    RobotArm.get_instance().run_solver()

# Insertion point for program
# TODO: Create the blocks and initalize them
# TODO: Designate the locations on the table
if __name__ == "__main__":
    # Ask for user input to get states
    ask_for_user_states()

    # Initialize the director (a type of game manager, a singleton object)
    cocos.director.director.init(width=Constants.WINDOW_WIDTH, height=Constants.WINDOW_HEIGHT, caption="World of Blocks - AI With Planning")

    # Create isntances of the layers
    heading_layer = Title()             # Title
    table_layer = Table()               # Table
    loc_1 = LocationLabel(Location.L1)  # L1 Label
    loc_2 = LocationLabel(Location.L2)  # L2 Label
    loc_3 = LocationLabel(Location.L3)  # L3 Label
    loc_4 = LocationLabel(Location.L4)  # L4 Label
    block_a = BlockSprite("A")
    block_b = BlockSprite("B")

    # State Labels
    init_state_label = InitialStateLabel()
    goal_state_label = GoalStateLabel()

    # State entry
    init_entry = InitialStateEntry()
    goal_entry = GoalStateEntry()

    # Testing new functionality
    block_b.set_y(13)
    block_b.set_x(Location.L3)

    arm_layer = RobotArmSprite()        # Robot arm sprite

    # Create a scene that contains the layer we just created as a child
    main_scene = cocos.scene.Scene()
    main_scene.add(heading_layer)
    main_scene.add(table_layer, 1)
    main_scene.add(loc_1, 1)
    main_scene.add(loc_2, 1)
    main_scene.add(loc_3, 1)
    main_scene.add(loc_4, 1)
    main_scene.add(block_a, 2)
    main_scene.add(block_b, 2)
    main_scene.add(arm_layer, 2)

    # Add state labels
    main_scene.add(init_state_label)
    main_scene.add(goal_state_label)

    # Add state entry
    main_scene.add(init_entry)
    main_scene.add(goal_entry)

    # Run the scene
    cocos.director.director.run(main_scene)




    '''
    DOING SOME TESTING HERE
    '''
    #abc_test()
    #create_states_test()