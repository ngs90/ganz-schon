import numpy as np
class GameSheet(object):

    def __init__(self):

        # Board
        self.yellow = np.eye(4, dtype=int)[::, ::-1]
        self.yellow_dictionary = {'1':   [(2, 0), (1, 1)],
                                    '2': [(1, 0), (2, 2)],
                                    '3': [(0, 0), (3, 1)],
                                    '4': [(3, 2), (2, 3)],
                                    '5': [(0, 2), (1, 3)],
                                    '6': [(0, 1), (3, 3)],
                                    }

        self.yellow_option_mapping = np.array([[0, 1, 2, None], [3, 4, None, 5], [6, None, 7, 8], [None, 9, 10, 11]])


        self.blue = np.zeros((3, 4), dtype=int)
        self.blue_option_mapping = np.arange(11, 23).reshape(3, 4)

        self.blue[0, 0] = 1
        self.green_pos = - 1 #changed to -1 so position = x means x is last crossed.
        self.green_bounds = np.array([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6])
        self.orange_pos = - 1
        self.orange_sum = 0
        self.purple_pos = - 1
        self.purple_sum = 0
        self.purple_last_value = 0
        self.green_orange_purple_bonus = np.array([[ - 1, - 1, - 1, - 1, - 1, 1, 5, - 1, 4, - 1, - 1],
                                                   [ - 1, - 1, - 1, - 1, 0, - 1, - 1,5, - 1, 4, - 1],
                                                   [ - 1, - 1, - 1,1, -1, 0, 5, - 1, 2, 3, - 1]]
                                                  ,dtype=int)
        self.choice = None # Value of die chosen
        self.last_mark = None
        self.yellow_side = None
        self.no_fox = 0
        self.plus_ones = 0
        self.rerolls = 0


        # Dice
        # yellow (0), blue (1), green (2), orange (3), purple (4), white (5)
        self.dice = np.zeros(6, dtype=int)
        self.dice_active = np.ones(6, dtype=int)

        self.options = None

        self.valid_options = None

    def Roll(self):
        print('Pre-Roll', self.dice[self.dice_active > 0], self.dice, self.dice_active)
        self.dice[self.dice_active > 0] = np.random.choice(6, np.sum(self.dice_active[self.dice_active > 0])) + 1
        return self.dice

#TODO: substitute choicewrap into active and passive roll.

    def ChoiceHandler(self):

        self.generatevalidoptions() # need something to map back to choice_option and yellow_side etc.
        self.choice_option = np.random.choice(self.options)  # TODO: Implement fancy algorithm choice nice mega awesome function here

        if self.choice_option >= 50:  # If color is white,
            self.index_choice = 5
            self.choice = self.dice[5]
        else:
            self.index_choice = self.choice_option
            self.choice = self.dice[self.index_choice]

        if self.choice_option in [0, 50]:
            self.bonus_choice = None
            self.generatevalidoptions()
            self.yellow_side = np.random.choice([0, 1], 1)[0]  # TODO: Implement fancy algorithm choice nice mega awesome function here
        else:
            self.yellow_side = None

    def ActiveRoll(self):
        self.dice_values = self.Roll()
        #active_dice_values = dice_values[self.dice_active]

        pre_options = np.argwhere(self.dice_active[:5] > 0).ravel()
        if self.dice_active[5] > 0:
            self.options = np.concatenate((pre_options, np.arange(50, 55, dtype = int)))
        else:
            self.options = pre_options

        self.ChoiceHandler()

        print('Dice values', self.dice_values, 'options', self.options, 'choice is', self.choice, 'with index', self.index_choice)
        self.dice_active[ self.dice_active > 0 ] = np.where(self.choice > self.dice_values, 0, self.dice_active)[self.dice_active > 0]
        self.dice_active[self.index_choice] = -1

        print('Active dice values', self.dice[self.dice_active > 0], 'Dice_active_index', self.dice_active)

    def PassiveRoll(self): #rules: Only 1 roll w/ 6 dice. Choose 1 among the 3 smallest dice.
        self.dice_values = self.Roll()
        small_dice = np.partition(self.dice_values, 3)[:3] #takes the 3 smallest dice
        max = small_dice.max()
