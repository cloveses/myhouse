from task7 import Freq

freq = Freq()
freq.add_file('./Ebooks/98-0.txt')
freq.add_file('./Ebooks/1342-0.txt')
freq.add_file('./Ebooks/2600-0.txt')
print(freq.evaluate_frequency('./Ebooks/84-0.txt'))
