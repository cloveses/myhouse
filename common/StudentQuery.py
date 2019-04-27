import os
import math

def get_datas():
    filename = None
    while True:
        filename = input('Please enter filename:')
        if not filename.strip():
            print('Filename is empty!')
            continue
        if not os.path.exists(filename):
            print('File is not exists!')
            continue
        break
    try:
        with open(filename) as f:
            datas = []
            while True:
                headers = f.readline().strip().split('\t')
                if headers:
                    break
            for line in f.readlines():
                row_datas = {}
                if line.strip():
                    row = line.strip().split('\t')
                    for k,v in zip(headers, row):
                        row_datas[k] = v
                datas.append(row_datas)
            return headers,datas
    except Exception as e:
        print(e)

def display_all(headers, datas):
    if not datas:
        print('No datas!')
        return
    max_page = math.ceil(len(datas) / 10)
    page = 0
    page_num = 10
    while True:
        for header in headers:
            print(header, end='\t')
        print()
        for row in datas[page * 10 : (page + 1) * 10]:
            for k in headers:
                print(row[k], end='\t')
            print()
        command = input('Continue(Enter) or Quit(Q)?')
        if command.strip().lower() == 'q':
            break
        page += 1
        if page >= max_page:
            break



def query_from_id(headers, datas):
    while True:
        ID = input('Please input a students\'s ID:').strip()
        if ID:
            break
    flag = True
    for data in datas:
        if data['ID'] == ID:
            flag = False
            for header in headers:
                print(header, ':\t', data[header])
    if flag:
        print('No data was finded!')

def query_from_lastname(headers, datas):
    while True:
        name = input('Please input a students\'s name:').strip()
        if name:
            break
    flag = True
    for data in datas:
        if data['Last'].lower().startswith(name.lower()):
            flag = False
            for header in headers:
                print(header, ':\t', data[header])
    if flag:
        print('No data was finded!')

def query_from_some_field(headers, datas):
    while True:
        print('All fields:', headers)
        field_name = input('Please input a students\'s field name:').strip()
        if field_name and field_name in headers:
            break
    while True:
        value = input('Please input a students\'s value:').strip().lower()
        if value:
            break
    for header in headers:
        print(header, end='\t')
    print()
    for data in datas:
        if data[field_name].lower() == value:
            for header in headers:
                print(data[header], end='\t')
            print()

def display_grad_year(headers, datas):
    while True:
        grad_year = input('Please input a students\'s GradYear:').strip()
        if grad_year and grad_year.isdigit():
            # grad_year = int(grad_year)
            break
    datas = [d for d in datas if d['GradYear'] == grad_year]
    # print(datas)
    display_all(headers, datas)

def count_one_year(headers, datas, grad_year):
    ret = {}
    for data in datas:
        if data['GradYear'] == grad_year:
            if data['DegreeProgram'] in ret:
                ret[data['DegreeProgram']] += 1
            else:
                ret[data['DegreeProgram']] = 1
    # print(ret)
    if ret:
        totals = sum(ret.values())
        for k,v in ret.items():
            print(k, ':', v, 'Percent:', v / totals * 100)
    else:
        print('No datas!')

def count_from_grad_year(headers, datas):
    while True:
        grad_year = input('Please input a students\'s GradYear:').strip()
        if grad_year and grad_year.isdigit():
            # grad_year = int(grad_year)
            break
    while True:
        on_after = input('Please Select On or After(On or Aft)? :').strip().lower()
        if on_after and on_after in ('on', 'aft'):
            break
    if on_after == 'on':
        count_one_year(headers, datas, grad_year)
    elif on_after == 'aft':
        max_year = 0
        for data in datas:
            if int(data['GradYear']) > max_year:
                max_year = int(data['GradYear'])
        if max_year < int(grad_year):
            print('No datas')
        else:
            for year in range(int(grad_year), max_year):
                count_one_year(headers, datas, grad_year)


def main():
    print('init from file ...')
    while True:
        datas = get_datas()
        if datas:
            break
    headers, studs = datas
    commands = {'list':display_all,'qid':query_from_id,
            'qlst':query_from_lastname, 'qfd':query_from_some_field,
            'qcgy': count_from_grad_year, 'dgy':display_grad_year}
    while True:
        print()
        print('-------------------------------')
        print('List all:(list); Query ID:(Qid); Query Last(Qlst); Query field(Qfd);\
            Count GradYear(Qcgy); display_grad_year(Dgy); Quit(Q)')
        print('-------------------------------')
        command = input('Input your command:').lower()
        print()
        if command == 'q':
            break
        if not command or command not in commands.keys():
            print('Bad command!')
            continue
        else:
            commands[command](headers, studs)
   

if __name__ == '__main__':
    main()
