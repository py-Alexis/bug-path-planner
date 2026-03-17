import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_dilation


def bresenham(x1, y1=None, x2=None, y2=None):
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


def expand_obstacles(matrix, robot_radius):
    radius = int(max(0, robot_radius))
    if radius == 0:
        return matrix

    grid = np.array(matrix, dtype=bool)
    y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
    disk = (x * x + y * y) <= radius * radius
    expanded = binary_dilation(grid, structure=disk)
    return expanded.astype(np.uint8).tolist()

def image_to_binary_matrix(image_path: str, threshold: int = 5, invert: bool = False):
    """
    Load an image and convert it to a binary matrix
    0 (free) or 1 (obstacle)
    """
    img = plt.imread(image_path)

    if img.ndim == 3:
        rgb = img[..., :3].astype(np.float32)

        if rgb.max() <= 1.0:
            rgb = rgb * 255.0

        gray = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    else:
        gray = img.astype(np.float32)
        if gray.max() <= 1.0:
            gray = gray * 255.0

    binary = (gray < threshold).astype(np.uint8)

    if invert:
        binary = 1 - binary

    return binary.tolist()


def select_start_end(matrix):
    from bug import Pose

    title = "Click START, then END (2 clicks)"
    grid = np.array(matrix, dtype=np.uint8)

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.imshow(grid, cmap="gray_r")

    print("\n=== Click START position, then END position on the map ===")
    clicks = plt.ginput(2, timeout=0)
    plt.close(fig)

    if len(clicks) < 2:
        print("That's not 2 points")
        select_start_end(matrix)

    start_pose = Pose(int(round(clicks[0][0])), int(round(clicks[0][1])))
    end_pose = Pose(int(round(clicks[1][0])), int(round(clicks[1][1])))

    print(f"Start: ({start_pose.x}, {start_pose.y})")
    print(f"End:   ({end_pose.x}, {end_pose.y})")

    return start_pose, end_pose