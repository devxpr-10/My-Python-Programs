class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class QueueFrontier:
    def __init__(self):
        self.frontier = []
        self.frontierStates = set()

    def add(self, node: Node):
        self.frontier.append(node)
        self.frontierStates.add(node.state)

    def remove(self) -> Node:
        node = self.frontier.pop(0)
        self.frontierStates.remove(node.state)
        return node
    
    def empty(self):
        return len(self.frontier) == 0
        
class StackFrontier(QueueFrontier):
    def remove(self):
        node = self.frontier.pop(-1)
        self.frontierStates.remove(node.state)
        return node

def locOf(el):
    for r_idx, r in enumerate(mazeDat):
        if el in r:
            return (r_idx, r.find(el))
    return None

def expand(node: Node) -> list[Node]:
    nodes = []
    r, c = node.state
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        # Boundary check
        if 0 <= nr < colSize and 0 <= nc < rowSize:
            if mazeDat[nr][nc] != '#':
                nodes.append(Node((nr, nc), node, None))
    return nodes

def solve(maze: list[str], mode: str = "BFS"):
    global mazeDat, colSize, rowSize
    """Solves the maze and returns the pathway. Mode can be either BFS(Breadth First Search) or DFS(Depth First Search)"""

    mazeDat = maze
    rowSize = max(len(md) for md in mazeDat)
    colSize = len(mazeDat)

    start_state = locOf('A')
    goalState = locOf('B')

    frontier = QueueFrontier() if mode == "BFS" else StackFrontier()
    exploredStates = set()

    node = Node(start_state, None, None)
    frontier.add(node)

    goal_node = None

    while True:
        if frontier.empty(): 
            return None

        node = frontier.remove()

        if node.state == goalState: 
            goal_node = node
            break

        exploredStates.add(node.state)

        for child in expand(node):
            if child.state not in exploredStates and child.state not in frontier.frontierStates:
                frontier.add(child)

    pathway = []
    node = goal_node.parent
    while node.parent != None:
        pathway.append(node.state)
        node = node.parent
    pathway.reverse()

    return pathway