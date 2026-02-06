def bresenham(x1, y1=None, x2=None, y2=None):
    """
    Generate integer points on a line using Bresenham's algorithm.

    Usage:
        bresenham(x1, y1, x2, y2)
        bresenham(p1, p2) where p1 = [x1, y1], p2 = [x2, y2]

    Returns:
        List of (x, y) tuples
    """

    # Handle 2-argument form
    if y1 is not None and x2 is None and y2 is None:
        p1 = x1
        p2 = y1
        x1, y1 = p1
        x2, y2 = p2
    elif y2 is None:
        raise ValueError("Expecting either 2 or 4 arguments")

    x = x1
    y = y1

    if x2 > x1:
        xd = x2 - x1
        dx = 1
    else:
        xd = x1 - x2
        dx = -1

    if y2 > y1:
        yd = y2 - y1
        dy = 1
    else:
        yd = y1 - y2
        dy = -1

    points = []

    if xd > yd:
        a = 2 * yd
        b = a - xd
        c = b - xd

        while True:
            points.append((x, y))
            if x == x2 and y == y2:
                break

            if b < 0:
                b += a
                x += dx
            else:
                b += c
                x += dx
                y += dy
    else:
        a = 2 * xd
        b = a - yd
        c = b - yd

        while True:
            points.append((x, y))
            if x == x2 and y == y2:
                break

            if b < 0:
                b += a
                y += dy
            else:
                b += c
                x += dx
                y += dy

    return points
