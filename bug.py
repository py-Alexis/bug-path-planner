from utils import bresenham, expand_obstacles


class Pose:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Pose):
            return self.x == other.x and self.y == other.y
        return False

    def is_free(self, matrix):
        return False if matrix[self.y][self.x] else True

    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def print(self):
        print(f"x={self.x}, y={self.y}")

    def cell(self, matrix):
        return matrix[self.y][self.x]
    
    def print_matrix(self, matrix):
        print()
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if self and self.x == x and self.y == y:
                    print("●", end="")  # Represent the robot's position
                elif cell == 1:
                    print("■", end="")  # Filled square for obstacles
                else:
                    print("□", end="")  # Empty space for free cells
            print() 
        print()

    def circle_next_cell(self, matrix, clockwise=True):
        directions = [
            (-1, 0),  # Top
            (-1, 1),  # Top-right
            (0, 1),   # Right
            (1, 1),   # Bottom-right
            (1, 0),   # Bottom
            (1, -1),  # Bottom-left
            (0, -1),  # Left
            (-1, -1)  # Top-left
        ]

        if not clockwise:
            directions = directions[::-1]

        next_cell = None

        for dx, dy in directions:
            neighbour = Pose(self.x+dx, self.y+dy)
            # print("neighbour visisted = ",end="")
            # neighbour.print()

            try:
                if not neighbour.cell(matrix):
                    if dx == 0 or dy == 0:
                        next_cell = neighbour
                else:
                    if next_cell:
                        return next_cell

            except:
                # quick way to not have to check if in bound
                # not a good practice because if there is another error it will be ignored
                pass

        if next_cell:
            return next_cell

                


def bug1(matrix, robot_radius, start_pose, end_pose):
    matrix = expand_obstacles(matrix, robot_radius)
    if not start_pose.is_free(matrix) or not end_pose.is_free(matrix):
        return []

    FREE_PATH = "free_path"
    AVOIDING_OBSTACLE = "avoiding_obstacle"
    RETURNING_TO_CLOSEST = "returning_to_closest"


    state = FREE_PATH
    current_pose = start_pose
    current_free_path = bresenham(start_pose.x, start_pose.y, end_pose.x, end_pose.y)[1:]
    print(current_free_path)

    path_taken = []
    
    while current_pose != end_pose:

        path_taken.append((current_pose.x, current_pose.y))
        if state == FREE_PATH:
            if not matrix[current_free_path[0][1]][current_free_path[0][0]]:
                current_pose = Pose(*current_free_path.pop(0))
            else:
                start_circle = current_pose
                closest_point = current_pose
                circle_step = 0
                closest_step = 0

                state = AVOIDING_OBSTACLE

        if state == AVOIDING_OBSTACLE:
            next_point = current_pose.circle_next_cell(matrix)

            if next_point == start_circle:
                current_pose = next_point
                state = RETURNING_TO_CLOSEST
                returning_clockwise = closest_step < circle_step/2


            else:
                current_pose = next_point
                circle_step += 1

                if current_pose.distance_to(end_pose) < closest_point.distance_to(end_pose):
                    closest_point = current_pose
                    closest_step = circle_step
                    

        elif state == RETURNING_TO_CLOSEST:
            next_point = current_pose.circle_next_cell(matrix, returning_clockwise)
            current_pose = next_point

            if current_pose == closest_point:
                state = FREE_PATH
                current_free_path = bresenham(current_pose.x, current_pose.y, end_pose.x, end_pose.y)[1:]
                if not Pose(*current_free_path[0]).is_free(matrix):
                    return path_taken
                
            

        # print("current state", state)
        # current_pose.print_matrix(matrix)
        # print("=====================")


    path_taken.append((current_pose.x, current_pose.y))
    return path_taken


def bug2(matrix, robot_radius, start_pose, end_pose):
    matrix = expand_obstacles(matrix, robot_radius)
    if not start_pose.is_free(matrix) or not end_pose.is_free(matrix):
        return []

    FREE_PATH = "free_path"
    AVOIDING_OBSTACLE = "avoiding_obstacle"
    RETURNING_TO_CLOSEST = "returning_to_closest"


    state = FREE_PATH
    current_pose = start_pose
    current_free_path = bresenham(start_pose.x, start_pose.y, end_pose.x, end_pose.y)[1:]
    print(current_free_path)

    path_taken = []
    
    while current_pose != end_pose:

        path_taken.append((current_pose.x, current_pose.y))
        if state == FREE_PATH:
            if not matrix[current_free_path[0][1]][current_free_path[0][0]]:
                current_pose = Pose(*current_free_path.pop(0))
            else:
                start_circle = current_pose
                circle_step = 0
                closest_step = 0

                state = AVOIDING_OBSTACLE

        if state == AVOIDING_OBSTACLE:
            next_point = current_pose.circle_next_cell(matrix)
            # print(current_free_path)

            if next_point == start_circle:
                return path_taken

            elif (next_point.x, next_point.y) in current_free_path:
                current_pose = next_point
                state = FREE_PATH

                index = current_free_path.index((current_pose.x, current_pose.y))
                current_free_path = current_free_path[index+1:]


            else:
                current_pose = next_point
                circle_step += 1
            

        # print("current state", state)
        # current_pose.print_matrix(matrix)
        # print("=====================")


    path_taken.append((current_pose.x, current_pose.y))
    return path_taken


if __name__ == "__main__":
    # Create an empty matrix (5x5 grid with no obstacles)
    matrix = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]


    test_pose = Pose(3,2)

    # Define start and end poses
    start_pose = Pose(5, 0)
    end_pose = Pose(5, 11)

    # Run the bug1 algorithm
    
    path = bug2(matrix, robot_radius=1, start_pose=start_pose, end_pose=end_pose)

    # Print the path taken
    print("Path taken by the robot:")
    for step in path:
        print(step)
