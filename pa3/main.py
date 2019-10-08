import orderlog

ORDERS = orderlog.orderlst

def get_input(info):
    while True:
        days = input(info)
        days = days.strip()
        if days:
            if days.isdigit():
                return int(days)
            elif days.startswith('-') and days[1:].isdigit():
                return int(days)

def labelString(n, base=6 * 60, interval=60):
    minutes = base + n * interval
    start_h = minutes // 60
    start_m = minutes % 60
    minutes = base + (n + 1) * interval - 1
    end_h  = minutes // 60
    end_m = minutes % 60
    start_time = ':'.join((str(start_h),str(start_m).zfill(2)))
    end_time = ':'.join((str(end_h),str(end_m).zfill(2)))
    return ' - '.join((start_time, end_time))

# for i in range(4):
#     print(labelString(i))

def get_minutes(mdate):
    mtime = mdate.split()[-1]
    h, m, _ = mtime.split(':')
    return (int(h) - 6) * 60 + int(m)

def composeOrderMatrix(days=31, interval=60):
    datas = ORDERS[1:]
    datas = [d for d in datas if int(d[0][8:10]) <= days]
    summaries = []
    # 初始化存放结果数据列表
    for _ in range(((24 - 6) * 60) // interval):
        summaries.append([0,] * days)

    for data in datas:
        minute_seq = get_minutes(data[0]) // interval
        day_seq = int(data[0][8:10]) - 1
        summaries[minute_seq][day_seq] += 1
    return summaries

# print(composeOrderMatrix(10))
def printOrderSummaryMatrix(summaries, interval):
    print()
    title = 'ORDER SUMMARY'
    print(format(title, ' >30'))
    print()
    print('    TIME \\ DAY  | 1 2 3 4 5 6 7 8 9 10')
    print('------------------------------------------------')
    i = 0
    for summary in summaries:
        label = labelString(i, interval=interval)
        print(format(label, ' >15'), end=' | ')
        summary = [format(str(s), ' >2') for s in summary]
        print(' '.join(summary))
        i += 1
    print()

def printHistogram(summaries, nday, interval):
    print()
    title = 'NUMBER OF ORDERS PER 60 min FOR DAY ' + str(nday)
    print(format(title, ' ^60'))
    print()
    i = 0
    for summary in summaries:
        label = labelString(i, interval=interval)
        print(format(label, ' >15'), end=' | ')
        order_num = summary[nday - 1]
        print('*' * order_num)
        i += 1
    print()

def main():
    days = get_input('How many days would you like to include?')
    interval = get_input('Please specify the length of the time interval in minutes:')
    summaries = composeOrderMatrix(days)
    printOrderSummaryMatrix(summaries, interval)
    nday = 0
    while nday != -1:
        nday = get_input('Enter day number from 1 to ' + str(days) +' to see a histogram, or -1 to exit:')
        if 1 <= nday <= days:
            printHistogram(summaries, nday, interval)

main()