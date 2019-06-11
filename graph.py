import copy
from igraph import Graph, plot


class ColouredGraph:
    """
    A data structure for representing coloured graphs.
    """
    colors_list = ["#FC4040", "#40FC40", "#4040FC", "#FCFC40", "#FC40FC", "#40FCFC", "#B57955"]

    def __init__(self, matrix, colours_number):
        """
        :param matrix: adjacency matrix representing a graph
        :param colours_number: nu,ber of colours to colour graph into
        """
        self._adjacency_list = self.matrix_to_list(matrix)
        self.colours = ColouredGraph.colors_list[:colours_number]

    @staticmethod
    def matrix_to_list(matrix):
        """
        Converts an adjancency matrix to an adjacency list.

        :param matrix: An adjacency matrix.
        :returns: A dictionary object that represents an adjacency list.
        :rtype: dict
        """
        return [{'adjacent': {row for row in range(len(matrix[col])) if matrix[col][row] != 0}, 'colour': None} for
                col in range(len(matrix))]

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

        # if any adkacent vertex already has the same colour
        if any(self._adjacency_list[adjacent]['colour'] == color for adjacent in
               self._adjacency_list[node]['adjacent']):
            raise ValueError(
                "Either one of the adjacent nodes has the same color or the node itself is already colored.")

        # color the vertex
        self._adjacency_list[node]['colour'] = color
        return True

    def __color_helper(self, vertex=0):
        if vertex == len(self._adjacency_list):
            # if all the vertices are coloured already
            return True

        # iterate over all the possible colours
        for color in self.colours:
            try:
                # try to colour in given color
                self.colour(vertex, color)

                # recurse to the next vertex
                if self.__color_helper(vertex + 1):
                    return True

                # clear the colour while going back to the previous vertex
                self._adjacency_list[vertex]['colour'] = None
            except ValueError:
                continue
        return False

    def color_graph(self):
        """ 
        Colours graph with colours pri]ovided.
        """
        # create new graph object not to mekt the method destructive
        graph = copy.deepcopy(self)

        # color the graph
        status = graph.__color_helper()
        if status is True:
            # replace all the Nones to colors names in the initial graph
            self._adjacency_list = graph._adjacency_list
        return status

    def show(self):
        """
        Show graph in default image viewer program
        """
        # create Graph object from python-igraph library
        g = Graph([(a, b) for a in range(len(self._adjacency_list))
                   for b in self._adjacency_list[a]['adjacent'] if a < b])

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
        plot(g, vertex_size=35, edge_width=2, vertex_label_dist=1.5, vertex_label_size=20, margin=70,
             vertex_label_angle=1.57, edge_color="#888888")
