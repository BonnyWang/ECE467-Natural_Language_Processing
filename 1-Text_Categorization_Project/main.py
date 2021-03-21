import nltk;
from nltk.tokenize import RegexpTokenizer;

# Get user inputs
name_Labeled = input("Please enter the name of the list of labeled training documents:");
name_Unlabeled = input("Please enter the name of the list of labeled training documents:");

# Get information for training
train_File = open(name_Labeled,"r");

lines = train_File.readlines();


# Create 
catorgories = [];

train_datas = {}; 
#{document : category}

train_categories = {}; 
#{catorgory: [document1, documeng2, ...]}

tokenizer = RegexpTokenizer(r'\w+');

n_TrainDoc = 0;

for line in lines:
    info = line.split();
    category_Name = info[1];
    doc_Path = info[0];
    train_datas[doc_Path] = category_Name;
    if category_Name not in train_categories:
        train_categories[category_Name] = [];
    train_categories[category_Name].append(doc_Path);

    # Use to Tokenizer to tokenize the document 
    text_Of_Document = open(doc_Path).read().lower();
    
    if n_TrainDoc == 0:
        print(text_Of_Document);

    n_TrainDoc += 1;

