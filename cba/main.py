import fileinput

stud_num = {}
stud_score = {}
class_not_pass = {}

for line in fileinput.input('score.txt'):
    datas = line.split(',')
    grade = datas[0][:2]
    stud_class = datas[-2]
    score = int(datas[-1])
    if grade in stud_num:
        stud_num[grade] += 1
    else:
        stud_num[grade] = 1
    if grade in stud_score:
        stud_score[grade] += score
    else:
        stud_score[grade] = score
    if score < 60:
        if stud_class in class_not_pass:
            class_not_pass[stud_class] += 1
        else:
            class_not_pass[stud_class] = 1
print(stud_num,stud_score,class_not_pass)