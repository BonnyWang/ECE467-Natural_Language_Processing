# ECE467-Natural_Language_Processing
Course works for Cooper Union NLP Course
## Project 1: Text Categorization
### Instruction
In order to run the program, nltk and sklearn library is needed besides the standard library from python3.The following command can be used to install this library:
```
pip install -U nltk
pip install -U sklearn
```

To run the program, simply type py/python command and enter the name of the training, testing and output file name. A sequence of sample commands are shown below:

```
>>py main.py
Please enter the name of the list of labeled training documents:corpus1_train.labels
Training Completed!
Please enter the name of the list testing documents:corpus1_test.list
Finished predicting the category for documents!
Please enter the name of the output file:corpus1_predictions.labels
```

### Explanation
This project mainly used TF*IDF value to process the data. First, tokens are extracted from each document by the tokenizer and stemmer from nltk libaray. Then the TF*IDF value is calculated for each token in each document. By summing the TF*IDF from the all the documents in the same category, the weighted model is created. In addition, when calculating the term frequency, arbitrary weight of 1 is chosen, by experimenting, to be added for better performance.

The similarity between the predicting document and the weight matrix of tokens is measured by the cosine similarity metric, which is calculated by the dot product.

The second and third dataset is evaluated by separating part of the training data into the testing data.

The SVM with different kernels from the sklearn library is also experimented in this project. However, there is no significant advantage by using them from the results obtained. Therefore, they are not chosen for the ultimate version of the program.

Further experiments can be performed for this project. Naive Bayes method can be alternatively used for this project. More experimentation towards different tokenizer and tuning weights for specific tokens and categories may also improve the result. If the datasets get larger, machine learning methods include deep learning and neural networks might be cost effective. 

## Project 2: Parser
This program will prompt the user to enter a text file specifiying a CFG in Chomsky normal form.\
\
After inputing the grammar, user will allow to enter sentecese. All valid parses from the grammar will be displayed.

## Final Project: Chinese Poem Autogenerator
### Dataset Used
From https://github.com/chinese-poetry/chinese-poetry

In the JSON folder:

Poet.tang.0.json 
Poet.tang.1000.json
Poet.tang.2000.json
Poet.tang.3000.json   

Are arbitrarily selected to be the datasets of the project.

### Architecture
RNN with GRU is chosen for this project.

Compared to LSTM, GRU has fewer parameters and thus is easier for training. Based on the size of data and the limit of the training environment, GRU is chosen for its computational efficiency.

GRU also prevents the vanishing gradient problem in traditional RNN.

The input layer of the project is the word embedding. The GRU layer is in between the input and the output layer. The output layer will produce the log likelihood of all the unique characters and the one with maximum possibility will be chosen to be appended to the result.

The size of the input layer is 1*5129(the size of the vocab), same as the output layer. The size of the GRU layer should be 64 since the batch size is 64.

The word embedding dimension is chosen to be 1024 to create a more sparse matrix since there are much more unique characters in Chinese(compared to English).

Epoch 20 is chosen to produce good results. The loss value has a clear reduction after each epoch. However, it does have the cost of long running time.(Since I have a rtx2060 on my laptop, the training time is reasonable. It could take much longer on other machines without GPU acceleration). In addition, by experimenting, the loss value is below 2 after 16 epochs, below 1 after 26 epochs, below 0.5 after 32 epoches and around 0.2 after 40 epochs.

### Sample Output
title:橫吹曲辭 巫山高\
authors:杜甫\
paragraphs:\
幽州意氣箕山坂，戰子三蕃阻鼠鞭。\
躍壁月中不改，金事不齊身。\
草木相微滿畫堂，繡蒿金縷繡林塘。\
琱青綺閣揖如已，一時榮落自君心。\
專詔燕樓崇已識，城梁和洗絕氛租。


title:白雪寄王師秋夜懷徐公挽歌詞二首 二\
authors:李賀\
paragraphs:\
九月笙歌鼓吹笙，蝶動風竿過上驄。\
蹌纖塵霧兮兩殷獨感，不同歲李之明驕。\
半月羅輪起曉天，明月明珠照耀雲。\
歌宛轉歌崔玉幣，河山桂族垂雲湖。\
小姬塞口入張舍，玉檻浮雲臥未央。

title:橫吹曲辭 驄馬千堆\
authors:郭震\
paragraphs:\
隴火無氣色，山空髮盤乾。\
深沈不可巡，知食不能聽。\

title:相和歌辭 大歌辭 鳳吹曲\
authors:沈佺期\
paragraphs:張說\
paragraphs:\
鴛鴦夜白水驚碧，噴潤清笳簇金樞。\
綺房鶴容如不息，幽源今萬旗列出。
