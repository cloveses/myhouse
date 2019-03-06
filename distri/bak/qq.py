import random
from base import *


def dijkstra(g, info):
    src, des = info
    src_paths = {src:[0,[]], }
    des_paths = {vert.getName():[-1,[]] for vert in g.vertList.values() 
                if vert.getName() != src }
    shortest = 0
    curr_id = src
    while des_paths:
        curr_vert = g.getVertex(curr_id)
        if not curr_vert:
            continue

        # update des_paths
        dists = {vid:dist+shortest for vid, dist in 
                    curr_vert.connectedTo.items() if vid not in src_paths}
        for vid,dist in dists.items():
            if des_paths[vid][0] == -1:
                des_paths[vid][0] = dist
            elif des_paths[vid][0] > dist:
                des_paths[vid][0] = dist
                des_paths[vid][1].append(curr_id)

        # out  shortest vertex
        dists = [d[0] for d in des_paths.values() if d[0] != -1]
        if dists:
            shortest = min(dists)
            for k,v in des_paths.items():
                if v[0] == shortest:
                    v[1].append(k)
                    src_paths[k] = [v[0],v[1]]
                    curr_id = k
                    del des_paths[k]
                    break
        # add path
        for vid,dist in des_paths.items():
            if dist[0] == -1:
                dist[1].append(curr_id)

        # print('src_paths',src_paths)
    print(src,end=' ')
    for p in src_paths[des][-1]:
        print(p, end=' ')


def dijkstra_2(g, info):
    src, des = info
    src_paths = {src:[0,[]], }
    des_paths = {vert.getName():[-1,[]] for vert in g.vertList.values() 
                if vert.getName() != src }
    shortest = 0
    curr_id = src
    while des_paths:
        curr_vert = g.getVertex(curr_id)
        if not curr_vert:
            continue
        # update des_paths
        dists = {vid:dist+shortest for vid, dist in 
                    curr_vert.connectedTo.items() if vid not in src_paths}
        for vid,dist in dists.items():
            if des_paths[vid][0] == -1:
                des_paths[vid][0] = dist
            elif des_paths[vid][0] > dist:
                des_paths[vid][0] = dist
                des_paths[vid][1].append(curr_id)

        # out shortest vertex
        dists = [d[0] for d in des_paths.values() if d[0] != -1]
        if dists:
            shortest = min(dists)
            for k,v in des_paths.items():
                if v[0] == shortest:
                    v[1].append(k)
                    src_paths[k] = [v[0],v[1]]
                    curr_id = k
                    del des_paths[k]
                    break
        if curr_id == des:
            break
        # add path
        for vid,dist in des_paths.items():
            if dist[0] == -1:
                dist[1].append(curr_id)

        # print('src_paths',src_paths)
    print(src,end=' ')
    for p in src_paths[des][-1]:
        print(p, end=' ')

def tool(g, shortest, curr_id, src_paths, des_paths):
    curr_vert = g.getVertex(curr_id)
    if not curr_vert:
        return shortest, curr_id
    # update des_paths
    dists = {vid:dist+shortest for vid, dist in 
                curr_vert.connectedTo.items() if vid not in src_paths}
    for vid,dist in dists.items():
        if des_paths[vid][0] == -1:
            des_paths[vid][0] = dist
        elif des_paths[vid][0] > dist:
            des_paths[vid][0] = dist
            des_paths[vid][1].append(curr_id)

    # out shortest vertex
    dists = [d[0] for d in des_paths.values() if d[0] != -1]
    if dists:
        shortest = min(dists)
        for k,v in des_paths.items():
            if v[0] == shortest:
                v[1].append(k)
                src_paths[k] = [v[0],v[1]]
                curr_id = k
                del des_paths[k]
                break
    # if curr_id == des:
    #     break

    # add path
    for vid,dist in des_paths.items():
        if dist[0] == -1:
            dist[1].append(curr_id)

    return shortest, curr_id

def get_min_path(flag, src_paths, des_paths):
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


def dijkstra_3(g, info):
    src, des = info
    src_paths_before = {src:[0,[]], }
    des_paths_before = {vert.getName():[-1,[]] for vert in g.vertList.values() 
                if vert.getName() != src }
    shortest_before = 0
    curr_id_before = src

    src_paths_after = {des:[5,[]], }
    des_paths_after = {vert.getName():[-1,[]] for vert in g.vertList.values() 
                if vert.getName() != des }
    shortest_after = 0
    curr_id_after = des

    # while minpaths have public element:quit
    flag = None
    while not flag:
        shortest_before, curr_id_before = tool(g, shortest_before, 
            curr_id_before, src_paths_before, des_paths_before)

        shortest_after, curr_id_after = tool(g, shortest_after, 
            curr_id_after, src_paths_after, des_paths_after)

        flag = set(src_paths_before.keys()) & set(src_paths_after.keys())

    #     print('src_paths',src_paths)
    # print(src,end=' ')
    # for p in src_paths[des][-1]:
    #     print(p, end=' ')
    # print(flag)
    # print(src_paths_before)
    # print(src_paths_after)

    # get min path from flag(middle vertex)
    mid,dist = get_min_path(flag, src_paths_before, src_paths_after)
    print(src, end=' ')
    for vert in src_paths_before[mid][1]:
        print(vert, end=' ')
    for vert in src_paths_after[mid][1][1:]:
        print(vert, end='')
    print(des, end='')

def simple_test():
    g, info = build_from_file_test()
    print('initial...')
    dijkstra(g, info)
    print('idea 1')
    dijkstra_2(g, info)
    print('idea 2')
    dijkstra_3(g, info)

def main():
    g, vert_num = build_from_file()
    infos = []
    random.seed(2)
    for i in range(3):
        infos.append((random.randint(0,vert_num-1), random.randint(0,vert_num-1)))
    print(infos)
    for info in infos:
        # print('initial...')
        # dijkstra(g, info)
        # print('idea 1')
        # dijkstra_2(g, info)
        print('idea 2')
        dijkstra_3(g, info)

if __name__ == '__main__':

    main()