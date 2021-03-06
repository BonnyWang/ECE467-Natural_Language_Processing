import tensorflow as tf;
from tensorflow.keras.layers.experimental import preprocessing;

import numpy as np;
import os;
import time;

import json;


def main():

    # Create the dataSet from the json file
    perProcessData();

    text = open("./dataSet.txt", 'rb').read().decode(encoding='utf-8')

    vocab = sorted(set(text));
    

    # Process the text to inegers for training 
    ids_from_chars = preprocessing.StringLookup(vocabulary=list(vocab));

    # Parse the texts to ids
    all_ids = ids_from_chars(tf.strings.unicode_split(text, 'UTF-8'));

    # a reverse funciton to get characters from integers
    chars_from_ids = tf.keras.layers.experimental.preprocessing.StringLookup(
    vocabulary=ids_from_chars.get_vocabulary(), invert=True)

    # Convert the text vector into a stream of character indices
    ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids);
    
    # Create sequence for the input and target sets
    # First create the sets of sequences from the text
    seq_length = 100;
    sequences = ids_dataset.batch(seq_length+1, drop_remainder=True);

    # Create the dataset with input and target sequence pairs
    dataset = sequences.map(split_input_target);

    BATCH_SIZE = 64;

    BUFFER_SIZE = 10000;

    # Shuffle data and put them into batches
    dataset = (
        dataset
        .shuffle(BUFFER_SIZE)
        .batch(BATCH_SIZE, drop_remainder=True)
        .prefetch(tf.data.experimental.AUTOTUNE));

    # Length of the vocabulary in chars
    vocab_size = len(vocab);

    # The embedding dimension
    embedding_dim = 1024;

    # Number of RNN units
    rnn_units = 1024;

    model = MyModel(
    vocab_size=len(ids_from_chars.get_vocabulary()),
    embedding_dim=embedding_dim,
    rnn_units=rnn_units);

    # define the loss function
    loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True);

    model.compile(optimizer='adam', loss=loss);

    # define check points for saved paras
    checkpoint_dir = './training_checkpoints';
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}");

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True);
    
    EPOCHS = 20;

    # Execute training the model
    history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback]);

    print(model.summary());


    # Create model to produce next charactor
    one_step_model = OneStep(model, chars_from_ids, ids_from_chars);

    states = None;
    next_char = tf.constant(['title:']);
    result = [next_char];

    # Genereate texts one char by one
    for n in range(1000):
      next_char, states = one_step_model.generate_one_step(next_char, states=states);
      result.append(next_char);

    result = tf.strings.join(result);
    print(result[0].numpy().decode('utf-8'), '\n\n' + '_'*80);


def perProcessData():
  
  # Clean the data from json format to more natrual  format
  
  path_to_file = ["./poet.tang.0.json","poet.tang.1000.json","poet.tang.2000.json","poet.tang.3000.json"];
  outputDataSet =  open("dataSet.txt", "w",encoding="utf-8");
  
  for file in path_to_file:
   
    with open(file,  encoding='utf-8') as json_file:
      data = json.load(json_file)
   
    for p in data:
      outputDataSet.write("title:"+ str(p['title']) + "\n");
      outputDataSet.write("authors:"+ p['author']+ "\n");
      outputDataSet.write("paragraphs:\n");
      
      for para in p['paragraphs']:
        outputDataSet.write(para+"\n"); 
      
      outputDataSet.write("\n");

  outputDataSet.close();

# Function to rejoin the text from the ids
def text_from_ids(ids):
  return tf.strings.reduce_join(chars_from_ids(ids), axis=-1);

# The input and the target text are differed by one shifted character
def split_input_target(sequence):
    input_text = sequence[:-1];
    target_text = sequence[1:];
    return input_text, target_text;


class MyModel(tf.keras.Model):
  def __init__(self, vocab_size, embedding_dim, rnn_units):
    super().__init__(self)
    self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
    self.gru = tf.keras.layers.GRU(rnn_units,
                                   return_sequences=True,
                                   return_state=True)
    self.dense = tf.keras.layers.Dense(vocab_size)

  def call(self, inputs, states=None, return_state=False, training=False):
    x = inputs
    x = self.embedding(x, training=training)
    if states is None:
      states = self.gru.get_initial_state(x)
    x, states = self.gru(x, initial_state=states, training=training)
    x = self.dense(x, training=training)

    if return_state:
      return x, states
    else:
      return x


class OneStep(tf.keras.Model):
  def __init__(self, model, chars_from_ids, ids_from_chars, temperature=1.0):
    super().__init__()
    self.temperature = temperature
    self.model = model
    self.chars_from_ids = chars_from_ids
    self.ids_from_chars = ids_from_chars

    
    skip_ids = self.ids_from_chars(['', '[UNK]'])[:, None]
    sparse_mask = tf.SparseTensor(
        values=[-float('inf')]*len(skip_ids),
        indices=skip_ids,
        dense_shape=[len(ids_from_chars.get_vocabulary())])
    self.prediction_mask = tf.sparse.to_dense(sparse_mask)

  @tf.function
  def generate_one_step(self, inputs, states=None):
  
    input_chars = tf.strings.unicode_split(inputs, 'UTF-8')
    input_ids = self.ids_from_chars(input_chars).to_tensor()

    
    predicted_logits, states = self.model(inputs=input_ids, states=states,
                                          return_state=True)

    predicted_logits = predicted_logits[:, -1, :]
    predicted_logits = predicted_logits/self.temperature
    # Apply the prediction mask: prevent "" or "[UNK]" from being generated.
    predicted_logits = predicted_logits + self.prediction_mask


    predicted_ids = tf.random.categorical(predicted_logits, num_samples=1)
    predicted_ids = tf.squeeze(predicted_ids, axis=-1)

    predicted_chars = self.chars_from_ids(predicted_ids)

    return predicted_chars, states

if __name__ == '__main__':
  main();