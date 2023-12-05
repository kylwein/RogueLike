from wfc import State, Rule, Wave


# class shall be used to define rules that must be followed
# in the Wave Function Collapse algorithm for level generation
class WaveFunctionCollapse():

    def __init__(self):
        self.wall = State(
            "wall",
            Rule(
                lambda x, y: {
                    (x, y + 1): ["floor"],  # Wall can have floor below
                    (x, y - 1): ["wall", "floor"]  # Wall can have wall or floor above
                }
            )
        )

        self.floor = State(
            "floor",
            Rule(
                lambda x, y: {
                    (x, y + 1): ["floor", "wall"],  # Floor can have floor or wall below
                    (x, y - 1): ["floor"]  # Floor can have floor above
                }
            )
        )

    def collapse(self, x, y):
        # Define the dimensions of your level (e.g., 10x40)
        level_dimensions = (x, y)

        # Create the wave with your states
        level_wave = Wave(level_dimensions, [self.wall, self.floor])

        # Collapse the wave to generate the level
        generated_level = level_wave.collapse()

        return generated_level
