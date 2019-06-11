import copy


class ColouredGraph:
    def __init__(self, matrix, colours):
        self._adjacency_list = self.matrix_to_dict(matrix)
        self.colours = colours

    @staticmethod
    def matrix_to_dict(matrix):
        return {col: {'adjacent': {row for row in range(len(matrix[col])) if matrix[col][row] != 0}, 'colour': None} for
                col in range(len(matrix))}

    def __str__(self):
        return "\n".join(f"{x}: {self._adjacency_list[x]}" for x in self._adjacency_list)

    def __getitem__(self, pos):
        if pos not in range(0, len(self._adjacency_list)):
            raise IndexError
        return self._adjacency_list[pos]

    def colour(self, node, color):
        if color not in self.colours:
            raise KeyError(f"Colour \'{color}\' is not available for this graph.")
        if any(self._adjacency_list[adjacent]['colour'] == color for adjacent in
               self._adjacency_list[node]['adjacent']):
            raise ValueError(
                "Either one of the adjacent nodes has the same color or the node itself is already colored.")
        self._adjacency_list[node]['colour'] = color
        return True

    def __color_helper(self, vertex=0):
        if vertex == len(self._adjacency_list):
            return True

        for color in self.colours:
            try:
                self.colour(vertex, color)
                print(self, "\n")
                if self.__color_helper(vertex + 1):
                    return True
                else:
                    self._adjacency_list[vertex]['colour'] = None
            except ValueError:
                continue
        return False

    def color_graph(self):
        graph = copy.deepcopy(self)
        status = graph.__color_helper()
        if status is True:
            self._adjacency_list = graph._adjacency_list
        return status


if __name__ == "__main__":
    mtr = [[0, 1, 1, 0, 1, 1], [1, 0, 1, 1, 0, 1], [1, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1], [1, 0, 1, 1, 0, 1],
              [1, 1, 0, 1, 1, 0]]
    graph = ColouredGraph(mtr, ("R", "G", "B"))
    # graph.colour(1, 'R')
    # graph.colour(2, 'R')
    # graph.colour(0, 'G')
    print(graph.color_graph())
    print(graph)
