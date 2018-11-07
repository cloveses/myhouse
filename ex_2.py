# -*- coding=utf-8 -*-

import os
import ipaddress

def get_rtab(inputfile):
    if not os.path.exists(inputfile):
        print('File is not exists!')
        return
    datas = []
    with open(inputfile) as f:
        while True:
            net = f.readline().strip()
            next_hop = f.readline().strip()
            out_interface = f.readline().strip()
            if not net:
                break
            net = ipaddress.IPv4Network(net)
            datas.append((net,next_hop,out_interface))
    if not datas:
        print('Router table is null!')
        return
    return datas

def get_rpackets(inputfile):
    if not os.path.exists(inputfile):
        print('File is not exists!')
        return
    datas = []
    with open(inputfile) as f:
        while True:
            dest = f.readline().strip()
            if not dest:
                break
            dest = ipaddress.IPv4Address(dest)
            datas.append(dest)
    if not datas:
        print('RandomPackets is null!')
        return
    return datas

def match_net(addr,rtabs):
    for rtab in rtabs:
        if addr in rtab[0]:
            return rtab

def main(rtabfile='RoutingTable.txt', rpacketsfile='RandomPackets.txt' , outputfile='RoutingOutput.txt'):
    rtab = get_rtab(rtabfile)
    # print(rtab)
    rpackets = get_rpackets(rpacketsfile)
    # print(rpackets)
    datas = []
    for rpacket in rpackets:
        if rpacket.is_loopback:
            outstr = '%s is loopback;discarded.' % str(rpacket)
        elif rpacket.is_reserved:
            outstr = '%s is malformed;discarded.' % str(rpacket)
        else:
            result = match_net(rpacket,rtab)
            if result:
                if '-' in result:
                    outstr = '%s will be forwarded on the directly connected network on interface %s.' % (str(rpacket),result[-1])
                else:
                    outstr = '%s will be forwarded to %s out on interface %s.' % (str(rpacket),result[1],result[-1])
        datas.append(outstr + '\n')
    if datas:
        try:
            with open(outputfile,'w') as f:
                f.writelines(datas)
        except:
            print('Failed to write datas into file.')



if __name__ == '__main__':
    main()