#        print(self.dice_values,small_dice,max)
        self.dice_active[self.dice_values > max] = 0
        no_strictly_smaller = sum(small_dice < max)
        no_equal = sum(self.dice_values == max) # if there are not exactly 3 smallest dice, randomness chooses
#        print("no_equal + no_strictly_smaller",no_equal,no_strictly_smaller,no_equal + no_strictly_smaller)
        if no_equal + no_strictly_smaller > 3:
            max_among_min = np.argwhere(self.dice == max).flatten()
#            print(max_among_min)
            indices_to_deactivate = np.random.choice(max_among_min, no_equal + no_strictly_smaller-3, replace=False)
            self.dice_active[indices_to_deactivate] = 0

        pre_options = np.argwhere(self.dice_active[:5] > 0).ravel()


        if self.dice_active[5] > 0:
            self.options = np.concatenate((pre_options, np.arange(50,55)))
        else:
            self.options = pre_options


        self.bonus_choice = None
        self.ChoiceHandler()

        print('Dice values', self.dice_values, 'options', self.options, 'choice is', self.choice, 'with index', self.index_choice)
        print('Active dice values', self.dice[self.dice_active > 0], 'Dice_active_index', self.dice_active)


    def MarkSheet(self, color=None, value=None, yellow_side=None):

        if color is None:
            color = self.choice_option

            if self.index_choice == 5: #If color is white, # self.choice_option >= 5
                color = self.choice_option % 10 # eller 5 eller 50
                value = self.dice[5]
            else:
                value = self.dice[self.index_choice]

        #if value is None:
        #    value = self.choice

        if yellow_side is None:
            yellow_side = self.yellow_side

        if color == 0:  # YELLOW
            print('YELLOW')
            value_yellow = self.dice[0]
            print(yellow_side, value_yellow)
            index = self.yellow_dictionary[str(value_yellow)][yellow_side]
            row = index[0]
            col = index[1]
            self.yellow[row:row+1, col:col+1] = 1
            self.CheckYellowBonuses(row=row, col=col)

        if color == 1: # BLUE
            print('BLUE!')
            value_white = self.dice[5]
            value_blue = self.dice[1]
            blue_white_sum = value_blue + value_white

            # Placement
            row = (blue_white_sum - 1) // self.blue.shape[1]
            col = (blue_white_sum - 1) % self.blue.shape[1]
            print('row col', row, col)
            self.blue[row:row+1, col:col+1] = 1
            print(self.blue)
            self.CheckBlueBonuses(row=row, col=col)

        if color == 2: # GREEN
            print('GREEN')
            self.green_pos += 1
            self.CheckGreenOrangePurpleBonuses(color, self.green_pos)

        if color == 3:  # ORANGE
            self.orange_pos += 1
            if self.orange_pos in [3, 6, 8]:
                self.orange_sum += 2*value
            elif self.orange_pos == 10:
                self.orange_sum += 3*value
            else:
                self.orange_sum += value
            self.CheckGreenOrangePurpleBonuses(color, self.orange_pos)

        if color == 4:  # purple
            self.purple_pos += 1
            self.purple_sum += value
            if value == 6:
                self.purple_last_value = 0
            else:
                self.purple_last_value = value
            self.CheckGreenOrangePurpleBonuses(color, self.purple_pos)


    def CheckYellowBonuses(self, row, col):

        if np.all(self.yellow[row, :] == 1):
            if row == 0:
                pass
                self.bonus_choice = 1
                self.generatevalidoptions()
                # TODO: make a choice

            elif row == 1:
                self.MarkSheet(color=3, value=4) # add orange 4
            elif row == 2:
                self.MarkSheet(color=2, value=6) # add green (cross, value is irrelevant)
            elif row == 3:
                self.no_fox += 1

