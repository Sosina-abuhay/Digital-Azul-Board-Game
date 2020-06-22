"""
 *****************************************************************************
   FILE:       game.py

   AUTHOR:     Sosina Abuhay

   ASSIGNMENT: Final Project

   DATE:       12/11/2019

   DESCRIPTION: A version of Azul board game where players don't have to
                manually calculate their scores.

 *****************************************************************************
"""

from random import choice
from random import sample
from cs110graphics import *

# Global Variables:
PLAYER_NUM = 2
TILE_SIZE = 50
SCORE_BOARD_SIZE = 25
SCORE_SQUARE_COLOR = 'white'
FACTORY_SIZE = 50
FACTORY_CAPACITY = 4
FACTORY_NUM = 5
FACTORY_ORIGINAL_COLOR = 'white'
TILE_TYPE = 5
FACTORY_Y_OFFSET = 50
STREET_SIZE = 50
WALL_SIZE = 50
TILE_COLORS = ['teal', 'darkorange', 'maroon', 'olive', 'cornflowerblue']
STREET_ORIGINAL_NUMBER = '0'
LADDER_ORIGINAL_COLOR = 'white'
BUTTON_COLOR = 'palegreen'
BUTTON_RADIUS = 10
ORIGINAL_TILE_POSITION = (1000, 1000)
PLAYER1_STARTER_POS = (300, 200)
PLAYER2_STARTER_POS = (1100, 200)
START_BUTTON_ORIGINAL_POSITION = (700, 580)


