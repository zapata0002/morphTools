"""
Sides for nodes in maya
"""

center = 'c'
left = 'l'
right = 'r'


def get_opposite_side(side):
    """
    Get the opposite side
    :return: opposite side
    """
    if side == left:
        return right
    elif side == right:
        return left
    else:
        return center
