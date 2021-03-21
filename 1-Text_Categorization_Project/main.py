import nltk;
import math;
from collections import Counter;

# Get user inputs
name_Labeled = input("Please enter the name of the list of labeled training documents:");
name_Unlabeled = input("Please enter the name of the list of labeled training documents:");

# Get information for training
train_File = open(name_Labeled,"r");

lines = train_File.readlines();


# Create 
train_docs = {}; 
#{document : category}

train_categories = {}; 
#{catorgory: [document1, documeng2, ...]}

train_Doc_Tokens = {}
#{doc: {token: n}}

trian_Tokens = {}
#  whether tokens appear in all documents {tokens : n}

train_Doc_TFIDF = {}
#{doc : tf*idf}

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+');
stemmer = nltk.stem.SnowballStemmer('english');
lemmatizer = nltk;

n_TrainDoc = 0;

for line in lines:
    info = line.split();
    category_Name = info[1];
    doc_Path = info[0];
    train_docs[doc_Path] = category_Name;
    if category_Name not in train_categories:
        train_categories[category_Name] = [];
    train_categories[category_Name].append(doc_Path);

    # Use to Tokenizer and stemer to tokenize the document 
    text_Of_Document = open(doc_Path).read().lower();
    tokens = tokenizer.tokenize(text_Of_Document);
    tokens = [stemmer.stem(token) for token in tokens];
    freq_Tokens = dict(Counter(tokens));

    train_Doc_Tokens[doc_Path] = freq_Tokens;

    for token in freq_Tokens:
        if token in trian_Tokens:
            trian_Tokens[token] += 1;
        else:
            trian_Tokens[token] = 1;
    

#  Calculate the tf*idf value for each document
for doc in train_docs:
    
    tokens = trian_Tokens.keys();
    tfidf = [];

    for token in tokens:
        if token in train_Doc_Tokens[doc]:
            tf = math.log10(train_Doc_Tokens[doc][token] + 1);
            idf = math.log10(len(lines)/trian_Tokens[token]);
            tfidf.append(tf*idf);
        else:
            tfidf.append(0);
    train_Doc_TFIDF[doc] = tfidf;

for category in train_categories:
    

    if n_TrainDoc == 0:
        print(freq_Tokens);

    n_TrainDoc += 1;

