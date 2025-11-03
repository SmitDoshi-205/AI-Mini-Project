# A* pathfinding algorithm 
import heapq

def heuristic(a, b):
    # Manhattan heuristic for grid
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    """
    grid: 2D list where 0 = walkable, 1 = blocked
    start, goal: (x, y) grid coordinates (integers)
    returns: list of cells from start to goal (includes start & goal) or [] if no path
    """
    if start == goal:
        return [start]

    rows = len(grid)
    cols = len(grid[0])
    open_heap = []
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    heapq.heappush(open_heap, (f_score[start], start))
    came_from = {}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path.reverse()
            return path
        cx, cy = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                tentative = g_score[current] + 1
                neighbor = (nx, ny)
                if tentative < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative
                    f_score[neighbor] = tentative + heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (f_score[neighbor], neighbor))
    return []