'''
Pathfinding elements to carry out the problem solving.
'''
import Actions
from Blocks import Location
from RobotArm import RobotArm

class Solver:
    # Holds initial state blocks and goal state blocks
    def __init__(self, init_state_blocks, goal_state_blocks):
        self.init_state = init_state_blocks     # Initial state blocks
        self.goal_state = goal_state_blocks     # Goal state blocks
        self.current_state = init_state_blocks  # Current state of the blocks
        self.l1_complete = False
        self.l2_complete = False
        self.l3_complete = False
        self.l4_complete = False
        self.goals = {}

    '''
    Check if we have reached the goal state
    '''
    def goal_state_reached(self):
        return self.current_state == self.goal_state

    '''
    Solve the World of Blocks problem.
    '''
    def solve(self):
        # Get all blocks to the default position
        self.reposition()

        # If there are any blocks going to L1, find the TABLE block, and then reposition
        # Do this for each stack location
        self.get_l1_blocks()
        self.get_l2_blocks()
        self.get_l3_blocks()
        self.get_l4_blocks()

    '''
    Checks if a block in the "default" state has a goal state of the specified location
    '''
    def block_in_location(self, loc):
    # Check if there is a block in L$ that belongs in loc
        loc_found = False
        for block in self.current_state.L4:
            if RobotArm.get_instance().get_goal_dict()[block.symbol].location == loc:
                loc_found = True
        return loc_found

    '''
    Moves blocks to L3 from L4
    '''
    def remove_bad_block(self):
        # Unstack the block and move it to L3
        block = self.current_state.L4.pop()
        Actions.unstack(block, self.current_state.L4[-1])
        Actions.move(Location.L3)
        if len(self.current_state.L3) == 0: # Put down if L3 is empty, stack otherwise
            Actions.put_down(block, Location.L3)
        else:
            Actions.stack(block, self.current_state.L3[-1])

    '''
    Handle block movement to L1
    '''
    def get_l1_blocks(self):
        if self.block_in_location(Location.L1): # Check if we have blocks in location
            # Check each block in L4, if it is the table block
            # move it to L1. Otherwise place it on L3 for repositioning
            for block in self.current_state.L4:
                # If the block has a goal in L1
                if RobotArm.get_instance().get_goal_dict()[block.symbol].location == Location.L1:
                    # Check if L1 has any blocks on it; if it does not, find the TABLE block first
                    if len(self.current_state.L1) == 0: # Table block not found yet
                        # Find table block
                        if RobotArm.get_instance().get_goal_dict()[block.symbol].table:
                            table_block = self.current_state.L4[-1] # pull off table block
                            if table_block.state.table: # pick-up if on table, unstack otherwise
                                table_block = self.current_state.L4.pop()
                                Actions.pick_up(table_block)
                                Actions.move(Location.L1)
                                Actions.put_down(table_block, Location.L1)
                                self.reposition()
                                self.get_l1_blocks()
                            else:
                                self.remove_bad_block()
                                self.get_l1_blocks()
                    else: # Table block already found, START HERE ==========================
                        # Find the block that goes on the topmost block, put it there
                        # Reposition and call get_l1_blocks to get rest of blocks
                        pass
                else: # block does not belong on specified location
                    self.remove_bad_block()
                    self.get_l1_blocks()


    '''
    Handle block movement to L2
    '''
    def get_l2_blocks(self):
        if self.block_in_location(Location.L2): # Check if we have blocks in location
            for block in self.current_state.L4:
                print("In L2: ", block.symbol)

    '''
    Handle block movement to L3
    '''
    def get_l3_blocks(self):
        if self.block_in_location(Location.L3): # Check if we have blocks in location
            for block in self.current_state.L4:
                print("In L3: ", block.symbol)

    '''
    Handle block movement to L4
    '''
    def get_l4_blocks(self):
        pass

    '''
    Iterate over each stack location and move the blocks to L4 to get them to a "default" state.
    '''
    def reposition(self):
        if not self.l1_complete and len(self.current_state.L1) > 0:
            if not len(self.current_state.L1) == 1:
                for item in self.current_state.L1:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L1[-1].at_goal:
                        break
                    block = self.current_state.L1.pop()
                    if Actions.unstack(block, block.state.on): # Attempt to Unstack
                        Actions.move(Location.L4)
                        if Actions.put_down(block, Location.L4): # Attempt put down on table
                            self.current_state.L4.append(block) # Add block to the stack
                        elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                            self.current_state.L4.append(block)

            # Get block from bottom of stack
            if not self.current_state.L1[0].at_goal:
                block = self.current_state.L1.pop()
                if Actions.pick_up(block):
                    Actions.move(Location.L4)
                if Actions.put_down(block, Location.L4): # Attempt put down on table
                    self.current_state.L4.append(block) # Add block to the stack
                elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                    self.current_state.L4.append(block)

        if not self.l2_complete and len(self.current_state.L2) > 0:
            if not len(self.current_state.L2) == 1:
                for item in self.current_state.L2:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L2[-1].at_goal:
                        break
                    block = self.current_state.L2.pop()
                    if Actions.unstack(block, block.state.on): # Attempt to Unstack
                        Actions.move(Location.L4)
                        if Actions.put_down(block, Location.L4): # Attempt put down on table
                            self.current_state.L4.append(block) # Add block to the stack
                        elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                            self.current_state.L4.append(block)

            # Get block from bottom of stack
            if not self.current_state.L2[0].at_goal:
                block = self.current_state.L2.pop()
                if Actions.pick_up(block):
                    Actions.move(Location.L4)
                if Actions.put_down(block, Location.L4): # Attempt put down on table
                    self.current_state.L4.append(block) # Add block to the stack
                elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                    self.current_state.L4.append(block)

        if not self.l3_complete  and len(self.current_state.L3) > 0:
            if not len(self.current_state.L3) == 1:
                for item in self.current_state.L3:
                    # If the next block is at the goal state, leave the loop
                    if self.current_state.L3[-1].at_goal:
                        break
                    block = self.current_state.L3.pop()
                    if Actions.unstack(block, block.state.on): # Attempt to Unstack
                        Actions.move(Location.L4)
                        if Actions.put_down(block, Location.L4): # Attempt put down on table
                            self.current_state.L4.append(block) # Add block to the stack
                        elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                            self.current_state.L4.append(block)

            # Get block from bottom of stack
            if not self.current_state.L3[0].at_goal:
                block = self.current_state.L3.pop()
                if Actions.pick_up(block):
                    Actions.move(Location.L4)
                if Actions.put_down(block, Location.L4): # Attempt put down on table
                    self.current_state.L4.append(block) # Add block to the stack
                elif Actions.stack(block, self.current_state.L4[-1]): # Attempt to stack
                    self.current_state.L4.append(block)

        # This is for testing purposes
        for block in self.current_state.L4:
            block.block_info()