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

def tools(g, current_vert, shortest, cur_paths, src_paths, des_paths):

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

    return current_vert, shortest

def get_min_path(src_paths, des_paths):
    flag = set(src_paths.keys()) & set(des_paths.keys())
    min_dist = -1
    min_mid = None
    for mid in flag:
        dist = src_paths[mid][0] + des_paths[mid][0]
        if min_dist != -1:
            if dist < min_dist:
                min_dist = dist
                min_mid = mid
        else:
            min_dist = dist
            min_mid = mid
    return min_mid, min_dist

def dijstra2(g, src, des):

    current_vert_before = src
    des_paths_before = {}
    src_paths_before = {src:[0,[src,]], }
    shortest_before = 0
    cur_paths_before = []

    current_vert_after = des
    des_paths_after = {}
    src_paths_after = {des:[des,[src,]], }
    shortest_after = 0
    cur_paths_after = []

    while True:
        current_vert_before, shortest_before = tools(g, 
            current_vert_before, shortest_before,
            cur_paths_before, src_paths_before, des_paths_before)

        current_vert_after, shortest_after = tools(g, 
            current_vert_after, shortest_after,
            cur_paths_after, src_paths_after, des_paths_after)

        if set(src_paths_before.keys()) & set(src_paths_after.keys()):
            break

    print(src_paths_before)
    print()
    print(src_paths_after)
    mid,dist = get_min_path(src_paths_before, src_paths_after)
    print(mid)
    paths = src_paths_before[mid][1][:]
    paths.append(mid)
    paths.extend(src_paths_after[mid][1][::-1])
    print(dist)
    print(paths)

if __name__ == '__main__':
    g = build_from_file('inputk.txt')

    dijstra(g, 3, 4)

    dijstra2(g, 3 , 4)

    # g = build_from_file()

    # dijstra(g, 896, 881)
    # dijstra2(g, 896, 881)

    # dijstra(g, 89, 139)
    # dijstra2(g, 89, 139)

    # dijstra(g, 23152, 23115)
    # dijstra2(g, 23152, 23115)