class Game:
    """ Class for the whole Game. """

    def __init__(self, window):
        """ The constructor method for the Game class. """

        # Assigns attributes for objects in the Game.
        self._window = window
        self._allfactories = []
        self._street = []
        self._wall1 = []
        self._wall2 = []
        self._allwalls = []
        self._ladder1 = []
        self._ladder2 = []
        self._allladders = []
        self._button1 = []
        self._button2 = []
        self._allbuttons = []
        self._alltiles = []
        self._tiles_on_factory = []
        self._tiles_on_street = [[], [], [], [], []]
        self._tiles_on_ladder1 = [[], [], [], [], []]
        self._tiles_on_ladder2 = [[], [], [], [], []]
        self._tiles_on_scorer1 = []
        self._tiles_on_scorer2 = []
        self._discarded_tiles = []
        self._players = []
        self._scorer1 = []
        self._scorer2 = []
        self._allscorer = []
        self._pointer1 = [[], []]
        self._pointer2 = [[], []]
        self._allpointers = []
        self._scorer_buttons = []
        self._starter_tile = None
        self._tile_clicked = False
        self._button_clicked = False
        self._street_clicked = False
        self._clicked_first_street = False
        self._game_over = False
        self._round_over = False
        self._arranged_on_ladder = False
        self._scorer_button_clicked = False
        self._empty_factories = 0
        self._empty_street_boxes = 0
        self._next_round_starter = 0
        self._start_button = None

        # Opens the welcome page of the game.
        self.welcome()

        # Creates and draws tiles.
        self.create_tiles()
        self.draw_tiles()

        # Creates the player objects.
        self.create_player()

        # Creates and draws the starter tile.
        self.create_starter_tile()
        self.draw_starter_tile()

    def welcome(self):
        """ Welcomes the players to the Game by opening the Welcome page. """

        # Gets the height and width of the graphics window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Calculates the center for the welcome message.
        center = ((width // 2), ((height // 2) - 50))

        # Creates a background image object.
        background = Image(self._window, 'azul.jpeg', width, height, (center[0], \
        (center[1] + 50)))

        # Assigns size and text for the welcome message.
        text = 'Welcome to Azul!'
        text_size = 100

        # Creates a welcome message text object.
        welcome_text = Text(self._window, text, text_size, center)

        # Sets the depth of the welcome message text.
        welcome_text.set_depth(20)

        # Adds the welcome message and the background image to the window.
        self._window.add(background)
        self._window.add(welcome_text)

        # Creates the start button.
        self.create_start_button()

    def create_start_button(self):
        """ Creates the StartButton for the Game. """

        # Creates attributes for the StartButton.
        center = START_BUTTON_ORIGINAL_POSITION
        text_color = 'black'
        text = 'Click this circle to start.'
        button_width = 160
        button_heigth = 160

        # Creates a StartButton by calling the StartButton class.
        self._start_button = StartButton(self._window, center, text_color, text, \
        button_width, button_heigth, self)

        # Draws the StartButton.
        self._start_button.draw()

    def start_game(self):
        """ Starts the Game when the StartButton is clicked. """

        # Sets the background of the game.
        self.set_background()

        # Creates and draws factories.
        self.create_factory()
        self.draw_factory()

        # Creates and draws the street.
        self.create_street()
        self.draw_street()

        # Creates and draws the walls.
        self.create_wall()
        self.draw_wall()

        # Creates and draws the ladders.
        self.create_ladder()
        self.draw_ladder()

        # Creates and draws the buttons.
        self.create_button()
        self.draw_button()

        # Creates and draws the scorers.
        self.create_scorer()
        self.draw_scorer()

        # Creates and draws the pointers.
        self.create_pointer()
        self.draw_pointer()

        # Creates and draws the scorer buttons.
        self.create_scorer_buttons()
        self.draw_scorer_buttons()

        # Fills the factories.
        self.fill_factory()

    def create_player(self):
        """ Creates two Player objects. """

        # Calls the Player class to make two player objects.
        for id in range(PLAYER_NUM):
            self._players.append(Player(id))

    def set_background(self):
        """ Creates the background image of the Game and adds it to window. """

        # Gets the height and width of the window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Calculates the center for the background image.
        center = ((width // 2), (height // 2))

        # Creates and adds the background image to the window.
        background = Image(self._window, 'back.gif', width, height, center)
        background.set_depth(0)
        self._window.add(background)

    def create_factory(self):
        """ Creates all the factories. """

        # Gets the width and height of the window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Calculates the total width of a factory.
        total_width = FACTORY_SIZE * FACTORY_NUM

        # Calculates the x and y offset for the factories.
        x_offset = (width - total_width) // 2 + 2 * (TILE_SIZE // 2)
        y_offset = FACTORY_Y_OFFSET

        # Assigns a vertical gap from the start of the window to the factories.
        gap = 30

        # Creates the factories.
        for id in range(FACTORY_NUM):

            # Assigns an empty list for each factory.
            factory = []

            # Creates each box of a factory by calling the FactoryBoxes class.
            for counter in range(FACTORY_CAPACITY):
                box = FactoryBoxes(self._window, (id + 1), \
                (x_offset + counter * FACTORY_SIZE), y_offset, FACTORY_SIZE, \
                FACTORY_ORIGINAL_COLOR, counter)

                # Adds each box of a factory to the factory list.
                factory.append(box)

            # Changes the y_offset to draw factories vertically.
            y_offset += ((FACTORY_SIZE // 2) + gap)

            # Appends each factory to a list.
            self._allfactories.append(factory)

    def draw_factory(self):
        """ Draws the factories. """

        # Loops through the factory list and the boxes of a factory.
        for factory in self._allfactories:
            for box in factory:
                box.draw()

    def create_street(self):
        """ Creates the street. """

        # Gets the width and height of the window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Calculates the total width of the street.
        total_width = STREET_SIZE * TILE_TYPE

        # Assigns a vertical gap from the start of the window to the factories.
        gap = 30

        # Calculates the x and y offset of the StreetBoxes.
        x_offset = (width - total_width) // 2 + (STREET_SIZE // 2)
        y_offset = FACTORY_Y_OFFSET + (FACTORY_NUM * FACTORY_SIZE) + gap

        # Creates each box of a street by calling the StreetBoxes class.
        for counter in range(TILE_TYPE):
            box = StreetBoxes(self._window, (x_offset + counter * STREET_SIZE), \
            y_offset, STREET_SIZE, TILE_COLORS[counter], STREET_ORIGINAL_NUMBER, \
            counter, self)

            # Appends each box of the street to a list.
            self._street.append(box)

    def draw_street(self):
        """ Draws the street. """

        # Loops through the street list to draw each box.
        for box in self._street:
            box.draw()

    def create_wall(self):
        """ Creates the walls. """

        # Assigns the colors for the wall boxes to create the diagonals.
        colors = [['teal', 'darkorange', 'maroon', 'olive', 'cornflowerblue'], \
        ['cornflowerblue', 'teal', 'darkorange', 'maroon', 'olive'], \
        ['olive', 'cornflowerblue', 'teal', 'darkorange', 'maroon'], \
        ['maroon', 'olive', 'cornflowerblue', 'teal', 'darkorange'], \
        ['darkorange', 'maroon', 'olive', 'cornflowerblue', 'teal']]

        # Gets the width and height of the window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Assigns vertical and horizontal gap for the first street.
        horizontal_gap = 50
        vertical_gap = 80

        # Calculates y offset for the first wall.
        y_pos = FACTORY_Y_OFFSET + (FACTORY_NUM * FACTORY_SIZE) + (WALL_SIZE)

        # Makes the wall of the first player.
        for row in range(FACTORY_NUM):
            player = 0

            # Assigns x offset for the first wall.
            x_pos = (horizontal_gap * 2) + (WALL_SIZE * TILE_TYPE) + \
            (WALL_SIZE // 2)

            # Initializes an empty list for each row.
            row_box = []

            # Choses a color for each box.
            color_list = colors[row]

            # Increments the y position by the WALL_SIZE.
            y_pos += WALL_SIZE

            # Loops through the columns that make up the wall.
            for col in range(FACTORY_NUM):

                # Assigns color for each box.
                color = color_list[col]

                # Increments the x position by the WALL_SIZE.
                x_pos += WALL_SIZE

                # Creates a WallBox by calling the WallBoxes class.
                box = WallBoxes(self._window, x_pos, y_pos, WALL_SIZE, color, \
                row, col, player)

                # Appends each box to a list.
                row_box.append(box)

            # Appends each row to a list.
            self._wall1.append(row_box)

        # Appends the wall of the first player to a list.
        self._allwalls.append(self._wall1)

        # Calculates the y offset of the wall for the second player.
        y_pos = FACTORY_Y_OFFSET + (FACTORY_NUM * FACTORY_SIZE) + (WALL_SIZE)

        # Makes the wall of the second player.
        for row in range(TILE_TYPE):
            player = 1

            # Assigns x offset for the second wall.
            x_pos = (width - ((horizontal_gap * 2) + (WALL_SIZE * TILE_TYPE)))

            # Initializes an empty list for each row.
            row_box = []

            # Choses a color for each box.
            color_list = colors[row]

            # Increments the y position by the WALL_SIZE.
            y_pos += WALL_SIZE

            # Loops through the columns that make up the wall.
            for col in range(TILE_TYPE):

                # Assigns color for each box.
                color = color_list[col]

                # Increments the x position by the WALL_SIZE.
                x_pos += WALL_SIZE

                # Creates a WallBox by calling the WallBoxes class.
                box = WallBoxes(self._window, x_pos, y_pos, WALL_SIZE, color, \
                row, col, player)

                # Appends each box to a list.
                row_box.append(box)

                # Appends each row to a list.
            self._wall2.append(row_box)

        # Appends the wall of the second player to a list.
        self._allwalls.append(self._wall2)

    def draw_wall(self):
        """ Draws the boxes that make up the walls. """

        # Draws the wall of the first player by looping through the list.
        for row in self._wall1:
            for entry in row:
                entry.draw()

        # Draws the wall of the second player by looping through the lsit.
        for row in self._wall2:
            for entry in row:
                entry.draw()

    def create_ladder(self):
        """ Creates the ladders. """

        # Assigns o for no box and 1 for a box to make the ladder.
        ladder = [[0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], \
        [0, 1, 1, 1, 1], [1, 1, 1, 1, 1]]

        # Gets the width of the window.
        width = self._window.get_width()

        # Assigns a horizontal and vertical gap for the first ladder.
        horizontal_gap = 50
        vertical_gap = 80

        # Calculates y offset for the first ladder.
        y_pos = FACTORY_Y_OFFSET + (FACTORY_NUM * FACTORY_SIZE) + (WALL_SIZE)

        # Draws a ladder for the first player.
        for row in range(TILE_TYPE):
            player = 0

            # Assigns x offset for the first ladder.
            x_pos = horizontal_gap

            # Initializes an empty list for each row.
            row_box = []

            # Determines the list for each row.
            ladder_list = ladder[row]

            # Increments the y offset by WALL_SIZE.
            y_pos += WALL_SIZE

            # Loops through the columns that make up the ladder.
            for col in range(TILE_TYPE):

                # Assigns value for each box.
                value = ladder_list[col]

                # Increments the x offset by WALL_SIZE.
                x_pos += WALL_SIZE

                # Creates a LadderBox by calling LadderBoxes class.
                if value == 1:
                    box = LadderBoxes(self._window, x_pos, y_pos, \
                    WALL_SIZE,LADDER_ORIGINAL_COLOR, row, col, player)

                    # Appends each box to a row list.
                    row_box.append(box)

            # Appends each row list to a ladder.
            self._ladder1.append(row_box)

        # Appends the first ladder to the all ladders list.
        self._allladders.append(self._ladder1)

        # Calculates y offset for the first ladder.
        y_pos = FACTORY_Y_OFFSET + (FACTORY_NUM * FACTORY_SIZE) + (WALL_SIZE)

        # Draws the ladder for the second player.
        for row in range(TILE_TYPE):
            player = 1

            # Assigns x offset for the first ladder.
            x_pos = (width - (((horizontal_gap * 3) + \
            2 * (WALL_SIZE * TILE_TYPE)) + (WALL_SIZE // 2)))

            # Initializes an empty list for each row.
            row_box = []

            # Determines the list for each row.
            ladder_list = ladder[row]

            # Increments the y offset by WALL_SIZE.
            y_pos += WALL_SIZE

            # Loops through the columns that make up the ladder.
            for col in range(TILE_TYPE):

                # Assigns value for each box.
                value = ladder_list[col]

                # Increments the x offset by WALL_SIZE.
                x_pos += WALL_SIZE

                # Creates a LadderBox by calling LadderBoxes class.
                if value == 1:
                    box = LadderBoxes(self._window, x_pos, y_pos, \
                    WALL_SIZE,LADDER_ORIGINAL_COLOR, row, col, player)

                    # Appends each box to a row list.
                    row_box.append(box)

            # Appends each row list to a ladder.
            self._ladder2.append(row_box)

        # Appends the first ladder to the all ladders list.
        self._allladders.append(self._ladder2)

    def draw_ladder(self):
        """ Draws each box that make up a ladder. """

        # Draws the first ladder.
        for row in self._ladder1:
            for entry in row:
                entry.draw()

        # Draws the second ladder.
        for row in self._ladder2:
            for entry in row:
                entry.draw()

    def create_button(self):
        """ Creates the buttons. """

        # Gets the width of the window.
        width = self._window.get_width()

        # Assigns horizontal and vertical gap for the buttons.
        horizontal_gap = 50
        vertical_gap = 80

        # Calculates x and y offset for the first set of buttons.
        y_pos = FACTORY_Y_OFFSET + (FACTORY_NUM * FACTORY_SIZE) + 2 * (WALL_SIZE)
        x_pos = horizontal_gap + (TILE_TYPE * WALL_SIZE) + WALL_SIZE

        # Draws buttons for the first player.
        for row in range(TILE_TYPE):
            player = 0

            # Creates button objects by calling the Button class.
            button = Button(self._window, BUTTON_COLOR, BUTTON_RADIUS, x_pos, \
            y_pos, row, player, self)

            # Appends all the first set of buttons to a list.
            self._button1.append(button)

            # Increments the y offset by a WALL_SIZE
            y_pos += WALL_SIZE

        # Appends the list of buttons of the first player to a list.
        self._allbuttons.append(self._button1)

        # Assigns y and x offset for the second set of buttons.
        y_pos = FACTORY_Y_OFFSET + (FACTORY_NUM * FACTORY_SIZE) + 2 * (WALL_SIZE)
        x_pos = (width - (((horizontal_gap * 3) + 2 * (WALL_SIZE * TILE_TYPE)) + \
        (WALL_SIZE // 2))) + WALL_SIZE + (WALL_SIZE * TILE_TYPE)

        # Draws the buttons for the second player.
        for row in range(TILE_TYPE):
            player = 1

            # Creates button objects by calling the Button class.
            button = Button(self._window, BUTTON_COLOR, BUTTON_RADIUS, x_pos, \
            y_pos, row, player, self)

            # Appends all the second set of buttons to a list.
            self._button2.append(button)

            # Increments the y offset by a WALL_SIZE
            y_pos += WALL_SIZE

        # Appends the list of buttons of the second player to a list.
        self._allbuttons.append(self._button2)

    def draw_button(self):
        """ Draws the buttons. """

        # Draws the buttons for player 1.
        for button in self._button1:
            button.draw()

        # Draws the buttons for player 2.
        for button in self._button2:
            button.draw()

    def create_scorer(self):
        """ Creates the scorers. """

        # Assigns number for each box.
        number_list = ['-1', '-1', '-2', '-2', '-2', '-3', '-3']

        # Gets the width and height of the window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Assigns the x and y offset of the first scorer.
        y_offset = height - 75
        x_offset = 200

        # Draws the scorer for the first player.
        for number in range(7):
            player = 0

            # Assigns a number for each box.
            text = number_list[number]

            # Creates a ScorerBox by calling the ScorerBoxes class.
            box = ScorerBoxes(self._window, (x_offset + number * WALL_SIZE), \
            y_offset, WALL_SIZE, LADDER_ORIGINAL_COLOR, text, player)

            # Appends each box to a list.
            self._scorer1.append(box)

        # Appends the first scorer to a list.
        self._allscorer.append(self._scorer1)

        # Assigns the x and y offset of the second scorer.
        y_offset = height - 75
        x_offset = width - ((11 * WALL_SIZE)) + (WALL_SIZE // 2)

        # Draws the scorer for the second player.
        for number in range(7):
            player = 1

            # Assigns a number for each box.
            text = number_list[number]

            # Creates a ScorerBox by calling the ScorerBoxes class.
            box = ScorerBoxes(self._window, (x_offset + number * WALL_SIZE), \
            y_offset, WALL_SIZE, LADDER_ORIGINAL_COLOR, text, player)

            # Appends each box to a list.
            self._scorer2.append(box)

        # Appends the second scorer to a list.
        self._allscorer.append(self._scorer2)

    def draw_scorer(self):
        """ Draws ScorerBoxes. """

        # Draws both the scorers by looping through the all scorers list.
        for scorer in self._allscorer:
            for box in scorer:
                box.draw()

    def create_scorer_buttons(self):
        """ Creates the scorer buttons. """

        # Gets the width and height of the window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Assigns x and y offset for the first scorer button.
        x_pos = 550
        y_pos = height - 75

        # Assigns the player id.
        player = 0

        # Draws a scorer button for the first player.
        scorer_button1 = ScorerButton(self._window, BUTTON_COLOR, BUTTON_RADIUS, \
        x_pos, y_pos, player, self)

        # Appends the first scorer to a list.
        self._scorer_buttons.append(scorer_button1)

        # Assigns x and y offset for the second scorer button.
        x_pos = 825
        y_pos = height - 75

        # Assigns the player id.
        player = 1

        # Draws a scorer button for the first player.
        scorer_button2 = ScorerButton(self._window, BUTTON_COLOR, BUTTON_RADIUS, \
        x_pos, y_pos, player, self)

        # Appends the first scorer to a list.
        self._scorer_buttons.append(scorer_button2)

    def draw_scorer_buttons(self):
        """ Draws the scorer buttons. """

        # Draws both scorer buttons.
        for button in self._scorer_buttons:
            button.draw()

    def create_pointer(self):
        """ Creates pointer for each player. """

        # Gets the width and height of the window.
        width = self._window.get_width()
        height = self._window.get_height()

        # Assigns the position for the first player's text and number.
        text_xpos = 250
        text_ypos = 100
        num_xpos = 450

        # Assigns the text for the first pointer.
        text = "Player 1's Score: "
        number = '0'

        # Assigns the size of the pointers.
        size = 35

        # Creates a text of a pointer for the first player.
        pointer_text = Pointer(self._window, (text_xpos, text_ypos), text, size)

        # Appends the text to a list.
        self._pointer1[0].append(pointer_text)

        # Creates the number of a pointer for the first player.
        pointer_number = Pointer(self._window, (num_xpos, text_ypos), number, \
        size)

        # Appends the number to a list.
        self._pointer1[1].append(pointer_number)

        # Appends the first pointer to a list.
        self._allpointers.append(self._pointer1)

        # Assigns the position for the first player's text and number.
        text_xpos = 1100
        num_xpos = 1300

        # Assigns the text for the second pointer.
        text = "Player 2's Score: "

        # Creates a pointer for the second player.
        pointer_text = Pointer(self._window, (text_xpos, text_ypos), text, size)

        # Appends the text to a list.
        self._pointer2[0].append(pointer_text)

        # Creates the number of a pointer for the second player.
        pointer_number = Pointer(self._window, (num_xpos, text_ypos), number, \
        size)

        # Appends the number to a list.
        self._pointer2[1].append(pointer_number)

        # Appends the second pointer to a list.
        self._allpointers.append(self._pointer2)

    def draw_pointer(self):
        """ Darws the pointers. """

        # Draws both pointers for each player.
        for pointer in self._allpointers:
            for list in pointer:
                for item in list:
                    item.draw()

    def create_tiles(self):
        """ Creates the tiles. """

        # Assigns original positions off the screen.
        x_pos = ORIGINAL_TILE_POSITION[0]
        y_pos = ORIGINAL_TILE_POSITION[1]

        # Creates 20 tiles of each color.
        for color in TILE_COLORS:
            for _ in range(20):
                tile = Tiles(self._window, color, TILE_SIZE, x_pos, y_pos, self)

                # Appends all the tiles to a list.
                self._alltiles.append(tile)

    def draw_tiles(self):
        """ Darws the tiles. """

        # Draws all the tiles off the window.
        for tile in self._alltiles:
            tile.draw()

    def create_starter_tile(self):
        """ Creates the starter tile. """

        # Assigns x and y positions off the window for the starter tile.
        x_pos = ORIGINAL_TILE_POSITION[0]
        y_pos = ORIGINAL_TILE_POSITION[1]

        # Assigns attributes for the starter tile.
        color = 'rosybrown'
        text = 'S'
        radius = 30

        # Creates the starter tile by calling the StarterTile class.
        tile = StarterTile(self._window, color, x_pos, y_pos, text, radius)

        # Assigns the starter tile to an object.
        self._starter_tile = tile

    def draw_starter_tile(self):
        """ Draws the StarterTile. """

        # Draws the starter tile.
        self._starter_tile.draw()

    def fill_factory(self):
        """ Fills the factories with tile to start the Game. """

        # Clears all the tiles from the tiles_on_factory list.
        self._tiles_on_factory.clear()

        # For each factory, randomly chooses tiles.
        for factory in self._allfactories:
            tile_list = []
            for box in factory:
                center = box.get_center()
                tile = choice(self._alltiles)

                # Moves the tiles to the center of the factory boxes.
                tile.move_tile(center)
                tile_list.append(tile)

                # Removes the dealt tiles from the bad.
                self._alltiles.remove(tile)

            # Appends each list to tiles_on_factory.
            self._tiles_on_factory.append(tile_list)

    def check_game(self):
        """ Checks if the game is over. """

        # Initializes a list.
        winners = []

        # Loops through each walls.
        for player in range(PLAYER_NUM):

            # Loops through each row of a wall.
            for row in self._allwalls[player]:
                filled_boxes = 0

                # Loops through each box of a row.
                for box in row:

                    # Checks if all the boxes in the row are occupied.
                    if not box.get_availability():
                        filled_boxes += 1

                # If 5 boxes in a row are occupied, it ends the game.
                if filled_boxes == 5:
                    winners.append(player)

        # If atleast 1 player has a finished row, then the game is over.
        if len(winners) >= 1:
            self._game_over = True

            # Calculates the final point of the players.
            self.calculate_final_point()

    def calculate_final_point(self):
        """ Calculates the final point of the players. """

        # Loops through the player list.
        for player in range(PLAYER_NUM):
            completed_rows = 0

            # Calculates how many rows a player filled.
            for row in self._allwalls[player]:
                filled_boxes = 0
                for box in row:
                    if not box.get_availability():
                        filled_boxes += 1
                if filled_boxes == 5:
                    completed_rows += 1

            # Adds 2 points to the player for each completed rows.
            self._allpointers[player][1][0].add_point(2 * completed_rows)

            # Initializes the completed columns.
            completed_columns = 0

            # Calculates the number of columns a player filled.
            for counter in range(len(TILE_COLORS)):
                filled_vertical_boxes = 0
                for row in self._allwalls[player]:
                    if not row[counter].get_availability():
                        filled_vertical_boxes += 1
                if filled_vertical_boxes == 5:
                    completed_columns += 1

            # Adds 7 points to the player for each completed columns.
            self._allpointers[player][1][0].add_point(7 * completed_columns)

            # Initializes completed colors.
            completed_colors = 0

            # Calculates the number of colora that a player filled.
            for counter, color in enumerate(TILE_COLORS):
                filled_colors = 0
                for row in self._allwalls[player]:
                    for box in row:
                        box_color = box.get_color()
                        if box_color == color:
                            if not box.get_availability():
                                filled_colors += 1
                if filled_colors == 5:
                    completed_colors += 1

            # Adds 10 points to the player for each completed colors.
            self._allpointers[player][1][0].add_point(10 * completed_colors)

            # Determines the winner of the game.
            self.determine_winner()


    def determine_winner(self):
        """ Compares the scores of players to determine the winner."""

        # Initializes maximum score and a winner.
        max_score = 0
        winner = 0

        # Compares the final scores of the players.
        for player in range(PLAYER_NUM):
            final_score = self._allpointers[player][1][0].get_score()
            if final_score > max_score:
                max_score = final_score
                winner = player

        # Sends the winner of the game for the celebrate method.
        self.celebrate(winner)

    def celebrate(self, winner):
        """ Celebrates the winner. """

        # Gets the height and width of the window.
        height = self._window.get_height()
        width = self._window.get_width()

        # Calculates the center for the background image.
        center = ((width // 2), (height // 2))

        # Creates and adds a background image to the window.
        background = Image(self._window, 'azul.jpeg', width, height, center)
        background.set_depth(-20)
        self._window.add(background)

        # Assigns the size and text of the Congratulations text.
        size = 80
        text2 = 'Congratulations player {}!'.format(winner + 1)

        # Creates and adds the Congratulations message to the window.
        text_object1 = Text(self._window, text2, size, center)
        text_object1.set_depth(-23)
        self._window.add(text_object1)

    def check_round(self):
        """ Checks if a round is completed. """

        # Initializes empty street and factories.
        self._empty_factories = 0
        self._empty_street_boxes = 0

        # Loops through the factory to find out how many are empty.
        for factory in self._tiles_on_factory:
            if len(factory) == 0:
                self.check_filled_rows()
                self._empty_factories += 1

        # Loops through the street to find out how many boxes are empty.
        for box in self._tiles_on_street:
            if len(box) == 0:
                self.check_filled_rows()
                self._empty_street_boxes += 1

        # If 5 factories and 5 street boxes are empty, the round is over.
        if self._empty_factories == 5 and self._empty_street_boxes == 5:
            self._round_over = True

    def check_scorer(self):
        """ Checks if players have tiles on their scorer. """

        # Checks of the sorer of the first player has a tile on it.
        if len(self._tiles_on_scorer1) > 0:

            # Makes the scorer button if the scorer contains a tile.
            self._scorer_buttons[0].make_clickable()

        # Checks of the sorer of the second player has a tile on it.
        if len(self._tiles_on_scorer2) > 0:

            # Makes the scorer button if the scorer contains a tile.
            self._scorer_buttons[1].make_clickable()

    def check_filled_rows(self):
        """ Checks which ladder rows are filled. """

        # Loops through both ladders to find out the filled rows.
        for player in range(PLAYER_NUM):
            filled_rows = []
            for counter, list in enumerate(self._allladders[player]):
                occupied = []
                for box in list:
                    if not box.get_availability():
                        occupied.append(box)
                if len(occupied) == len(list):
                    filled_rows.append(counter)

            # If a row is filled, the button on that row becomes clickable.
            for row in filled_rows:
                self._allbuttons[player][row].make_clickable()

    def get_clickable_buttons(self):
        """ Returns a list of buttons that are clickable. """

        # Initializes a list.
        filled_row_buttons = []

        # Loops through the buttons to find out which are clickable.
        for list in self._allbuttons:
            for button in list:
                if button.is_clickable():
                    filled_row_buttons.append(button)

        # Returns the list of clickable buttons.
        return filled_row_buttons

    def tiles_on_filled_row(self, player, clicked_row):
        """ Returns a list of tiles that are in a filled row. """

        # Initializes a list.
        tile_list = []

        # Loops through the ladders to find out which tiles are on the ladder.
        if player == 0:
            for tile in self._tiles_on_ladder1[clicked_row]:
                tile_list.append(tile)
        else:
            for tile in self._tiles_on_ladder2[clicked_row]:
                tile_list.append(tile)

        # Returns a list of tiles that are on the ladder.
        return tile_list

    def get_maximum_index(self, grid, player):
        """ Receives a grid of of lists of '', 'yes' ,and 'new' and checks the
        longest sequence of yes,new with no '' in between. """

        # Initializes a list.
        points = []

        # Loops through the grid.
        for list in grid:
            new_pos = list.index('new')

            # Makes new lists based on the position of new.
            left_to_new = list[:new_pos]
            right_to_new = list[new_pos + 1:]
            left_point = 0
            right_point = 0

            # Initializes a boolean.
            please_break = False

            # Initializes a counter.
            counter = -1

            # Loops through the left list.
            for _ in range(len(left_to_new)):
                if not please_break:
                    if left_to_new[counter] == 'yes':
                        left_point += 1
                        counter += -1
                    else:
                        please_break = True

            # Initializes a boolean.
            please_break = False

            # Loops through the right list.
            for num in range(len(right_to_new)):
                if not please_break:
                    if right_to_new[num] == 'yes':
                        right_point += 1
                    else:
                        please_break = True

            # Calculates the points from each sides.
            point = 1 + left_point + right_point
            points.append(point)

        # Calculates the final point from the vertical and horizontal points.
        if points[0] == 1 or points[1] == 1:

            # Checks if the vertical and horizontal points are equal.
            if points[0] >= points[1]:
                total_point = points[0]

            # If they are not, it chooses the greater.
            elif points[0] < points[1]:
                total_point = points[1]

        # If both are different from 1, it gets their sum.
        else:
            total_point = points[0] + points[1]

        # Sends the calculates points to get scored.
        self.score_points(total_point, player)

    def score_points(self, points, player):
        """ Increases the score of a player by the points. """

        # Adds points to the number of a pointer.
        self._allpointers[player][1][0].add_point(points)

    def calculate_point(self, player, row_num, col_num):
        """ Forms a list of '', 'yes', and 'new' by looping through the boxes of
        a filled raw of a street.  """

        # Gets the filled rows.
        filled_row = self._allwalls[player][row_num]

        # Initializes a list.
        row_list = []

        # Loops through the filled rows.
        for counter, box in enumerate(filled_row):

            # Appends yes for a complete box, new for the new and '' for empty.
            if counter == col_num:
                entry = 'new'
            elif box.get_availability():
                entry = ''
            else:
                entry = 'yes'
            row_list.append(entry)

        # Initializes a list.
        col_list = []

        # Loops through the wall columns.
        for counter, row in enumerate(self._allwalls[player]):
            for box in row:
                box_col = box.get_col()
                if box_col == col_num:

                    # Appends yes for a complete, and '' for empty.
                    if counter == row_num:
                        entry = 'new'
                    elif box.get_availability():
                        entry = ''
                    else:
                        entry = 'yes'
                    col_list.append(entry)

        # Sends a grid to get the maximum index.
        self.get_maximum_index([row_list, col_list], player)

    def activate_all_players(self):
        """ Activates all the players. """

        # Activates all the players.
        for player in self._players:
            player.activate()

    def arrange_on_scorer(self):
        """ Arranges the clicked tiles on the scorer. """

        # Checks if a street is clicked.
        if self._street_clicked:

            # If the first street is clicked, starter tile is put.
            if not self._clicked_first_street:
                self._clicked_first_street = True
                self.put_starter_tile()

            # Gets a list of clicked tiles.
            tile_list = self.get_clicked_tile()

            # Sends all the list for point dedcution.
            self.deduct_point(tile_list)

            # Deacreases the number of a street box.
            self.decrease_street_number()

            # Gets the color of cliked tiles.
            tile_color = tile_list[0]

            # Finds the clicked street box and emptys the list.
            for id, box in enumerate(self._street):
                if box.is_clicked():
                    self._tiles_on_street[id].clear()

            # Unclicks the street.
            self.unclick_street()

        # If the clicked tiles are from a factory, they are sent for deduction.
        else:
            tile_list, unclicked_tiles = self.get_clicked_tile()
            self.arrange_on_street(unclicked_tiles)
            self.deduct_point(tile_list)

        # Arranges the tiles on wall.
        self._arranged_on_ladder = True

        # Makes final changes before changing players.
        self.make_changes()

    def street_is_clicked(self):
        """ Returns self._street_clicked. """

        return self._street_clicked

    def arrange_on_wall(self):
        """ Arranges tils on wall. """

        # Acticates all the players.
        self.activate_all_players()

        # Initializes player and clicked_row.
        player = 0
        clicked_row = 0

        # Gets a list of clickable_buttons.
        filled_row_buttons = self.get_clickable_buttons()

        # Loops through clickable buttons to get their row.
        if filled_row_buttons:
            for list in self._allbuttons:
                for row, button in enumerate(list):
                    if button.is_clicked():
                        player = button.get_player()
                        clicked_row = row

            # Gets a list of tiles on a filled row.
            tiles_on_filled_row = self.tiles_on_filled_row(player, clicked_row)

            # Gets the color of the tiles.
            tile_color = tiles_on_filled_row[0].get_color()

            # Checks the availability of each wall box.
            for counter, box in enumerate(self._allwalls[player][clicked_row]):
                box_color = box.get_color()
                if box_color == tile_color:
                    if box.get_availability():
                        box.occupy()
                        self.calculate_point(player, clicked_row, counter)

            # Unclicks the buttons.
            self.unclick_button()

            # Makes buttons unclickable.
            self._allbuttons[player][clicked_row].make_unclickable()

            # Removes all the tiles on a filled row.
            for tile in tiles_on_filled_row:
                tile.move_tile(ORIGINAL_TILE_POSITION)
                self._discarded_tiles.append(tile)
                if player == 0:
                    self._tiles_on_ladder1[clicked_row].clear()
                else:
                    self._tiles_on_ladder2[clicked_row].clear()

        # Gets a list of clickable buttons.
        filled_row_buttons = self.get_clickable_buttons()

        # Initializes clickable buttons.
        clickable_buttons = 0

        # If there are no clickable buttons, makes the scorer tiles clickable.
        if len(filled_row_buttons) == 0:
            for button in self._scorer_buttons:
                if button.is_clickable():
                    button.enable_clicking()
                    clickable_buttons += 1

            # Finalizes the sscore from the scorer.
            if clickable_buttons == 0:
                self.finalize_score()

    def finalize_score(self):
        """ Finalizes the score of a player by subtracting points based on the
        tiles on the scorer. """

        # Loops through scorer buttons and makes them unclickable.
        for button in self._scorer_buttons:
            if button.is_clicked():
                player = button.get_player()
                button.make_unclickable()
                button.disable_clicking()

                # Loops through the boxes of first scorer and puts a tile.
                if player == 0:
                    for box in self._scorer1:
                        if not box.get_availability():
                            point = box.get_number()
                            self.score_points(point, player)
                            box.unoccupy()

                    # Tiles on scorer1 are removed from the window.
                    for tile in self._tiles_on_scorer1:
                        tile.move_tile(ORIGINAL_TILE_POSITION)
                        self._discarded_tiles.append(tile)
                    self._tiles_on_scorer1.clear()

                # Loops throigh the boxes of second scorer and puts a tile.
                else:
                    for box in self._scorer2:
                        if not box.get_availability():
                            point = box.get_number()
                            self.score_points(point, player)
                            box.unoccupy()

                    # Tiles on scorer2 are removed from the window.
                    for tile in self._tiles_on_scorer2:
                        tile.move_tile(ORIGINAL_TILE_POSITION)
                        self._discarded_tiles.append(tile)
                    self._tiles_on_scorer2.clear()

        # The number of clickable buttons is calculated.
        unclickable_buttons = 0
        for button in self._scorer_buttons:
            if not button.is_clickable():
                unclickable_buttons += 1

        # If there are no clickable buttons, a new round is started.
        if unclickable_buttons == 2:
            self.start_new_round()

    def unoccupy_ladder(self):
        """ Unoccupies ladder boxes which are empty after a round is over. """

        # Loops thorugh the first ladder and emptys it.
        for player in range(PLAYER_NUM):
            if player == 0:
                for counter, list in enumerate(self._tiles_on_ladder1):
                    if len(list) == 0:
                        for box in self._allladders[player][counter]:
                            box.unoccupy()

            # Loops thorugh the second ladder and emptys it.
            else:
                for counter, list in enumerate(self._tiles_on_ladder2):
                    if len(list) == 0:
                        for box in self._allladders[player][counter]:
                            box.unoccupy()

    def start_new_round(self):
        """ Starts a new round by filling the factories and assigning the
        starter player. """

        # Unoccupies all ladders.
        self.unoccupy_ladder()

        # Deactivates all the players.
        self.deactivate_players()

        # Actovates a player that has the starter button.
        self._players[self._next_round_starter].activate()

        # Changes the booleans to false.
        self._round_over = False
        self._clicked_first_street = False

        # Checks if the game is over.
        self.check_game()

        # Checks the number of tiles in the bag.
        self.check_bag()

        # If the game is not over, the factories are filled to start a round.
        if not self._game_over:
            self.fill_factory()

    def check_bag(self):
        """ Checks how many tiles are left in the bag. """

        # If the bag is empty, all discarded tiles are put inside the bag.
        if len(self._alltiles) == 0:
            for tile in self._discarded_tiles:
                self._alltiles.append(tile)
                self._discarded_tiles.remove(tile)

    def arrange(self, color, button_row, tile_list,  boxes):
        """ Arranges the tiles on ladder. """

        # Gets the active player.
        active_player = self.get_active_player()

        # Checks if the first street is clicked.
        if self._street_clicked and not self._clicked_first_street:
            self._clicked_first_street = True
            self.put_starter_tile()

        # Gets if the chosen ladder and the clciked tiles match.
        if self.ladder_color_matched(button_row, color):

            # Compares the available boxes and the clciked tiles.
            if len(tile_list) <= len(boxes):
                for counter, tile in enumerate(tile_list):
                    tile.move_tile(boxes[counter].get_center())
                    boxes[counter].occupy()

                # Arranges the tiles and changes their location.
                self.change_tile_location(tile_list, active_player, button_row)
                self.change_location(tile_list, active_player, button_row)
                self._arranged_on_ladder = True
                self.make_changes()

            # Compares the available boxes and the clciked tiles.
            elif len(tile_list) > len(boxes):
                difference = len(tile_list) - len(boxes)
                scorer_tiles = tile_list[:difference]
                tile_on_ladder = tile_list[difference:]

                # Occupies the availbale boxes.
                for counter, box in enumerate(boxes):
                    tile_on_ladder[counter].move_tile(box.get_center())
                    box.occupy()

                # Arranges the tiles and changes their location.
                self.deduct_point(scorer_tiles)
                self.change_tile_location(tile_on_ladder, active_player, \
                button_row)
                self.change_location(tile_list, active_player, button_row)
                self._arranged_on_ladder = True
                self.check_scorer()
                self.make_changes()

            # Compares the available boxes and the clciked tiles.
            elif len(boxes) == 0:

                # Arranges the tiles and changes their location.
                self.deduct_point(tile_list)
                self.change_tile_location(tile_list, active_player, button_row)
                self.change_location(tile_list, active_player, button_row)
                self._arranged_on_ladder = True
                self.make_changes()

    def make_changes(self):
        """ Makes changes after tiles are arranged on a ladder. """

        # After arrangements are done:
        if self._arranged_on_ladder:

            # Changes the player.
            self.change_player()

            # unclicks tiles, buttons, and streets.
            self.unclick_button()
            self.unclick_tile()
            self.decrease_street_number()
            self.unclick_street()

            # Checks of a round is over.
            self.check_round()
            self.unclick_scorer_button()

            # Changes the arranges boolean to false.
            self._arranged_on_ladder = False

    def put_starter_tile(self):
        """ Puts the StarterTile on the a player's side. """

        # Gets the active player.
        player = self.get_active_player()

        # Assigns the starter of the next round.
        self._next_round_starter = player

        # Moves the starter tile to the player that clicked the first street.
        if player == 0:
            self._starter_tile.move(PLAYER1_STARTER_POS)
            self._pointer1[1][0].add_point(-1)
        else:
            self._starter_tile.move(PLAYER2_STARTER_POS)
            self._pointer2[1][0].add_point(-1)

    def change_location(self, tile_list, player, row):
        """ Changes the location of a tile from street to ladder. """

        # Finds the ladder which was recently clicked.
        if player == 0:
            tile_on_ladder = self._tiles_on_ladder1
        else:
            tile_on_ladder = self._tiles_on_ladder2

        # Finds the clicked row of a ladder.
        ladder_row_list = tile_on_ladder[row]

        # Removes all the tiles from the clicked street.
        for box in self._street:
            if box.is_clicked():
                id = box.get_id()
                self._tiles_on_street[id].clear()

    def arrange_on_ladder(self):
        """ Arranges the tiles on ladder. """

        # Gets the active player.
        active_player = self.get_active_player()

        # Initialize.
        tile_list = []
        unclicked_tiles = []
        button_row = 0
        boxes = []
        color = None

        # Checks if a tile or a street is clicked.
        if self._tile_clicked and self._button_clicked:

            # Gets the clicked tiles list.
            if self._street_clicked:
                tile_list = self.get_clicked_tile()
            else:
                tile_list, unclicked_tiles = self.get_clicked_tile()

            # Gets the color of the clicked tiles.
            color = tile_list[0].get_color()

            # Gets the clicked button.
            button_row = self.get_clicked_button()

            # Gets the wall that belongs to the active player.
            wall_row = self._allwalls[active_player][button_row]

            # Loops through boxes of the wall.
            for box in wall_row:
                box_color = box.get_color()

                # Compares box color to tile color.
                if box_color == color:

                    # Gets the availability of a box.
                    if box.get_availability():

                        # Gets the ladder row clicked.
                        ladder_row = self._allladders[active_player][button_row]

                        # Checks if the tile color and ladder color match.
                        if self.ladder_color_matched(button_row, color):

                            # Arranges the unclicked tiles on the street.
                            self.arrange_on_street(unclicked_tiles)

                            # Gets the centers of availbale boxes.
                            for box in ladder_row:
                                if box.get_availability():
                                    center = box.get_center()
                                    boxes.append(box)

                            # Arranges the tiles on available boxes.
                            self.arrange(color, button_row, tile_list, boxes)

    def ladder_color_matched(self, ladder_row, color):
        """ Checks if the color of clicked tiles match the color of the clicked
         ladder. """

        # Gets active player.
        active_player = self.get_active_player()

        # Loops through ladder boxes.
        for box in self._allladders[active_player][ladder_row]:

            # Check the availability of a box.
            if not box.get_availability():

                # Compares the color of the ladder with that of the tile.
                if active_player == 0:
                    for tile in self._tiles_on_ladder1[ladder_row]:
                        tile_color = tile.get_color()

                        # Returns a boolean accordingly.
                        if tile_color == color:
                            return True
                        else:
                            return False

                # Checks the ladder of the second player.
                else:

                    # Compares the color of the ladder with that of the tile.
                    for tile in self._tiles_on_ladder2[ladder_row]:
                        tile_color = tile.get_color()

                        # Returns a boolean accordingly.
                        if tile_color == color:
                            return True
                        else:
                            return False

            # If the clicked row is empty, it returns true.
            else:
                return True

    def deduct_point(self, tile_list):
        """ Moves the extra tiles to the scorer. """

        # Gets the active player.
        player = self.get_active_player()

        # Initializes lists.
        empty_boxes = []
        discarded_tiles = []
        tiles_on_penality = []

        # Gets the available boxes on the scorer.
        for box in self._allscorer[player]:
            if box.get_availability():
                empty_boxes.append(box)

        # Compares the available boxes with the clicked tiles.
        if len(empty_boxes) >= len(tile_list):
            for counter, tile in enumerate(tile_list):

                # Moves the tiles to the available boxes.
                tile.move_tile(empty_boxes[counter].get_center())
                empty_boxes[counter].occupy()

                # Appends the tiles to the scorers.
                if player == 0:
                    self._tiles_on_scorer1.append(tile)
                else:
                    self._tiles_on_scorer2.append(tile)

            # Removes the tiles from the clicked factory.
            for tile in tile_list:
                for factory in self._tiles_on_factory:
                    if tile in factory:
                        factory.remove(tile)

        # If the clicked tiles are grater than the available boxes:
        else:

            # Finds the difference.
            difference = len(tile_list) - len(empty_boxes)

            # Creates two new lists.
            tiles_on_penality = tile_list[:difference]
            discarded_tiles = tile_list[difference:]

            # If there are available boxes, it arranges the tiles.
            if len(empty_boxes) > 0:
                for counter, tile in enumerate(tiles_on_penality):
                    tile.move_tile(empty_boxes[counter].get_center())
                    empty_boxes[counter].occupy()

            # It appends the tiles to the scorer.
            for tile in tiles_on_penality:
                if player == 0:
                    self._tiles_on_scorer1.append(tile)
                else:
                    self._tiles_on_scorer2.append(tile)

            # Discards the tiles that are not arranged on the scorer.
            for tile in discarded_tiles:
                tile.move_tile(ORIGINAL_TILE_POSITION)
                self._discarded_tiles.append(tile)

            # Removes the discarded tiles from the selected factory.
            for tile in discarded_tiles:
                for factory in self._tiles_on_factory:
                    if tile in factory:
                        factory.remove(tile)
                    else:
                        for box in self._tiles_on_street:
                            if tile in box:
                                box.remove(tile)

    def change_tile_location(self, tile_list, player, row):
        """ Changes the location of the tiles from factory to ladder. """

        # Loops through the tile list:
        for tile in tile_list:

            # Appends the tiles to the ladder.
            if player == 0:
                self._tiles_on_ladder1[row].append(tile)
            else:
                self._tiles_on_ladder2[row].append(tile)

            # Removes the tiles from the factory.
            for factory in self._tiles_on_factory:
                if tile in factory:
                    factory.remove(tile)

    def tile_is_clicked(self):
        """ Returns the boolean that ckecks is a tile is clicked. """

        return self._tile_clicked

    def unclick_button(self):
        """Changes the boolean to False.  """

        self._button_clicked = False

    def unclick_scorer_button(self):
        """ Changes self._scorer_button_clicked to False. """

        self._scorer_button_clicked = False

    def unclick_street(self):
        """ Changes self._street_clicked to False and unclicks all streets. """

        self._street_clicked = False

        # Unclicks all the street boxes.
        for box in self._street:
            if box.is_clicked():
                box.unclick()

    def decrease_street_number(self):
        """ Decreases the numbers written on a StreetBox. """

        # Changes the number of a clicked street.
        for box in self._street:
            if box.is_clicked():
                box.decrease_number()

    def round_is_over(self):
        """ Returns self._round_over. """

        return self._round_over

    def game_is_over(self):
        """ Returns self._game_over. """

        return self._game_over

    def unclick_tile(self):
        """ Unclicks a Tile. """

        # Unclicks all the clicked tiles.
        for factory in self._tiles_on_factory:
            for tile in factory:
                tile.unclick()

        self._tile_clicked = False

    def get_clicked_tile(self):
        """ Creates a list of tiles that need to be moved to a ladder. """

        # Initializes lists.
        tile_list = []
        unclicked_tiles = []
        chosen_factory = []

        # Checks if a street clicked.
        if self._street_clicked:

            # Checks all the boxes of a street.
            for box in self._street:
                if box.is_clicked():
                    id = box.get_id()

                    # Gets all the tiles on the clicked street.
                    tile_list = self._tiles_on_street[id]
                    return tile_list

        # If a street is not cliked:
        else:

            # Loops through the tiles on factory to get the clicked tiles.
            for list in self._tiles_on_factory:
                for tile in list:
                    if tile.is_clicked():
                        chosen_factory = list

                        # Gets the colcor of the clicked tile.
                        chosen_color = tile.get_color()

                # Checks the which factory is chosen.
                if list == chosen_factory:
                    for tile in list:

                        # Compares the color of each tile with the chosen color.
                        color = tile.get_color()

                        # Appends tiles to list if color matched.
                        if color == chosen_color:
                            tile_list.append(tile)

                        # Appends tile in unclicked if no color matched.
                        else:
                            unclicked_tiles.append(tile)

            # Returns the clicked tiles and unclicked tiles.
            return tile_list, unclicked_tiles

    def arrange_on_street(self, tile_list):
        """ Arranges the unclicked tiles on the street. """

        # Loops through the unclicked tiles.
        for tile in tile_list:

            # Gets the color of the tiles.
            tile_color = tile.get_color()

            # Gets the color of each street box.
            for box in self._street:
                box_color = box.get_color()

                # Moves the colors to the box if the colors match.
                if box_color == tile_color:
                    id = box.get_id()
                    self._tiles_on_street[id].append(tile)
                    tile.move_tile(box.get_center())

                    # Increases the number written on the street.
                    box.increase_number()

            # Removes the tiles from the chosen factory.
            for list in self._tiles_on_factory:
                for enrty in list:
                    if enrty == tile:
                        list.remove(tile)

    def street_clicked(self):
        """ Clicks both a street and tile when a street is clicked. """

        self._street_clicked = True
        self._tile_clicked = True

        # Arranges the clicked tiles from a street.
        self.arrange_on_ladder()

    def tile_on_factory(self, tile):
        """ Checks if a tile is on a factory. """

        # Checks if a given tile is on a factory.
        for factory in self._tiles_on_factory:
            if tile in factory:
                return True

    def tile_on_street(self, tile):
        """ Returns True of a tile is on street. """

        # Checks if a given tile is on a street.
        for item in self._tiles_on_street:
            if item == tile:
                return True
            else:
                return False

    def get_active_player(self):
        """ Returns the id of the active player. """

        # Returns the id of the active player.
        for player in self._players:
            if player.is_active():
                return player.get_id()

    def change_player(self):
        """ The Game changes turns for the players. """

        # Gets the active player id.
        active_player_id = self.get_active_player()

        # Changes the id by adding 1 and moding by 2.
        active_player_id = (active_player_id + 1) % PLAYER_NUM

        # Deactivates all the players.
        self.deactivate_players()

        # Activates a new player.
        self._players[active_player_id].activate()

    def is_correct_player(self, button):
        """ Checks if a button belongs to the correct player. """

        # Gets the active player.
        correct_player_id = self.get_active_player()

        # If s given id matches the id of the correct player, returns True.
        if button.get_player() == correct_player_id:
            return True
        else:
            return False

    def deactivate_players(self):
        """ Deactivates all the players in the Game. """

        # Deactivates all the players.
        for player in self._players:
            player.deactivate()

    def click_tile(self):
        """ Clicks a Tile. """

        self._tile_clicked = True

    def click_button(self):
        """ Clicks a Button. """

        self._button_clicked = True

    def click_scorer_button(self):
        """ Clicks a scorer button. """

        self._scorer_button_clicked = True

    def get_clicked_button(self):
        """ Returns the row of a clicked button. """

        # Initializes a list.
        row = []

        # Gets active player.
        id = self.get_active_player()

        # Retuens the row of a clicked button.
        for button in self._allbuttons[id]:
            if button.is_clicked():
                row = button.get_row()
                return row
        return None


class StartButton(EventHandler):
    """ Class for the start button."""

    def __init__(self, window, center, text_color, text, width, height, game):
        """ The constractor method for StartButton. """

        # Assigns attributes.
        self._window = window
        self._center = center
        self._text_color = text_color
        self._text = text
        self._game = game
        self._width = width
        self._height = height

        # Creates text and body of the start button,
        self._size = 30
        self._body = Image(self._window, 'fact.png', self._width, \
        self._height, self._center)
        self._text = Text(self._window, self._text, self._size, \
        ((self._center[0] + 300), (self._center[1])))
        self._body.add_handler(self)
        self._text.add_handler(self)

    def draw(self):
        """ Draws the StartButton. """

        # Darws the start button.
        self._body.set_depth(1)
        self._text.set_depth(-24)
        self._window.add(self._body)
        self._window.add(self._text)

    def handle_mouse_press(self, event):
        """ When the StartButton is pressed, the game starts, and it desappears."""

        # Moves the start button from window and starts the game when clicked.
        self._game.start_game()
        self._body.move(1000, 1000)
        self._text.move(1000, 1000)


class FactoryBoxes():
    """ Class for the factories. """

    def __init__(self, window, factory, xpos, ypos, size, color, id):
        """ The constractor method for class Factory. """

        # Assigns attributes.
        self._window = window
        self._in_factory = factory
        self._id = id
        self._xpos = xpos
        self._ypos = ypos
        self._size = size
        self._color = color

        # Creates a square object.
        self._body = Square(self._window, self._size, (self._xpos, self._ypos))
        self._body.set_border_width(3)
        self._body.set_depth(-1)


    def draw(self):
        """ Draws a factory. """

        # Darws the boxes.
        self._body.set_fill_color(self._color)
        self._window.add(self._body)

    def get_center(self):
        """ Returns the center of FactoryBoxes. """

        return (self._xpos, self._ypos)


class StreetBoxes(EventHandler):
    """ Class for the boxes that make up the street. """

    def __init__(self, window, xpos, ypos, size, color, number, id, game):
        """ Constructor method for StreetBoxes. """

        # Assigns attributes.
        self._window = window
        self._xpos = xpos
        self._ypos = ypos
        self._size = size
        self._color = color
        self._number = number
        self._id = id
        self._game = game
        self._is_clicked = False

        # Creates square objects.
        self._body = Square(self._window, self._size, (self._xpos, self._ypos))
        self._body.set_border_width(3)
        self._body.set_depth(-9)
        self._body.add_handler(self)

        # Creates text objects.
        self._text = Text(self._window, self._number, int(0.6 * self._size), \
        (self._xpos, self._ypos))
        self._text.set_depth(-10)
        self._text.add_handler(self)

    def draw(self):
        """ Draws the boxes that make up the street. """

        # Darws the boxes.
        self._body.set_fill_color(self._color)
        self._window.add(self._body)
        self._window.add(self._text)

    def handle_mouse_press(self, event):
        """ When pressed, the border tickens. """

        # Clicks a street in the game when clicked.
        if self._number != STREET_ORIGINAL_NUMBER:
            self._game.unclick_tile()
            self._game.unclick_street()
            self._game.street_clicked()
            self._is_clicked = True
            self._body.set_border_width(8)
            self.draw()

    def is_clicked(self):
        """ Returns True if a StreetBox is clicked. """

        return self._is_clicked

    def get_color(self):
        """ Returns the color of a StreetBox. """

        return self._color

    def get_center(self):
        """ Return the center of a StreetBox. """

        return (self._xpos, self._ypos)

    def get_id(self):
        """ Returns the id of a StreetBox. """

        return self._id

    def unclick(self):
        """ Changes the clicked status of a StreetBox to False. """

        # Changes the boarder back to 3.
        self._is_clicked = False
        self._body.set_border_width(3)
        self.draw()

    def increase_number(self):
        """ Increments the number written on a StreetBox by 1. """

        # Increases the number written on the box by 1.
        number = int(self._number)
        new_number = number + 1
        self._number = str(new_number)
        self.change_text()

    def decrease_number(self):
        """ CHanged the text of a StreetBoxe to 0. """

        # Changes the number written on the box to 0.
        self._number = '0'
        self.change_text()

    def change_text(self):
        """ Changes the text written on a StreetBox. """

        # Changes the number written on a box.
        self._text.set_text(self._number)
        self.draw()


class ScorerBoxes():
    """ Class for the boxes that make up the score diduction. """

    def __init__(self, window, xpos, ypos, size, color, number, player):
        """ The constractor method. """

        # Assigns attributes.
        self._window = window
        self._xpos = xpos
        self._ypos = ypos
        self._size = size
        self._color = color
        self._number = number
        self._player = player
        self._available = True

        # Creates square objects.
        self._body = Square(self._window, self._size, (self._xpos, self._ypos))
        self._body.set_border_width(3)
        self._body.set_depth(-1)

        # Creates text objects.
        self._text = Text(self._window, self._number, int(0.6 * self._size), \
        (self._xpos, self._ypos))
        self._text.set_depth(-3)

    def draw(self):
        """ Draws the ScorerBoxes. """

        # Draws the boxes.
        self._body.set_fill_color(self._color)
        self._window.add(self._body)
        self._window.add(self._text)

    def get_center(self):
        """ Returns the center of a ScorerBoxe. """

        return (self._xpos, self._ypos)

    def occupy(self):
        """ Chnages the availability status of a ScorerBox to False. """

        self._available = False

    def unoccupy(self):
        """ Changes the availability status of a ScorerBox to True. """

        self._available = True

    def get_availability(self):
        """ Returns the availability of ScorerBox. """

        return self._available

    def get_number(self):
        """ Returns the number written on a ScorerBox. """

        return int(self._number)


class Pointer():
    """ Class for pointers. """

    def __init__(self, window, center, text, size):
        """ The constractor method. """

        # Assigns attributes.
        self._window = window
        self._center = center
        self._text = text
        self._size = size

        # Creates a text object.
        self._body = Text(self._window, self._text, self._size, self._center)

    def draw(self):
        """ Draws the pointers. """

        # Draws the pointer.
        self._body.set_depth(-1)
        self._body.set_color('white')
        self._window.add(self._body)

    def add_point(self, point):
        """ Adds a point to the player's score. """

        # Changes the number of the score.
        old_point = int(self._text)
        new_point = old_point + point
        self._text = str(new_point)

        # Redraws the text.
        self._body.set_text(self._text)
        self.draw()

    def get_score(self):
        """ Returns the text of a player's pointer. """

        return int(self._text)


class WallBoxes():
    """ Class for the boxes that make up the wall. """

    def __init__(self, window, xpos, ypos, size, color, row, column, player):
        """ The constractor method. """

        # Assigns attributes.
        self._window = window
        self._xpos = xpos
        self._ypos = ypos
        self._size = size
        self._color = color
        self._row = row
        self._column = column
        self._in_player = player
        self._available = True

        # Creates square objects.
        self._body = Square(self._window, self._size, (self._xpos, self._ypos))
        self._body.set_border_width(3)
        self._text = Text(self._window, '', 40, (self._xpos, self._ypos))

    def draw(self):
        """ Draws each box of a wall. """

        # Draws the boxes.
        self._body.set_fill_color(self._color)
        self._body.set_depth(-1)
        self._text.set_depth(-2)
        self._window.add(self._body)
        self._window.add(self._text)

    def get_color(self):
        """ Returns the color of a WallBox. """

        return self._color

    def get_availability(self):
        """ Returns the availability of a WallBox. """

        return self._available

    def occupy(self):
        """ Changes the availability status of a WallBox to False. """

        # Puts a tick mark on the box when occupied and thicken the boarder.
        self._available = False
        self._text.set_text('✔')
        self._window.add(self._text)
        self._body.set_border_width(8)
        self.draw()

    def get_row(self):
        """ Returns the row of a WallBoxe. """

        return self._row

    def get_col(self):
        """ Returns the column of a WallBox. """

        return self._column


class LadderBoxes():
    """ Class for the ladder. """

    def __init__(self, window, xpos, ypos, size, color, row, col, player):
        """ The constractor method. """

        # Assigns attributes.
        self._window = window
        self._xpos = xpos
        self._ypos = ypos
        self._size = size
        self._color = color
        self._row = row
        self._column = col
        self._in_player = player
        self._available = True

        # Creates square objects.
        self._body = Square(self._window, self._size, (self._xpos, self._ypos))
        self._body.set_border_width(3)

    def draw(self):
        """ Draws the boxes that make up the ladder. """

        # Draws the boxes.
        self._body.set_fill_color(self._color)
        self._body.set_depth(-1)
        self._window.add(self._body)

    def get_availability(self):
        """ Returns the availability status of a LadderBox. """

        return self._available

    def occupy(self):
        """ Changes the availability of a LadderBox to False. """

        self._available = False

    def unoccupy(self):
        """ Changes the availability of a LadderBox to True. """

        self._available = True

    def get_center(self):
        """ Returns the center of a LadderBox. """

        return (self._xpos, self._ypos)


class Button(EventHandler):
    """ Class for the buttons. """

    def __init__(self, window, color, radius, xpos, ypos, row, player, game):
        """ The constractor mothod. """

        # Assigns attributes.
        self._window = window
        self._color = color
        self._radius = radius
        self._xpos = xpos
        self._ypos = ypos
        self._row = row
        self._player = player
        self._game = game
        self._clicked = False
        self._is_clickable = False

        # Creates a circle object.
        self._body = Circle(self._window, self._radius, \
        (self._xpos, self._ypos))
        self._body.set_border_width(3)
        self._body.add_handler(self)

    def draw(self):
        """ Draws the buttons. """

        # Draws the buttons.
        self._body.set_fill_color(self._color)
        self._body.set_depth(-1)
        self._window.add(self._body)

    def handle_mouse_press(self):
        """ The boarder thickens when buttons clicked. """

        # Checks if round is over and a tile is clicked.
        clicked_tiles = self._game.tile_is_clicked()
        round_over = self._game.round_is_over()

        # Arranges tiles on ladder if a tile is clicked.
        if clicked_tiles:
            if self._game.is_correct_player(self):
                self._body.set_border_width(8)
                self.draw()
                self._clicked = True
                self._game.click_button()
                self._game.arrange_on_ladder()
                self.unclick()

        # Arranges tiles on wall if a round is over.
        elif round_over:
            if self._is_clickable:
                self._body.set_border_width(8)
                self.draw()
                self._clicked = True
                self._game.click_button()
                self._game.arrange_on_wall()
                self.unclick()


    def is_clicked(self):
        """ Returns the clicked status of a Button. """

        return self._clicked

    def get_row(self):
        """ Returns the row of a Button. """

        return self._row

    def get_player(self):
        """ Returns which player a Button belongs to. """

        return self._player

    def make_clickable(self):
        """ Changes the clickability of a button to True. """

        # Changes the color to dark green.
        self._is_clickable = True
        self._color = 'darkgreen'
        self.draw()

    def make_unclickable(self):
        """ Changes the clickability of a button to False. """

        # Changes the color to a light green.
        self._is_clickable = False
        self._color = 'lightgreen'
        self.draw()

    def unclick(self):
        """ Unclicks a Button. """

        # Resets the boarder back to 3.
        self._clicked = False
        self._body.set_border_width(3)
        self.draw()

    def is_clickable(self):
        """ Returns the clickability of a Button. """

        return self._is_clickable


class ScorerButton(EventHandler):
    """ Class for the scorer buttons. """

    def __init__(self, window, color, radius, xpos, ypos, player, game):
        """ The constractor method. """

        # Assigns attributes.
        self._window = window
        self._color = color
        self._radius = radius
        self._xpos = xpos
        self._ypos = ypos
        self._player = player
        self._game = game
        self._clicked = False
        self._is_clickable = False
        self._can_be_clicked = False

        # Creates the circle objects.
        self._body = Circle(self._window, self._radius, \
        (self._xpos, self._ypos))
        self._body.set_border_width(3)
        self._body.add_handler(self)

    def draw(self):
        """ Draws the scorer buttons. """

        # Draws the buttons.
        self._body.set_fill_color(self._color)
        self._body.set_depth(-1)
        self._window.add(self._body)

    def handle_mouse_press(self, event):
        """ The boarder thickens when a button is clicked. """

        # Checks if a tile or a street is clicked and if a round is over.
        clicked_tiles = self._game.tile_is_clicked()
        round_over = self._game.round_is_over()
        street_clicked = self._game.street_is_clicked()

        # Arranges tile on scorer if a tile is clicked.
        if clicked_tiles:
            if self._game.is_correct_player(self):
                self._body.set_border_width(8)
                self.draw()
                self._clicked = True
                self._game.click_scorer_button()
                self._game.arrange_on_scorer()
                self.make_clickable()
                self.unclick()

        # Arranges tiles on scorer if a street is clicked.
        if street_clicked:
            if self._game.is_correct_player(self):
                self._body.set_border_width(8)
                self.draw()
                self._clicked = True
                self._game.click_scorer_button()
                self._game.arrange_on_scorer()
                self.make_clickable()
                self.unclick()

        # Finalizes grades if a round is over.
        elif round_over:
            if self._is_clickable:
                if self._can_be_clicked:
                    self._body.set_border_width(8)
                    self.draw()
                    self._clicked = True
                    self._game.click_scorer_button()
                    self._game.finalize_score()
                    self.unclick()

    def unclick(self):
        """ Unclicks a Button. """

        # Chnages the boarder back to 3.
        self._clicked = False
        self._body.set_border_width(3)
        self.draw()

    def make_clickable(self):
        """ Changes the clickability of a ScorerButton to True. """

        # Changes the color to dark green.
        self._is_clickable = True
        self._color = 'darkgreen'
        self.draw()

    def make_unclickable(self):
        """ Changes the clickability of a ScorerButton to False. """

        # Changes the color to lightgreen.
        self._is_clickable = False
        self._color = 'lightgreen'
        self.draw()

    def get_player(self):
        """ Returns which player the button belongs to. """

        return self._player

    def is_clickable(self):
        """ Returns the clickability of a Button. """

        return self._is_clickable

    def enable_clicking(self):
        """ Changes self._can_be_clicked to True. """

        self._can_be_clicked = True

    def disable_clicking(self):
        """ Changes self._can_be_clicked to False. """

        self._can_be_clicked = False

    def is_clicked(self):
        """ Returns self._is_clicked. """

        return self._clicked


class StarterTile():
    """ Class for the StarterTile. """

    def __init__(self, window, color, x_pos, y_pos, text, radius):
        """ The constractor method. """

        # Assigns attributes.
        self._window = window
        self._color = color
        self._radius = radius
        self._xpos = x_pos
        self._ypos = y_pos
        self._letter = text
        self._text_size = 30

        # Creates the circle object.
        self._body = Circle(self._window, self._radius, \
        (self._xpos, self._ypos))
        self._text = Text(self._window, self._letter, self._text_size, \
        (self._xpos, self._ypos))

    def draw(self):
        """ Draws the StarterTile. """

        # Draws the starter tile.
        self._body.set_fill_color(self._color)
        self._body.set_depth(-13)
        self._text.set_depth(-14)
        self._window.add(self._body)
        self._window.add(self._text)

    def move(self, center):
        """ Moves the StarterTile to a center. """

        # Moves the tile to a given center.
        self._body.move_to(center)
        self._text.move_to(center)

    def get_center(self):
        """ Returns the center of the StarterTile. """

        return (self._xpos, self._ypos)


class Tiles(EventHandler):
    """ Class for all the tiles. """

    def __init__(self, window, color, size, xpos, ypos, game):
        """ The constractor method. """

        # Assigns attributes.
        self._window = window
        self._color = color
        self._size = size
        self._xpos = xpos
        self._ypos = ypos
        self._game = game
        self._clicked = False

        # Creates the tile objects.
        self._body = Square(self._window, self._size, (self._xpos, self._ypos))
        self._body.set_border_width(3)
        self._body.add_handler(self)

    def draw(self):
        """ Draws the tiles. """

        # Draws the tiles.
        self._body.set_fill_color(self._color)
        self._body.set_depth(-2)
        self._window.add(self._body)

    def handle_mouse_press(self):
        """ When Tile is pressed it changes its boarder width. """

        # Clicks itself if it is on a factory.
        if self._game.tile_on_factory(self):
            self._game.unclick_street()
            self._game.unclick_tile()
            self._body.set_border_width(8)
            self.draw()
            self._game.click_tile()
            self._clicked = True

    def is_clicked(self):
        """ Returns the clicked status of a Tile. """

        return self._clicked

    def move_tile(self, center):
        """ Moves a Tile to the given center. """

        # Moves a tile to a given center.
        self._body.set_border_width(3)
        self._body.move_to(center)

    def get_color(self):
        """ Returns the color of a Tile. """

        return self._color

    def get_center(self):
        """ Returns the center of a Tile. """

        return (self._xpos, self._ypos)

    def unclick(self):
        """ Changed the clicked status of a Tile to False. """

        # It sets its boarder back to 3.
        self._body.set_border_width(3)
        self.draw()
        self._clicked = False


class Player():
    """ Class for players. """

    def __init__(self, id):
        """ Constructor method. """

        # Assigns attributes.
        self._id = id
        self._active = False

        # Starts the game by activating player 1.
        if self._id == 0:
            self._active = True

    def get_id(self):
        """ Returns the id of a Player. """

        return self._id

    def is_active(self):
        """ Returns the activity status of a PLayer. """

        return self._active

    def deactivate(self):
        """ Sets the activity status of a Player to False. """

        self._active = False

    def activate(self):
        """ Sets the activity status of a Player to True. """

        self._active = True


def main(win):
    """ The main function. """

    win.set_width(1400)
    win.set_height(780)
    Game(win)


if __name__ == "__main__":
    StartGraphicsSystem(main)
