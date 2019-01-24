txt = '''
As your program gets longer, you may want to split it into several files for easier maintenance.

'''

words = txt.split(' ')
for index,word in enumerate(words):
    if 'l' in word:
        print(word)
        reply = input('是否纠正(y或回车)：')
        if reply.lower() == 'y':
            words[index] = word.replace('l','i')
print(' '.join(words))