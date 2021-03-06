"FIZZBUZZ NET using PyTorch"

#IMPORTING LIBRARIES
import torch
import numpy as np
from torch import nn
import torch.nn.functional as F
from torch import optim
from sklearn.preprocessing import LabelEncoder
from sklearn import utils
from sklearn import metrics

def binary_encoder(input_size,number):
  """Given a number, it returns the Binary Digit notation of it"""
  ret = [int(i) for i in '{0:b}'.format(number)]
  return [0] * (input_size - len(ret)) + ret 

def fizzbuzz(x):
  """The function we are trying to learn"""
  if x%15 == 0:
    return 'fizzbuzz'
  elif x%3 == 0:
    return 'fizz'
  elif x%5 == 0:
    return 'buzz'
  return ''

def build_dataset(input_size = 10, limit = 1000):
  """ The function that builds the dataset, appending FizzBuzz labels and inputs to dataset"""
  X = []
  y = []
  for i in range(limit):
    X.append(binary_encoder(input_size=10,number=i))
    y.append(fizzbuzz(i))
  return X,y

class FizzBuzz(nn.Module):
  #BUILDING ARCHITECTURE
  """ 
  3 layer network for predicting Fizz or Buzz
  param: input_size -> int
  param: output_size -> int
  """
  """ Input ---> FC(ReLU) ---> FC(ReLU) ---> Softmax"""

  def __init__(self,input_size,hidden_size1,hidden_size2,output_size):
    super(FizzBuzz,self).__init__()
    self.hidden1 = nn.Linear(input_size,hidden_size1)
    self.hidden2 = nn.Linear(hidden_size1,hidden_size2)
    self.out = nn.Linear(hidden_size2,output_size) 

  def forward(self,batch):
    hid1 = F.relu(self.hidden1(batch))
    hid2 = F.relu(self.hidden2(hid1))
    out = self.out(hid2)

    return out

ceil = lambda x: int(np.ceil(x))      #Ceiling for Upper Limit

def trainer(
    model:nn.Module,
    X:torch.Tensor,
    y:torch.Tensor,
    n_epochs:int,
    batch_size:int,
    validation_frac:float,
    log_every:int):
  
  """
  The function that trains model with listed hyperparams
  """
  val_samples = ceil(X.shape[0] * validation_frac)
  trn_samples = X.shape[0] - val_samples
  #n_batches = ceil(trn_samples / batch_size)

  #CREATING VALIDATION AND TRAINING SET
  X_val = X[:val_samples]
  y_val = y[:val_samples]
  X_trn = X[val_samples:]
  y_trn = y[val_samples:]

  for epoch in range(1,n_epochs+1):
    epoch_loss=0
    for start in range(0,len(X_trn),batch_size):
      end = start+batch_size
      batchX = X_trn[start:end]
      batchy = y_trn[start:end]

      model.zero_grad()
      y_pred = model(X_trn)
      loss = loss_fn(y_pred,y_trn)

      loss.backward()
      optimizer.step()

      epoch_loss += loss.item()

    if epoch%log_every ==0:
      predictions = model(X_trn).argmax(-1)
      trn_accu = metrics.accuracy_score(predictions,y_trn)

      predictions = model(X_val).argmax(-1)
      val_accuracy = metrics.accuracy_score(predictions, y_val)
      print('Epoch %4d train loss: %4.4f train accuracy %4.4f valid. accuracy %4.4f' % (epoch, epoch_loss, trn_accu, val_accuracy))

#MODEL HYPERPARAMETERS
hidden_size = 20
n_labels = 4
n_bits = 10
epochs = 10000
batch_size = 32
learning_rate = 0.01

#BUILDING DATASET
X,y = build_dataset()
encoder = LabelEncoder()
y = encoder.fit_transform(y)

#THE MODEL
model = FizzBuzz(n_bits,hidden_size,hidden_size,n_labels)
optimizer = optim.SGD(model.parameters(),lr=learning_rate)
loss_fn = nn.CrossEntropyLoss()


# training
X = torch.tensor(X, dtype=torch.float32)
y = torch.from_numpy(y)

trainer(model, n_epochs=epochs, batch_size=batch_size, X=X, y=y, validation_frac=0.2, log_every=1000)

#TESTING

X_tst,y_tst = build_dataset(input_size=10,limit=100)
X_tst = torch.tensor(X_tst,dtype=torch.float32)
y_tst = encoder.transform(y_tst)

model.eval()
y_hat = model(X_tst).argmax(-1)
acc = metrics.accuracy_score(y_hat,y_tst)
print("Test Accuracy: ", acc)



