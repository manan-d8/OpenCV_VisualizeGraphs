import cv2
import numpy as np
import random
import math

HWSize = 600
MinNode = 8
MaxNode = 8
SAVE_FILE = True


def GenGraph(Graph):
    G = []
    N = random.randint(MinNode, MaxNode)
    for i in range(N):
        x = random.randint(100, Graph.shape[1] - 100)
        y = random.randint(100, Graph.shape[0] - 100)
        # print(x,y)
        G.append((i, x, y))
    return G


def FindDist(A, B):
    return int(((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5)


def VALID_EDGE_OR_NOT(u, v, m):
    if u == v:
        return False
    if m[u] == False and m[v] == False:
        return False
    elif m[u] == True and m[v] == True:
        return False
    return True


def PRIMS_ALGO(G):
    Graph = G.copy()

    V = Graph.shape[0]
    Container = [False] * V
    # Here I Am Adding First Vertex Into the Mst
    Container[0] = True
    EdgeCount = 0
    MSTEdgeList = []

    for i in range(V):
        for j in range(V):
            if Graph[i][j] == 0:
                Graph[i][j] = 99999

    # Add Edges Unless V-1 Edges Are Added
    while EdgeCount < V - 1:
        minimum = math.inf
        a = -1
        b = -1
        for i in range(V):
            for j in range(V):
                if Graph[i][j] < minimum:
                    # Here I Am Checking if edge should be Added in MST or not according to prims algo.
                    if VALID_EDGE_OR_NOT(i, j, Container) == 1:
                        minimum = Graph[i][j]
                        a = i
                        b = j

        if a != -1 and b != -1:
            # print(f"Edge {EdgeCount}: ({a+1}, {b+1})")
            EdgeCount += 1
            Container[b] = Container[a] = True
            MSTEdgeList.append([a, b, minimum])
    return MSTEdgeList


def GenDist(G):
    N = len(G)

    Dist = np.zeros((N, N))

    for i in range(N):
        for j in range(i, N):
            D = FindDist(G[i], G[j])
            if random.random() > 0.5:
                D = 0
            Dist[i][j] = Dist[j][i] = D

    return Dist


def CheckValidDist(Dist):
    for i in Dist:
        if sum(i) == 0:
            return False
    return True


def ShowGraph(Graph, G, Dist):
    N = len(G)

    for i in range(N):
        for j in range(i, N):
            if Dist[i][j]:
                Graph = cv2.line(
                    Graph, (G[i][1], G[i][2]), (G[j][1], G[j][2]), (0, 0, 255), 2
                )

    for i, x, y in G:
        Graph = cv2.circle(Graph, ((x, y)), 10, (0, 255, 255), -1)

    for i in range(N):
        for j in range(i, N):
            if Dist[i][j]:
                XX, YY = (((G[i][1] + G[j][1]) // 2), ((G[i][2] + G[j][2])) // 2)
                Graph = cv2.rectangle(
                    Graph,
                    (XX, YY + 5),
                    (XX + 30, YY - 15),
                    (0, 255, 0),
                    -1,
                )
                Graph = cv2.putText(
                    Graph,
                    str(int(Dist[i][j])),
                    (XX, YY),
                    cv2.FONT_HERSHEY_TRIPLEX,
                    0.5,
                    (255, 0, 0),
                    1,
                )

    Graph = cv2.rectangle(
        Graph,
        (HWSize - 2, 0),
        (HWSize, HWSize),
        (255, 255, 255),
        -1,
    )
    Graph = cv2.putText(
        Graph,
        " Original Graph ",
        (10, 50),
        cv2.FONT_HERSHEY_TRIPLEX,
        1,
        (255, 0, 0),
        2,
    )
    print(Dist)

    MstEdges = PRIMS_ALGO(Dist)
    Mst = np.zeros((HWSize, HWSize, 3))
    MstGraph = ShowMST(Mst, G, MstEdges)
    Graph = np.concatenate([Graph, MstGraph], axis=1)

    if SAVE_FILE:
        SavePath = "Graphs/Graph_" + str(random.randint(0, 999999))
        cv2.imwrite(SavePath + ".jpg", Graph)
        WriteTxt(SavePath, Dist, G, MstEdges)

    cv2.imshow("Graph", Graph)
    cv2.waitKey(0)


def ShowMST(Graph, G, MstEdges):
    N = len(G)

    for e in MstEdges:
        Graph = cv2.line(
            Graph, (G[e[0]][1], G[e[0]][2]), (G[e[1]][1], G[e[1]][2]), (0, 0, 255), 2
        )
        XX, YY = (((G[e[0]][1] + G[e[1]][1]) // 2), ((G[e[0]][2] + G[e[1]][2])) // 2)
        Graph = cv2.rectangle(
            Graph,
            (XX, YY + 5),
            (XX + 30, YY - 15),
            (0, 255, 0),
            -1,
        )
        Graph = cv2.putText(
            Graph,
            str(int(Dist[e[0]][e[1]])),
            (XX, YY),
            cv2.FONT_HERSHEY_TRIPLEX,
            0.5,
            (255, 0, 0),
            1,
        )

    for i, x, y in G:
        Graph = cv2.circle(Graph, ((x, y)), 10, (0, 255, 255), -1)

    Cost = 0
    for e in MstEdges:
        Cost += e[2]

    Graph = cv2.putText(
        Graph,
        " Kruskal's MST ",
        (10, 50),
        cv2.FONT_HERSHEY_TRIPLEX,
        1,
        (255, 0, 0),
        2,
    )

    Graph = cv2.putText(
        Graph,
        " MST Cost : " + str(Cost),
        (10, HWSize - 50),
        cv2.FONT_HERSHEY_TRIPLEX,
        1,
        (255, 0, 0),
        2,
    )

    return Graph


def WriteTxt(path, Dist, G, MstEdges):
    File = open(path + ".txt", "w")
    File.write(str(G))
    File.write("\n#\n")
    File.write(str(Dist))
    File.write("\n#\n")
    File.write(str(MstEdges))
    File.close()


# for i in range(1):
Graph = np.zeros((HWSize, HWSize, 3))

G = GenGraph(Graph)
while True:
    Dist = GenDist(G)
    if CheckValidDist(Dist):
        break
    print("INVALID DIST")
ShowGraph(Graph, G, Dist)
