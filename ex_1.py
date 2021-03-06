# -*- coding=utf-8 -*-

import os

def get_fdb(inputfile):

    if not os.path.exists(inputfile):
        print('File is not exists!')
        return
    fdb_datas = {}
    # open the BridgeFDB.txt file and read data to a dictionary.
    with open(inputfile) as f:
        while True:
            mac = f.readline().strip()
            port = f.readline().strip()
            if not mac:
                break
            fdb_datas[mac] = port
    if not fdb_datas:
        print('Bridge_FDB is null!')
        return
    return fdb_datas

def get_rframes(inputfile):
    if not os.path.exists(inputfile):
        print('File is not exists!')
        return
    rframes = []
    # # open the BridgeFDB.txt file and read data to a list.
    with open(inputfile) as f:
        while True:
            src = f.readline().strip()
            dest = f.readline().strip()
            port = f.readline().strip()
            if not src:
                break
            rframes.append((src,dest,port))
    if not rframes:
        print('RandomFrames is null!')
        return
    return rframes



def main(fdbfile='BridgeFDB.txt', rframesfile='RandomFrames.txt' , outputfile='BridgeOutput.txt'):
    fdb_datas = get_fdb(fdbfile)
    # print(fdb_datas)
    rframes = get_rframes(rframesfile)
    # print(rframes)
    if fdb_datas and rframes:
        # use outdatas to save the output information.
        outdatas = []
        # start to go through all RandomFrames
        for rframe in rframes:
            outstr = '\t'.join(rframe)
            # deal with the random frame in the FDB.
            if rframe[1] in fdb_datas:
                # the random frame has been in the destination.
                if rframe[2] == fdb_datas[rframe[1]]:
                    print(rframe,'Discarded')
                    outstr += ''.join(('\t','Discarded','\n'))
                    outdatas.append(outstr)
                else:
                    # deal with the random frame need to forward.
                    print(rframe,'Forwarded on port %s' % fdb_datas[rframe[1]])
                    outstr += ''.join(('\t','Forwarded on port %s' % fdb_datas[rframe[1]],'\n'))
                    outdatas.append(outstr)
            else:
                print(rframe,'Broadcast')
                outstr += ''.join(('\t','Broadcast','\n'))
                outdatas.append(outstr)
            if rframe[0] not in fdb_datas:
                # update Bridge_FDB.
                fdb_datas[rframe[0]] = rframe[2]
        # fdb_strs = ['/t'.join((k,v)) for k,v in fdb_datas.items()]
        # fdb_strs = '\n' + 'BridgeFDB' +'\n' + '\n'.join(fdb_strs)
        if outdatas:
            try:
                # save the result into file.
                with open(outputfile,'w') as f:
                    f.writelines(outdatas)
                    # f.write(fdb_strs)
            except:
                print('Write Error!')


if __name__ == '__main__':
    main()