import nltk

with open('text.txt','r') as src_file:
    texts = src_file.readlines()
texts = [text.lower() for text in texts]

all_tokens = [token for tweet in texts for token in nltk.word_tokenize(tweet)]
# print(all_tokens)

nltk_stopwords = nltk.corpus.stopwords.words('english')

fstop = open('stopwords.txt', 'r')
stoptext = fstop.read()
stopwords = stoptext.split()
stopwords.extend(nltk_stopwords)
all_tokens = [t for t in all_tokens if t not in stopwords and t.isalpha()]

res = nltk.FreqDist(all_tokens)
top_words = res.most_common(30)

for w,f in top_words:
    print(w,f)

texts = [
'Celebrate #NationalPetDay with our puppy playlist: https://t.co/eBHHFPW0z7 https://t.co/uix5AY2FFQ',
"""<a href="http://msande.stanford.edu"> Management Science and Engineering </a>
<p class="MsoNormal">
      Address: Terman 311, Stanford CA 94305<br>
      Email: ashishg@cs.stanford.edu<br>
      Phone: (650)814-9999 [Cell], Fax: (650)723-9999<br>
      Admin asst: Roz Morf, Terman 405, 650-723-9999, rozm@stanford.edu</p>
""",
"""The U.S.A. olympic teams have east-west training centers with up-to-date equipment."""
]

re_url = r''
re_phone = r'\d{3}-\d{8}|\d{4}-\d{7}'
re_email = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
re_hyphen = ''
re_acronyms = ''