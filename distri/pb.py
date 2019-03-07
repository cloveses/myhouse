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
            if distance < 0.00000000001:
                continue
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

    return graph, points


# def dijstra(g, src, des):

#     current_vert = src
#     des_paths = {}
#     src_paths = {src:[0,[src,]], }
#     shortest = 0
#     cur_paths = []

#     while True:
#         print(cur_paths)
#         # cur_paths.append(current_vert)
#         # update des_paths distances
#         dists = {v:d + shortest for v,d in g[current_vert] if v not in src_paths}
#         for v, d in dists.items():
#             if v not in des_paths:
#                 if current_vert not in cur_paths:
#                     cur_paths.append(current_vert)
#                 des_paths[v] = [d,cur_paths[:]]
#             elif des_paths[v][0] > d:
#                 if current_vert not in cur_paths:
#                     cur_paths.append(current_vert)
#                 des_paths[v][0] = d
#                 des_paths[v][1].append(cur_paths[:])

#         # out shortest vertex
#         dists = (d[0] for d in des_paths.values())
#         if dists:
#             shortest = min(dists)
#             for v,data in des_paths.items():
#                 if data[0] == shortest:
#                     current_vert = v
#                     src_paths[v] = des_paths[v]
#                     del des_paths[v]
#                     break

#         # print(current_vert, end=',')
#         # print()
#         if current_vert == des:
#             break
#         if not des_paths:
#             break
#     print(src_paths)
#     print(des_paths)
#     print()
#     src_paths[des][1].append(des)
#     print(src_paths[des])
#     print()

def dijstra(g, src, des):

    current_vert = src
    des_paths = {}
    src_paths = {src:[0,[src,]], }
    shortest = 0
    cur_paths = []

    while True:
        # print(cur_paths)
        # cur_paths.append(current_vert)
        # update des_paths distances
        dists = {v:d + shortest for v,d in g[current_vert] if v not in src_paths}
        for v, d in dists.items():
            if v not in des_paths:
                if current_vert not in cur_paths:
                    cur_paths.append(current_vert)
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
                    cur_paths = src_paths[v][1][:]
                    del des_paths[v]
                    break

        # print(current_vert, end=',')
        # print()
        if current_vert == des:
            break
        if not des_paths:
            break
    # print(src_paths)
    # print(des_paths)
    print()
    src_paths[des][1].append(des)
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
            des_paths[v][0] = d
            des_paths[v][1] = cur_paths[:]

    # out shortest vertex
    dists = (d[0] for d in des_paths.values())
    if dists:
        shortest = min(dists)
        for v,data in des_paths.items():
            if data[0] == shortest:
                current_vert = v
                src_paths[v] = des_paths[v]
                # cur_paths = src_paths[v][1][:]
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

def all_side(src , des, vert_sets, points):
    left = set()
    right = set()
    x1, y1 = points[src]
    x2, y2 = points[des]
    for vert in vert_sets:
        x, y = points[vert]
        y_out = (((x - x1) * (y2 - y1)) / (x2 - x1)) + y1
        if y_out > y:
            left.add(vert)
        elif y_out < y:
            right.add(vert)
        if left and right:
            return True

def directly_link(g, src, des):
    for v,d in g[src]:
        if v == des:
            return d

def dijstra2(g, src, des, points):

    d = directly_link(g, src, des)
    if d:
        print(d,src,'-',des)
        return

    current_vert_before = src
    des_paths_before = {}
    src_paths_before = { }
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

        public_verts = set(src_paths_before.keys()) & set(src_paths_after.keys())
        if all_side(src, des, public_verts, points) or not des_paths_before or not des_paths_after:
            break
    # print(public_verts)


    # print(src_paths_before)
    # print()
    # print(src_paths_after)

    for public_vert in public_verts:
        print(public_vert, src_paths_before[public_vert])
        print(public_vert, src_paths_after[public_vert])
        print()

    mid,dist = get_min_path(src_paths_before, src_paths_after)
    print('mid', mid)
    paths = src_paths_before[mid][1][:]
    paths.append(mid)
    paths.extend(src_paths_after[mid][1][::-1])
    print(dist)
    print(paths)

if __name__ == '__main__':
    # g, points = build_from_file('inputk.txt')
    # print(g)

    # for i in range(len(points)):
    #     for j in (range(i+1,len(points))):

    #         print('start..',i,'--',j)
    #         dijstra(g, i, j)

    #         dijstra2(g, i , j, points)
    #         print()

    g, points = build_from_file()
    # print('start ...')

    # dijstra(g, 896, 881)
    # dijstra2(g, 896, 881, points)

    # print('start ...')
    # dijstra(g, 89, 139)
    # dijstra2(g, 89, 139, points)

    # print('start ...')
    # print(23152,g[23152])
    # print(23110,g[23110])
    # print(23153,g[23153])
    # dijstra(g, 23152, 23115)
    # dijstra2(g, 23152, 23115, points)

    print('start ...')
    dijstra(g, 23152, 23146)
    dijstra2(g, 23152, 23146, points)
