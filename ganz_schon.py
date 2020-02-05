import numpy as np

class GameSheet(object):

    def __init__(self):

        # Board
        self.yellow = np.eye(4)[::, ::-1]
        self.yellow_dictionary = {'1': [(2, 0), (1, 1)],
                                    '2': [(1, 0), (2, 2)],
                                    '3': [(0, 0), (3, 1)],
                                    '4': [(3, 2), (2, 3)],
                                    '5': [(0, 2), (1, 3)],
                                    '6': [(0, 1), (3, 3)],
                                   }


        self.blue = np.zeros((3, 4))
        self.blue[0, 0] = 1

        self.green_pos = 0 # np.zeros(11, dtype=int)
        self.orange_pos = 0
        self.orange_sum = 0
        self.purple_pos = 0
        self.purple_sum = 0

        self.choice = None
        self.last_mark = None
        self.yellow_side = None

        self.no_fox = 0


        # Dice
        # yellow (0), blue (1), green (2), orange (3), purple (4), white (5)
        self.dice = np.zeros(6, dtype=int)
        self.dice_active = np.ones(6, dtype=int)

    def Roll(self):
        print('Pre-Roll', self.dice[self.dice_active > 0], self.dice, self.dice_active)
        self.dice[self.dice_active > 0] = np.random.choice(6, np.sum(self.dice_active[self.dice_active > 0])) + 1
        return self.dice

    def OneRoll(self):
        dice_values = self.Roll()
        #active_dice_values = dice_values[self.dice_active]

        options = np.argwhere(self.dice_active > 0).ravel()
        self.index_choice = np.random.choice(options)

        # CHOICE MUST BE MADE
        self.choice, self.yellow_side = self.dice[self.index_choice], np.random.choice([0,1],1)[0] # TODO: Implement fancy algorithm choice nice mega awesome function here

        print('options', options, 'choice is', self.choice, 'with index', self.index_choice)

        self.dice_active[self.dice_active > 0] = np.where(self.choice > dice_values, 0, self.dice_active)[self.dice_active > 0]
        self.dice_active[self.index_choice] = -1

        active = self.dice[self.dice_active > 0]

        print('Dice values', dice_values, 'Active dice values', active, 'Dice_active_index', self.dice_active)

        return self.choice

    def MarkSheet(self, color=None, value=None, yellow_side=None):

        if color is None:
            color = self.index_choice
        if value is None:
            value = self.choice
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
            value = value + value_white

            # Placement
            row = (value - 1) // self.blue.shape[1]
            col = (value - 1) % self.blue.shape[1]
            print('row col', row, col)
            self.blue[row:row+1, col:col+1] = 1
            print(self.blue)

        if color == 2: # GREEN
            print('GREEN')
            self.green_pos += 1

        if color == 3:  # ORANGE
            self.orange_pos += 1
            self.orange_sum += value

        if color == 4:  # purple
            self.purple_pos += 1
            self.purple_sum += value

    def CheckYellowBonuses(self, row, col):

        if np.all(self.yellow[row, :] == 1):
            if row == 0:
                pass
                # make a choice
            elif row == 1:
                self.MarkSheet(color=3, value=4) # add orange 4
            elif row == 2:
                self.MarkSheet(color=2, value=6) # add green (cross, value is irrelevant)
            elif row == 3:
                self.no_fox += 1


if __name__ == '__main__':
    gs = GameSheet()

    #print(gs.yellow)
    #print(gs.blue)
    #print(gs.green)
    #print(gs.orange)
    #print(gs.purple)

    for i in range(0, 3):
        print('-'*20, 'Så rulles slag nr. ', i+1)
        if np.any(gs.dice_active > 0):
            gs.OneRoll()
            #
            gs.MarkSheet()




