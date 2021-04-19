import sys;

cnfTerminals = {};
# Key = A Value = [[B,C],[C,D],...]

cnfNounTerminals = {};
# Key = A Value = [w1, w2, w3,...]

def terminal(word):
    if word[0].isupper() or word.startswith("_"):
        return False;
    else:
        return True;

def main():
    # Get the name of the file from the command line
    cnfFileName = sys.argv[1];

    cnfFile = open(cnfFileName,"r");
    lines = cnfFile.readlines();

    print("Loading grammar...");

    for line in lines:
        # Ignore comment lines
        if not line.startswith("#"):
            words = line.split();
            
            # Check whether the cnf is A--> B C or A --> w
            if terminal(words[2]):
                if words[0] in cnfTerminals.keys():
                    cnfTerminals[words[0]].append(words[2]);
                else:
                    cnfTerminals[words[0]] = [words[2]];
            else:
                if words[0] in cnfNounTerminals.keys():
                    cnfNounTerminals[words[0]].append([words[2], words[3]]);
                else:
                    cnfNounTerminals[words[0]] = [[words[2], words[3]]]; 

    print(cnfTerminals);
    print(cnfNounTerminals);

    # while True:
    #     sentence = input();
    #     if sentence == 'quit':
    #         sys.exit(0);


    print("hi");


if __name__ == '__main__':
    main();
