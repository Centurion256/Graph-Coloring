from Graph import Graph

# generate the lost of colors being used in graph coloring
colors_list = ["#FC4040", "#40FC40", "#4040FC", "#FCFC40", "#FC40FC", "#40FCFC", "#B57955"]

# get the number of vertices fro user
vertices = 0
while not vertices:
    try:
        vertices = int(input("Enter the number of vertices in graph ( > 0): "))
        if vertices <= 0:
            raise ValueError
    except ValueError:
        vertices = 0

# generate adjacency matrix
matrix = [[0 for i in range(vertices)] for j in range(vertices)]
print(f"Added vertices {', '.join(map(str, range(vertices)))}")

# get the connected vertices from user
while True:
    pair = input(
        "Enter the pair of connected vertices(e.g. '0 2'(without quotes)) or press return to finish prompt:")
    if not pair:
        break
    pair.replace(',', '')
    try:
        a, b = map(int, pair.split())
        matrix[a][b] = 1
        matrix[b][a] = 1
    except:
        print("Wrong input")

# get the number of colors from user
colors = 0
while not colors:
    try:
        colors = int(input("Enter the number of colors of the graph (0 < colors < 8): "))
        if not 0 < colors < 8:
            raise ValueError
    except ValueError:
        colors = 0

# crete graph and try to colour it
graph = ColouredGraph(matrix, colors_list[:colors])
if not graph.color_graph():
    print(f"Cant colour this graph into {colors} colors")

# show the image to user
graph.show()
