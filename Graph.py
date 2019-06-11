import copy
from igraph import Graph, plot


class ColouredGraph:
    """ 
    A data structure for representing coloured graphs.
    """

    def __init__(self, matrix, colours):
        self._adjacency_list = self.matrix_to_dict(matrix)
        self.colours = colours

    @staticmethod
    def matrix_to_dict(matrix):
        """
        Converts an adjancency matrix to an adjacency list(dict).

        :param matrix: An adjacency matrix.
        :returns: A dictionary object that represents an adjacency list.
        :rtype: dict
        """
        return {col: {'adjacent': {row for row in range(len(matrix[col])) if matrix[col][row] != 0}, 'colour': None} for
                col in range(len(matrix))}

    def __str__(self):
        return "\n".join(f"{x}: {self._adjacency_list[x]}" for x in self._adjacency_list)

    def __getitem__(self, pos):
        if pos not in range(0, len(self._adjacency_list)):
            raise IndexError
        return self._adjacency_list[pos]

    def colour(self, node, color):
        """
        Colours a given vertex with the specified colour.

        :param node: a vertex, an integer value.
        :param color: the colour in which the vertex should be painted. 
        :returns: A boolean value, signifying that the colouring operation was completed sucessfully.
        :rtype: bool
        """
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
                if self.__color_helper(vertex + 1):
                    return True
                self._adjacency_list[vertex]['colour'] = None
            except ValueError:
                continue
        return False

    def color_graph(self):
        """ 
        Colours graph with colours privided.
        """
        graph = copy.deepcopy(self)
        status = graph.__color_helper()
        if status is True:
            self._adjacency_list = graph._adjacency_list
        return status

    def show(self):
        """
        Show graph in default image viewer program
        """
        # create Graph object from python-igraph library
        g = Graph([(a, b) for a in range(len(self._adjacency_list)) for b in self._adjacency_list[a]['adjacent']])

        # add labels to vertices to distinguish between them
        g.vs["label"] = list(range(len(self._adjacency_list)))

        # add proper color to every vertex
        for vertex in g.vs:
            if self._adjacency_list[vertex['label']]['colour'] is None:
                # if vertes is not colored
                vertex['color'] = "#FFFFFF"
            else:
                vertex["color"] = self._adjacency_list[vertex['label']]['colour']

        # show the graph to user
        plot(g, vertex_size=35, edge_width=2, vertex_label_dist=1.5, vertex_label_size=20, margin=40,
             vertex_label_angle=1.57, edge_color="#888888")