#Blue Bonusses. Two help-methods "BlueBonusRows", "BlueBonusCols" to simplify "CheckBlueBonuses"
    def BlueBonusRows(self, row):
        if row == 0:
            self.MarkSheet(color=3, value=5)
        elif row == 1:
            self.bonus_choice = 0
            self.generatevalidoptions()
            # TODO: make a yellow (0) choice
            pass
        elif row == 2:
            self.no_fox += 1

    def BlueBonusCols(self, col):
        if col == 0:
            self.rerolls += 1
        elif col == 1:
            self.MarkSheet(color=2, value=6)
        elif col == 2:
            self.MarkSheet(color=4, value=6)
        elif col == 3:
            self.plus_ones += 1

    def CheckBlueBonuses(self, row, col):
        if np.all(self.blue[row, :] == 1):
            self.BlueBonusRows(row)
        if np.all(self.blue[:, col] == 1):
            self.BlueBonusCols(col)

#Green Orange and Purple have similar bonus structure, so check is done together:

    def CheckGreenOrangePurpleBonuses(self, color, position):
        row = color - 2
        bonus = self.green_orange_purple_bonus[row, position]
        if bonus == 0:
            self.bonus_choice = 0
            self.generatevalidoptions()
            #TODO: choose yellow
            pass
        if bonus == 1:
            self.bonus_choice = 1
            self.generatevalidoptions()
            #todo: Choose blue
            pass
        if bonus == 2:
            self.MarkSheet(color=2, value=6)
        if bonus == 3:
            self.MarkSheet(color=3, value=6)
        if bonus == 4:
            self.MarkSheet(color=4, value=6)

    def printSheet(self):
        print('Yellow')
        print(self.yellow)
        print('Blue')
        print(self.blue)
        print('Green', self.green_pos)
        print('Orange', self.orange_pos)
        print('Green', self.purple_pos)

    def generatevalidoptions(self):
        """
        Description:
            Updates the valid options
        """

        self.valid_options = np.zeros(2*56 + 2, dtype=int)  #[False]*len(self.options)

        if self.bonus_choice is None:

            # YELLOW
            if self.dice_active[0] == 1:
                (row1, col1), (row2, col2) = self.yellow_dictionary[str(self.dice_values[0])]
                if self.yellow[row1, col1] == 0:
                    option_number = self.yellow_option_mapping[row1, col1]
                    print('yellow option', option_number)
                    self.valid_options[option_number] = 1
                if self.yellow[row2, col2] == 0:
                    option_number = self.yellow_option_mapping[row2, col2]
                    print('yellow option', option_number)
                    self.valid_options[option_number] = 1

            # YELLOW WHITE
            if self.dice_active[5] == 1:
                (row1_w, col1_w), (row2_w, col2_w) = self.yellow_dictionary[str(self.dice_values[5])]
                if self.yellow[row1_w, col1_w] == 0:
                    option_number = self.yellow_option_mapping[row1_w, col1_w] + 56
                    print('yellow white option', option_number)
                    self.valid_options[option_number] = 1
                if self.yellow[row2_w, col2_w] == 0:
                    option_number = self.yellow_option_mapping[row2_w, col2_w] + 56
                    print('yellow option', option_number)
                    self.valid_options[option_number] = 1

            # BLUE
            if self.dice_active[1] == 1:
                blue_white_sum = self.dice_values[1] + self.dice_values[5]
                row = (blue_white_sum - 1) // self.blue.shape[1]
                col = (blue_white_sum - 1) % self.blue.shape[1]
                if self.blue[row, col] == 0:
                    self.valid_options[11 + blue_white_sum - 1] = 1

            if self.dice_active[5] == 1:
                blue_white_sum = self.dice_values[1] + self.dice_values[5]
                row = (blue_white_sum - 1) // self.blue.shape[1]
                col = (blue_white_sum - 1) % self.blue.shape[1]
                if self.blue[row, col] == 0:
                    self.valid_options[56 + 11 + blue_white_sum - 1] = 1  # WHITE

            # GREEN
            if self.dice_active[2] == 1:
                if self.green_bounds[self.green_pos+1] <= self.dice_values[2]:
                    if self.green_pos < 10:
                        self.valid_options[2*11 + (self.green_pos+2)] = 1

            # GREEN WHITE
            if self.dice_active[5] == 1:
                if self.green_bounds[self.green_pos+1] <= self.dice_values[5]:
                    if self.green_pos < 10:
                        self.valid_options[56 + 2*11 + (self.green_pos+2)] = 1

            # ORANGE
            if self.dice_active[3] == 1:
                if self.orange_pos < 10:
                    self.valid_options[3 * 11 + (self.orange_pos + 2)] = 1

            # ORANGE WHITE
            if self.dice_active[5] == 1:
                if self.orange_pos < 10:
                    self.valid_options[56 + 3 * 11 + (self.orange_pos + 2)] = 1

            # PURPLE
            if self.dice_active[4] == 1:
                if self.dice_values[3] > self.purple_last_value:
                    if self.purple_pos < 10:
                        print('Purple option', 4*11 + (self.purple_pos+2))
                        self.valid_options[4*11 + (self.purple_pos+2)] = 1

            # PURPLE WHITE
            if self.dice_active[5] == 1:
                if self.dice_values[5] > self.purple_last_value:
                    if self.purple_pos < 10:
                        print('Purple white option', 56 + 4*11 + (self.purple_pos+2))
                        self.valid_options[56 + 4*11 + (self.purple_pos+2)] = 1

            # SPECIAL ACTIONS
            if self.rerolls > 0:
                self.valid_options[56 + 5*11 + 1] = 1
            if self.plus_ones > 0:
                self.valid_options[56 + 5*11 + 3] = 1

            print(len(self.valid_options), self.valid_options)


        # YELLOW BONUS
        elif self.bonus_choice == 0:
            for row in range(0, 4):
                for col in range(0, 3):
                    if row + col != 3:
                        if self.yellow[row, col] == 0:
                            option_number = self.yellow_option_mapping[row, col]
                            self.valid_options[option_number] = 1

        # BLUE BONUS
        elif self.bonus_choice == 1:
            for blue_white_sum in range(2, 13):
                row = (blue_white_sum - 1) // self.blue.shape[1]
                col = (blue_white_sum - 1) % self.blue.shape[1]
                if self.blue[row, col] == 0:
                    self.valid_options[11 + blue_white_sum - 1] == 1

        print('YELLOW OPTIONS', self.valid_options[:12])
        print('BLUE OPTIONS', self.valid_options[12:12 + 11])
        print('GREEN OPTIONS', self.valid_options[12 + 11:12 + 2 * 11])
        print('ORANGE OPTIONS', self.valid_options[12 + 2 * 11:12 + 3 * 11])
        print('PURPLE OPTIONS', self.valid_options[12 + 3 * 11:12 + 4 * 11])
        print('YELLOW WHITE OPTIONS', self.valid_options[56:56+12])
        print('BLUE WHITE OPTIONS', self.valid_options[56+12:56+12 + 11])
        print('GREEN WHITE OPTIONS', self.valid_options[56+12 + 11:56+12 + 2 * 11])
        print('ORANGE WHITE OPTIONS', self.valid_options[56+12 + 2 * 11:56+12 + 3 * 11])
        print('PURPLE WHITE OPTIONS', self.valid_options[56+12 + 3 * 11:56+12 + 4 * 11])
        print('OTHER WHITE OPTIONS', self.valid_options[56+12+4*11:])

        #TODO: Mapping function from valid_options to options

        #if self.yellow[tuple(zip(*self.yellow_dictionary[self.dice_values[0]]))][0] == 0:
            #    self.valid_options[] = True






if __name__ == '__main__':
    gs = GameSheet()
    #print(gs.yellow)
    #print(gs.blue)
    #print(gs.green)
    #print(gs.orange)
    #print(gs.purple)

    print('Active rolls:')
    for i in range(0, 3):
        print('-'*20, 'Saa rulles slag nr. ', i+1)
        if np.any(gs.dice_active > 0):
            gs.ActiveRoll()
            gs.MarkSheet()
    gs.dice_active = np.ones(6, dtype=int) #reset, all dice in play again.

    print('#'*50)
    print('Passive roll:')
    gs.PassiveRoll()
    gs.generatevalidoptions()
    gs.MarkSheet()
    gs.printSheet()
