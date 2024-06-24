from enum import Enum


class Direction(Enum):
    """
    An enumeration class to represent the directions.

    Attributes:
        - UP: The up direction.
        - LEFT: The left direction.
        - DOWN: The down direction.
        - RIGHT: The right direction.
    """
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"


if __name__ == "__main__":
    print(Direction.UP)  # Output: "Direction.UP"
    print(Direction("left"))  # Output: "Direction.LEFT"
    print(Direction.DOWN.name)  # Output: "DOWN"
    print(Direction.RIGHT.value)  # Output: "right"