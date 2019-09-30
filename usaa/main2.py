

def get_datas(filename):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        ds = []
        for line in f.readlines():
            # print(line)
            row = line.split(',')
            row = [r.strip() for r in row]
            if row[1].isdigit() and row[2].isdigit():
                print(row)
                row[4] = float(row[4])
                row[6] = float(row[6])
                ds.append(row)
        ds.sort(key=lambda x: x[4])
        before_low_datas = [d for d in ds if d[4] < d[6]]
        after_high_datas = [d for d in ds if d[4] > d[6]]
        res = []
        res.extend(before_low_datas)
        res.extend(after_high_datas)
        return res


if __name__ == '__main__':
    print(get_datas('raw_data.csv'))
