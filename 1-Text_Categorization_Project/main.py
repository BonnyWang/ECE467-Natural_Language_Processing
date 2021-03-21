import nltk;
import math;
import numpy;
import sklearn;
from collections import Counter;
from sklearn import svm;

tokenizer = nltk.tokenize.NLTKWordTokenizer();
stemmer = nltk.stem.RegexpStemmer('english');

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

        # Collect token appearance
        for token in token_Freqency:
            if token in allTokens:
                allTokens[token] += 1;
            else:
                allTokens[token] = 1;


# Calculate the tf*idf value for each document
def calculateTFIDF(documents,categories, allTokens, doc_Tokens, nDocument, doc_TFIDF):
    for doc in documents:
        tokens = allTokens.keys();
        tfidf = [];

        for token in tokens:
            if token in doc_Tokens[doc]:
                # plus one is chosen arbitarily to improve the performance and add more weight for appeared token
                tf = doc_Tokens[doc][token]/len(doc_Tokens[doc])+1;
                idf = math.log10(nDocument/allTokens[token]);
                tfidf.append(tf*idf);
            else:
                # So that they have the same size
                tfidf.append(0);
        doc_TFIDF[doc] = tfidf;


# Calculate the weigth value of each token for each category
def calculateWeight(categories, allTokens, doc_TFIDF, cat_TFIDF):
    for category in categories:
        weights = [0]*len(allTokens);
        for document in categories[category]:
            for i in range(0,len(weights)):
                # Summing all the weights for the same token
                weights[i] = weights[i]+doc_TFIDF[document][i];
        
        # Normalize the weight
        cat_TFIDF[category] = [weight/len(categories[category]) for weight in weights];      


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
#{doc : [tf*idf]}

train_Cat_TFIDF = {}
#{Category: [tf*idf]}


getTokens(train_Lines, train_docs, train_categories, train_Doc_Tokens, trian_Tokens);
calculateTFIDF(train_docs,train_categories,trian_Tokens,train_Doc_Tokens,len(train_Lines),train_Doc_TFIDF);
calculateWeight(train_categories,trian_Tokens,train_Doc_TFIDF,train_Cat_TFIDF);

#classifier = svm.SVC(kernel='linear');
#classifier.fit(numpy.array(list( train_Cat_TFIDF.values())),numpy.array(list( train_Cat_TFIDF.keys())));

print("Training Completed!");

# Start predicting the type of documents
name_Test = input("Please enter the name of the list testing documents:");

test_File = open(name_Test, "r");

test_Lines = test_File.readlines();

# Create necessay variables
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

# Prepare the documents for comaprison
getTokens(test_Lines,test_Doc,test_Cat,test_Doc_Tokens,test_Tokens);
calculateTFIDF(test_Doc,test_Cat,trian_Tokens,test_Doc_Tokens,len(test_Doc),test_Doc_Tfidf);

# test_Pred[doc] = classifier.predict(numpy.array(list(test_Doc_Tfidf[doc])).reshape(1,-1));

# Calculate the similarity and use the max value to predict the category
for doc in test_Doc:
    doc_Similarity = [];
    d = numpy.array(test_Doc_Tfidf[doc]);
    for cat in train_Cat_TFIDF:
        c = numpy.array(train_Cat_TFIDF[cat]);

        # the cosine value is the same as dot product/ norms
        doc_Similarity.append(numpy.dot(d, c)/(numpy.linalg.norm(d)*numpy.linalg.norm(c)))
    
    # Choose the categroy with the largest similarity value
    test_Pred[doc] = list(train_Cat_TFIDF)[doc_Similarity.index(max(doc_Similarity))]

print('Finished predicting the category for documents!');


output_Name = input('Please enter the name of the output file:');

# Write result to the output file
out_File = open(output_Name, "w")
for doc in test_Pred:
    out_File.write(doc + " " + test_Pred[doc] + '\n')