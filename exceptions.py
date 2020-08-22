class UnableToSolveError(Exception):
    """
    Raised when a solving strategy does not result in a change to any cells.
    """
    pass

class NumberNotInPossibleValuesError(KeyError):
    """
    Raised when the program tries to remove a possible value from a cell that isn't in that cell's possible values.
    """
    pass
