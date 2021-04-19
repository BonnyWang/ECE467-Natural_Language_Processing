import sys;

cnfNounTerminals = {};
# Key = A Value = [[B,C],[C,D],...]

cnfRevTerminals = {};
# Key = w Value = [A,B,C]

cnfRevNounTerminals = {}
# key = B Value = {A1, A2, A3}

validNodeHead = [];

# Use to create the parse tree
class Node:
    def __init__(self, data):

        self.left = None;
        self.right = None;
        self.data = data;

# Print the bracketed notation
def printBracketed(node):
    if node.right == None:
        result = "["+ node.data +" "+ node.left +"]"
    else:
        result = "["+ node.data +" "+ printBracketed(node.left) +" "+ printBracketed(node.right) +"]"
    return result

# Print the Textual Parse Tree
def printTextualTree(node, level = 1):
    level = level;
    if node.right == None:
        result = "["+ node.data +" "+ node.left +"]\n";
    else:
        result = "["+ node.data +"\n" + "   "*level+ printTextualTree(node.left, level+1)+ level*"   " + printTextualTree(node.right, level+1) +(level-1)*"   "+ "]\n";
    return result

# Determine the word is terminal or not 
def terminal(word):
    if word[0].isupper() or word.startswith("_"):
        return False;
    else:
        return True;

def loadGrammar(lines):
    for line in lines:
        # Ignore comment lines
        if not line.startswith("#"):
            words = line.split();
            
            # Check whether the cnf is A--> B C or A --> w
            if terminal(words[2]):
                if words[2] in cnfRevTerminals.keys():
                    cnfRevTerminals[words[2]].add(words[0]);
                else:
                    cnfRevTerminals[words[2]] = {words[0]};
            else:
                # Load noun terminals
                if words[0] in cnfNounTerminals.keys():
                    cnfNounTerminals[words[0]].append([words[2], words[3]]);
                else:
                    cnfNounTerminals[words[0]] = [[words[2], words[3]]]; 
                # Create the possible end of rule for better searching 
                for w in [words[2], words[3]]:
                    if w in cnfRevNounTerminals.keys():
                            cnfRevNounTerminals[w].add(words[0]);
                    else:
                        cnfRevNounTerminals[w] = {words[0]};

# Use CKY Algorithm to parse the sentence
def parseSentence(sentence):
    tokens = sentence.split();
    n = len(tokens);

    # Initialize for each sentence
    nValid = 0;
    validNodeHead.clear();
   
    #create a matrix
    matrix = [[ [] for i in range(n+1) ] for j in range(n+1)]; 

    for j in range(1,n+1):
        if tokens[j-1] in cnfRevTerminals.keys():
            # Fill the diagonal of the matrix
            for t in cnfRevTerminals[tokens[j-1]]:
                mnode = Node(t);
                mnode.left = tokens[j-1]
                matrix[j-1][j].append(mnode);
      
        for i in range(j-2, -1,-1):
            for k in range(i+1, j):
                # iterate each entry
                for entry1 in matrix[i][k]:
                    for entry2 in matrix[k][j]:
                       
                        # check if the two nounterminal is in the list of all nounterminals
                        if entry1.data in cnfRevNounTerminals.keys() and entry2.data in cnfRevNounTerminals.keys():
                            
                            # find the possible rule by intersection
                            posibleNode =list(set(cnfRevNounTerminals[entry1.data]) & set(cnfRevNounTerminals[entry2.data]));
                            if len(posibleNode)!= 0:
                                
                                for node in posibleNode:
                                    if [entry1.data,entry2.data] in cnfNounTerminals[node]:
                                        tempNode = Node(node);
                                        tempNode.left = entry1;
                                        tempNode.right = entry2;
                                        matrix[i][j].append(tempNode);
                                        # A valid parse if found
                                        if node == 'S' and i == 0 and j == n:
                                            nValid = nValid + 1;
                                            validNodeHead.append(tempNode);
    return nValid;

def getSentence():
    textualDisplay = True if input("Do you want textual parse trees to be displayed (y/n)?:") == 'y' else False;
    while True:
        sentence = input("Enter a sentence: ");
        if sentence == 'quit':
            print("Goodbye!");
            sys.exit(0);
        else:
            nValid = parseSentence(sentence);
            if not nValid:
                print("NO VALID PARSES");
            else:
                print("VALID SENTENCE\n");
                for i in range(0, nValid):
                    print("Valid parse #" + str(i+1) + ":");
                    print(printBracketed(validNodeHead[i]));
                    if textualDisplay:
                        print("\n"+ printTextualTree(validNodeHead[i]));
                print("\nNumber of valid parses: " + str(nValid));


def main():
    # Get the name of the file from the command line
    cnfFileName = sys.argv[1];
    cnfFile = open(cnfFileName,"r");
    lines = cnfFile.readlines();

    print("Loading grammar...");
    loadGrammar(lines);

    getSentence();

if __name__ == '__main__':
    main();
