

texts = []

def clear(word):
    

with open('THE TRAGEDY OF ROMEO AND JULIET.txt', 'r') as f:
    for line in f.readlines():
        words = line.strip().split()
        words = [w.lower() for w in words if w]
        texts.extend(words)


print(texts[:10])

