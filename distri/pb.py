import math

def build_from_file(vert_file='usa.txt'):
    points = {}
    graph = [None,]
    dist = lambda x,y,m,n:math.sqrt((x - m) ** 2 + (y - n) ** 2)

    with open(vert_file, 'r') as f:
        vertices,edges = map(int,f.readline().strip().split(' '))

        for i in range(vertices):
            line = f.readline().strip().split(' ')
            line = [d for d in line if d.strip()]
            points[int(line[0])] = (int(line[1]), int(line[-1]))
        f.readline()
        graph = graph * vertices

        for i in range(edges):
            datas = [d for d in f.readline().strip().split(' ') if d.strip()]
            x,y = map(int,datas)
            distance = dist(points[x][0], points[x][1], points[y][0], points[y][1])
            if graph[x]:
                graph[x].append([y, distance])
            else:
                graph[x] = [[y, distance], ]

            if graph[y]:
                graph[y].append([x, distance])
            else:
                graph[y] = [[x, distance], ]
    # for g in graph:
    #     print(g)

    return graph


def dijstra(g, src, des):

    current_vert = src
    des_paths = {}
    src_paths = {src:[0,[src,]], }
    shortest = 0
    cur_paths = []

    while True:
        cur_paths.append(current_vert)
        # update des_paths distances
        dists = {v:d + shortest for v,d in g[current_vert] if v not in src_paths}
        for v, d in dists.items():
            if v not in des_paths:
                des_paths[v] = [d,cur_paths[:]]
            elif des_paths[v][0] > d:
                if current_vert not in cur_paths:
                    cur_paths.append(current_vert)
                des_paths[v][0] = d
                des_paths[v][1].append(cur_paths[:])

        # out shortest vertex
        dists = (d[0] for d in des_paths.values())
        if dists:
            shortest = min(dists)
            for v,data in des_paths.items():
                if data[0] == shortest:
                    current_vert = v
                    src_paths[v] = des_paths[v]
                    del des_paths[v]
                    break

        # print(current_vert, end=',')
        # print()
        if current_vert == des:
            break
        if not des_paths:
            break
    print()
    print(src_paths[des])
    print()



def dijstra2(g, src, des):

    current_vert = src
    des_paths = {}
    src_paths = {src:[0,[src,]], }
    shortest = 0
    cur_paths = []

    while True:
        cur_paths.append(current_vert)
        # update des_paths distances
        dists = {v:d + shortest for v,d in g[current_vert] if v not in src_paths}
        for v, d in dists.items():
            if v not in des_paths:
                des_paths[v] = [d,cur_paths[:]]
            elif des_paths[v][0] > d:
                if current_vert not in cur_paths:
                    cur_paths.append(current_vert)
                des_paths[v][0] = d
                des_paths[v][1].append(cur_paths[:])

        # out shortest vertex
        dists = (d[0] for d in des_paths.values())
        if dists:
            shortest = min(dists)
            for v,data in des_paths.items():
                if data[0] == shortest:
                    current_vert = v
                    src_paths[v] = des_paths[v]
                    del des_paths[v]
                    break

        # print(current_vert, end=',')
        # print()
        if current_vert == des:
            break
        if not des_paths:
            break
    print()
    print(src_paths[des])
    print()

if __name__ == '__main__':
    # g = build_from_file('inputk.txt')
    # dijstra(g, 0, 5)
    g = build_from_file()
    dijstra(g, 896, 881)