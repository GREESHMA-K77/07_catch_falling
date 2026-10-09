

"""
Collision detection between falling objects and the basket.
"""


def is_caught(basket_rect, obj):
    # Check horizontal overlap.
    horizontal_overlap = (
        basket_rect.left <= obj.x + obj.radius
        and obj.x - obj.radius <= basket_rect.right
    )

    # Check vertical overlap.
    vertical_overlap = (
        obj.y + obj.radius >= basket_rect.top
        and obj.y - obj.radius <= basket_rect.bottom
    )

    return horizontal_overlap and vertical_overlap