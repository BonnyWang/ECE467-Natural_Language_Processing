import nltk;
import math;
import numpy;
from collections import Counter;

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+');
stemmer = nltk.stem.SnowballStemmer('english');

###########################################
# Functions for processing 

def getTokens(lines, document_Category, category_Document, doc_Tokens, allTokens):
    for line in lines:
        info = line.split();
        if(len(info) > 1):
            category_Name = info[1];
        else:
            category_Name = '';
        doc_Path = info[0];
        document_Category[doc_Path] = category_Name;
        if category_Name not in category_Document:
            category_Document[category_Name] = [];
        
        # Create the categroy with following documents name
        category_Document[category_Name].append(doc_Path);

        # Use to Tokenizer and stemer to tokenize the document 
        text_Of_Document = open(doc_Path).read().lower();
        tokens = tokenizer.tokenize(text_Of_Document);
        tokens = [stemmer.stem(token) for token in tokens];
        token_Freqency = dict(Counter(tokens));

        doc_Tokens[doc_Path] = token_Freqency;


        for token in token_Freqency:
            if token in allTokens:
                allTokens[token] += 1;
            else:
                allTokens[token] = 1;


# Calculate the tf*idf value for each document and for each category
def calculateTFIDF(documents,categories, allTokens, doc_Tokens, nDocument, doc_TFIDF):
    for doc in documents:
        tokens = allTokens.keys();
        tfidf = [];

        for token in tokens:
            if token in doc_Tokens[doc]:
                tf = doc_Tokens[doc][token]/ len(doc_Tokens[doc]);
                idf = math.log10(nDocument/allTokens[token]);
                tfidf.append(tf*idf);
            else:
                tfidf.append(0);
        doc_TFIDF[doc] = tfidf;

# Calculate the centroid value for each category
def calculateCentroid(categories, allTokens, doc_TFIDF, cat_TFIDF):
    for category in categories:
        sum_vec = [0]*len(allTokens);
        for document in categories[category]:
            sum_vec = [a+b for a,b in zip(sum_vec, doc_TFIDF[document])];
        
        cat_TFIDF[category] = [a/len(categories[category]) for a in sum_vec];      



###########################################
# The actual start of the program
# Get user inputs
name_Labeled = input("Please enter the name of the list of labeled training documents:");

# Get information for training
train_File = open(name_Labeled,"r");

train_Lines = train_File.readlines();

# Create necessary varaibles to hold the data
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

train_Cat_TFIDF = {}
#{Category: tf*idf}


getTokens(train_Lines, train_docs, train_categories, train_Doc_Tokens, trian_Tokens);
calculateTFIDF(train_docs,train_categories,trian_Tokens,train_Doc_Tokens,len(train_Lines),train_Doc_TFIDF);
calculateCentroid(train_categories,trian_Tokens,train_Doc_TFIDF,train_Cat_TFIDF);


print("Trainning Completed!");

# Start predicting the type of documents
name_Test = input("Please enter the name of the list testing documents:");

test_File = open(name_Test, "r");

test_Lines = test_File.readlines();


test_Doc_Tokens = {} 
# {Document: {token: n}}
test_Tokens = {} 
#{token: N}
test_Doc_Tfidf = {} 
#{Document: tf*idf}
test_Pred = {} 
# {Document: Predicted Category}

test_Doc = {};
test_Cat = {}


getTokens(test_Lines,test_Doc,test_Cat,test_Doc_Tokens,test_Tokens);
calculateTFIDF(test_Doc,test_Cat,trian_Tokens,test_Doc_Tokens,len(test_Doc),test_Doc_Tfidf);

for doc in test_Doc:
    doc_sim = []
    temp1 = numpy.array(test_Doc_Tfidf[doc])
    for cat in train_Cat_TFIDF:
        temp2 = numpy.array(train_Cat_TFIDF[cat])
        doc_sim.append(numpy.dot(temp1, temp2)/(numpy.linalg.norm(temp1)*numpy.linalg.norm(temp2)))
    test_Pred[doc] = list(train_Cat_TFIDF)[doc_sim.index(max(doc_sim))]

print(test_Pred);

output_Name = input('Please enter the name of the output file:');
out_File = open(output_Name, "w")
for doc in test_Pred:
    out_File.write(doc + " " + test_Pred[doc] + '\n')
