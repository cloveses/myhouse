# coding:utf-8


def insertion_sort(numbers):
    for i in range(1,len(numbers)):
        num = numbers[i]
        for j in range(i-1,-1,-1):
            if numbers[j] > num:
                numbers[j+1] = numbers[j]
                numbers[j] = num
            else:
                break
    print(numbers)


if __name__ == '__main__':
    insertion_sort([2,5,7,3,1,9,0])
