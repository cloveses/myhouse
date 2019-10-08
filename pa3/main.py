import orderlog

ORDERS = orderlog.orderlst

def get_input(info):
    while True:
        days = input(info)
        days = days.strip()
        if days and days.isdigit():
            return int(days)

def get_minutes(mdate):
    mtime = mdate.split()[-1]
    h, m, _ = mtime.split(':')
    return (int(h) - 6) * 60 + int(m)

def output(summaries, minutes):
    title = 'ORDER SUMMARY'
    print(format(title, ' >30'))
    print('    TIME \\ DAY  | 1 2 3 4 5 6 7 8 9 10')
    print('------------------------------------------------')
    h = 6
    m = 0
    for summary in summaries:
    # for i in range(18):
        start_time = ':'.join((str(h),str(m).zfill(2)))
        m += minutes
        h += m // 60
        m = m % 60
        end_h = h + 0
        end_m = m - 1
        if end_m < 0:
            end_h -= 1
            end_m += 60
        end_time = ':'.join((str(end_h),str(end_m).zfill(2)))
        print(format(' - '.join((start_time, end_time)), ' >15'), end=' | ')
        summary = [format(str(s), ' >2') for s in summary]
        print(' '.join(summary))

def main():
    days = get_input('How many days would you like to include?')
    minutes = get_input('Please specify the length of the time interval in minutes:')
    datas = ORDERS[1:]
    # datas.sort(key=lambda d:d[0])
    datas = [d for d in datas if int(d[0][8:10]) <= days]
    summaries = []
    # 初始化存放结果数据列表
    for _ in range(((24 - 6) * 60) // minutes):
        summaries.append([0,] * days)

    for data in datas:
        minute_seq = get_minutes(data[0]) // minutes
        day_seq = int(data[0][8:10]) - 1
        summaries[minute_seq][day_seq] += 1
    print(summaries)
    output(summaries, minutes)

main()