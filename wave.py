from wfc import State, Rule, Wave


# class shall be used to define rules that must be followed
# in the Wave Function Collapse algorithm for level generation
class WaveFunctionCollapse():

    def __init__(self):

        def repeat_state(state, count):
            return [state] * count

        floor_repeat_count = 10

        self.floor = State(
            "floor",
            Rule(
                lambda x, y: {
                    (x, y - 1): floor_repeat_count * ["floor"] + 1 * ["top_wall"],  # Above
                    (x - 1, y): floor_repeat_count * ["floor"] + 1 * ["left_wall"],  # Left
                    (x + 1, y): floor_repeat_count * ["floor"] + 1 * ["right_wall"],  # Right
                    (x, y + 1): floor_repeat_count * ["floor"] + 1 * ["bottom_wall"]  # Below
                }
            )
        )

        # 4 wall sides
        self.top_wall = State(
            "top_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["floor"],  # Above
                    (x - 1, y): ["top_left_wall", "top_wall"] + floor_repeat_count * ["floor"],  # Left
                    (x + 1, y): ["top_right_wall", "top_wall"] + floor_repeat_count * ["floor"],  # Right
                    (x, y + 1): ["floor"]  # Below
                }
            )
        )
        self.left_wall = State(
            "left_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["top_left_wall", "left_wall"] + floor_repeat_count * ["floor"],  # Above
                    (x - 1, y): ["floor"],  # Left
                    (x + 1, y): ["floor"],  # Right
                    (x, y + 1): ["bottom_left_wall", "left_wall"] + floor_repeat_count * ["floor"]  # Below
                }
            )
        )
        self.right_wall = State(
            "right_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["top_right_wall", "right_wall"] + floor_repeat_count * ["floor"],  # Above
                    (x - 1, y): ["floor"],  # Left
                    (x + 1, y): ["floor"],  # Right
                    (x, y + 1): ["bottom_right_wall", "right_wall"] + floor_repeat_count * ["floor"] # Below
                }
            )
        )
        self.bottom_wall = State(
            "bottom_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["floor"],  # Above
                    (x - 1, y): ["bottom_left_wall", "bottom_wall"] + floor_repeat_count * ["floor"],  # Left
                    (x + 1, y): ["bottom_right_wall", "bottom_wall"] + floor_repeat_count * ["floor"],  # Right
                    (x, y + 1): ["floor"]  # Below
                }
            )
        )


        # four corners
        self.top_left = State(
            "top_left_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["air", "floor"],  # Above
                    (x - 1, y): ["air", "floor"],  # Left
                    (x + 1, y): ["top_wall"],  # Right
                    (x, y + 1): ["left_wall"]  # Below
                }
            )
        )
        self.top_right = State(
            "top_right_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["air", "floor"],  # Above
                    (x - 1, y): ["top_wall"],  # Left
                    (x + 1, y): ["air", "floor"],  # Right
                    (x, y + 1): ["right_wall"]  # Below
                }
            )
        )
        self.bottom_left = State(
            "bottom_left_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["left_wall"],  # Above
                    (x - 1, y): ["air", "floor"],  # Left
                    (x + 1, y): ["bottom_wall"],  # Right
                    (x, y + 1): ["air", "floor"]  # Below
                }
            )
        )
        self.bottom_right = State(
            "bottom_right_wall",
            Rule(
                lambda x, y: {
                    (x, y - 1): ["right_wall"],  # Above
                    (x - 1, y): ["bottom_wall"],  # Left
                    (x + 1, y): ["air", "floor"],  # Right
                    (x, y + 1): ["air", "floor"]  # Below
                }
            )
        )








    def collapse(self, x, y):
        # Define the dimensions of your level (e.g., 10x40)
        level_dimensions = (x, y)

        # Create the wave with your states
        level_wave = Wave(level_dimensions, [self.floor, self.top_left, self.top_right, self.bottom_left, self.bottom_right,
                                             self.top_wall, self.right_wall, self.bottom_wall, self.left_wall,
                                             self.floor, self.floor, self.floor, self.floor, self.floor, self.floor,
                                             self.floor, self.floor, self.floor, self.floor, self.floor, self.floor,
                                             ])

        # Collapse the wave to generate the level
        generated_level = level_wave.collapse()

        return generated_level
