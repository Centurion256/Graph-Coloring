class ColouredGraph(object):

    def __init__(self, matrix):

        self._adjacency_list = self.matrix_to_dict(matrix)

    @staticmethod
    def matrix_to_dict(matrix):

        return {col: {row for row in range(len(matrix[col])) if matrix[col][row] != 0} for col in range(len(matrix))}

    def __str__(self):

        return "\n".join(f"{x}: {self._adjacency_list[x]}" for x in self._adjacency_list)
        
if __name__ == "__main__":
    
    matrix = [[1,1,0],[0,0,1],[1,0,0]]
    graph = ColouredGraph(matrix)
    print(graph)
