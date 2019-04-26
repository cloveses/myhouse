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
    max_page = math.ceil(len(datas) / 10)
    page = 0
    page_num = 10
    while True:
        for header in headers:
            print(header, end='\t')
        print()
        for i in range(page * 10 , (page + 1) * 10):
            for k in headers:
                row = datas[i]
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

def count_from_grad_year(headers, datas):
    while True:
        grad_year = input('Please input a students\'s GradYear:').strip()
        if grad_year and grad_year.isdigit():
            grad_year = int(grad_year)
            break
    sum = 0
    for data in datas:
        if int(data['GradYear']) <= grad_year:
            sum += 1
    print('Graduating on/after', grad_year, ':', sum)
    percent = sum / len(datas) * 100
    print('Graduating on/after Percent:', percent, '%')

def main():
    print('init from file ...')
    while True:
        datas = get_datas()
        if datas:
            break
    headers, studs = datas
    commands = {'list':display_all,'qid':query_from_id,
            'qlst':query_from_lastname, 'qfd':query_from_some_field, 'qcgy': count_from_grad_year}
    while True:
        print()
        print('-------------------------------')
        print('List all:(list); Query ID:(Qid); Query Last(Qlst); Query field(Qfd);\
            Count GradYear(Qcgy); Quit(Q)')
        print('-------------------------------')
        command = input('Input your command:').lower()
        if command == 'q':
            break
        if not command or command not in commands.keys():
            print('Bad command!')
            continue
        else:
            commands[command](headers, studs)
   

if __name__ == '__main__':
    main()
