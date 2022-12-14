# -*- coding: utf-8 -*-
"""cnn_functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jKwQLyQKnuY-Gs3_PVz-JMielP11Bwxm
"""

# cnn_functions.py

# Loading packages
import os
from torchvision import transforms 
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import random_split
from torchvision.utils import make_grid
from torch.utils.data.dataloader import DataLoader
import torch.optim as optim
import random
from tqdm.notebook import tqdm
import numpy as np
import warnings

# Add some function to check if GPU is available and use it
def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return None
    
def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)

# Plotting performance
def plot_performance(performance_training,performance_validation,metric = 'acc_loss'):
  if metric == 'acc_loss':
    #  Get metrics
    accuracy_train = [values[0].cpu() for values in performance_training]
    accuracy_val = [values[0].cpu() for values in performance_validation]
    loss_train = [values[1] for values in performance_training]
    loss_val = [values[1].cpu() for values in performance_validation]
    # Create plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 5))
    ax[0].plot(accuracy_train,'-x', label='train accuracy')
    ax[0].plot(accuracy_val,'-o',label='val accuracy')
    ax[0].set_title('Accuracy performance over epochs')
    ax[0].set_ylabel('Accuracy')
    ax[0].set_xlabel('N epochs')
    ax[0].legend()
    ax[1].plot(loss_train,'-x', label='train loss')
    ax[1].plot(loss_val,'-o',label='val loss')
    ax[1].set_title('Loss function over epochs')
    ax[1].set_ylabel('Loss value')
    ax[1].set_xlabel('N epochs')
    ax[1].legend()
    plt.show()

  elif metric == 'acc':
    accuracy_train = [values[0].cpu() for values in performance_training]
    accuracy_val = [values[0].cpu() for values in performance_validation]
    plt.plot(accuracy_val, '-x')
    plt.plot(accuracy_train, '-o')
    plt.title('Accuracy performance over epochs')
    plt.xlabel('N epoch')
    plt.ylabel('Accuracy')

  elif metric == 'loss':
    loss_train = [values[1] for values in performance_training]
    loss_val = [values[1].cpu() for values in performance_validation]
    plt.plot(accuracy_val, '-x')
    plt.plot(accuracy_train, '-o')
    plt.title('Loss function over epochs')
    plt.xlabel('N epoch')
    plt.ylabel('Loss value')

# Creation of a  general function to run CNN models
def fit_model(model,train_loader = None, val_loader = None, test_loader = None,optimization = 'SGD',loss_function = 'Cross-entropy',epochs = 15,learning_rate = 0.01):
  # Create an instance of our model
  cnn_model =  model
  # Pass  our model to cuda if there is available
  if torch.cuda.is_available():
        cnn_model.cuda()
  # Create loss function
  if loss_function == 'Cross-entropy':
    def criterion(input,output):
      loss = F.cross_entropy(output,input)
      return loss
  elif loss_function == 'Negative-loglikelihood':
    def criterion(input,output):
      loss = F.nll_loss(output,input)
      return loss

  # Create optimizer
  if optimization == 'SGD':
    optimizer = optim.SGD(cnn_model.parameters(), lr=learning_rate, momentum=0.9)
  elif optimization =='Adam':
    optimizer = optim.Adam(cnn_model.parameters(),lr = learning_rate)

  # Create complementary functions
    # Define an accuracy function
  def accuracy_val(output,target):
    with torch.no_grad():
      batch_size = target.size(0)
      _, pred = torch.topk(output,1)
      pred = pred.t()
      correct = (pred == target.unsqueeze(dim=0)).expand_as(pred)
      return correct.sum()/target.size(0)

  # We define a validation step function
  def validation_step(model,batch):
      images, labels = batch 
      # Generate predictions
      outputs = model(images)
      if type(outputs).__name__ == 'GoogLeNetOutputs':
        outputs = outputs.logits
      # Getting the prediction
      _, preds = torch.topk(outputs,1)         
      # Calculate loss
      loss = criterion(labels,outputs)
      # Calculate accuracy  
      acc = accuracy_val(outputs, labels)      
      return {'val_loss': loss.detach(), 'val_acc': acc,'prediction': preds}

  # Create a function to evalue new data
  @torch.no_grad()
  def evaluate(model,val_loader):
    model.eval()
    outputs = [validation_step(model,batch) for batch in val_loader]
    predictions_eval = [pred['prediction'] for pred in outputs]
    predictions_eval = [predictions[0].cpu().numpy() for predictions in predictions_eval]
    predictions = np.hstack(predictions_eval)
    return [sum([accur['val_acc'] for accur in outputs])/len(outputs),sum([accur['val_loss'] for accur in outputs])/len(outputs),predictions]

  # Create a function to evalue new data
  @torch.no_grad()
  def evaluate_test(model,test_loader):
    model.eval()
    outputs = [validation_step(model,batch) for batch in test_loader]
    return [sum([accur['val_acc'] for accur in outputs])/len(outputs)]

  # Create a list where we can save accuracy and loss values of validation and 
  # training steps
  performance_values_val = []
  performance_values_train = []

  # Train model. Loop over the dataset multiple times
  for epoch in range(epochs):  
      # Set running loss to zero and accuracy to zero
      running_loss = 0.0
      running_accuracy = 0.0
      for batch in tqdm(train_loader):
          # Get the inputs; data is a list of [inputs, labels]
          inputs, labels = batch
          # Zero the parameter gradients
          optimizer.zero_grad()
          # Forward + backward + optimize
          cnn_model.train()
          outputs = cnn_model(inputs)
          # In case of GoogleNet, we have three outputs. We need to select only one
          class_model = type(outputs).__name__
          if class_model == 'GoogLeNetOutputs':
            outputs = outputs.logits
          # Getting accuracy 
          acc = accuracy_val(outputs, labels)
          running_accuracy += acc
          # Get loss function
          loss = criterion(labels,outputs)
          loss.backward()
          optimizer.step()
          # Accumulate loss cost through each batch
          running_loss += loss.item()
      # Get accuracy of training per epoch
      accuracy_train_per_epoch = running_accuracy/len(train_loader) 
      # Append accuracy values
      performance_values_train.append([accuracy_train_per_epoch,running_loss / len(train_loader)])
      # Print loss value per each epoch
      print(f'[loss in training]:{running_loss / len(train_loader):.3f}')
      # We can include a validation phase
      validation_result = evaluate(cnn_model, val_loader)
      # Append value of accuracy per each epoch
      performance_values_val.append(validation_result)
  # Try model in test data
  testing_result = evaluate_test(cnn_model, test_loader)
  print('Finished Training')
  return cnn_model, performance_values_train,performance_values_val,testing_result

# Now, we can add a code to count number of Flops.
# This code is available from 
# https://cloudstor.aarnet.edu.au/plus/s/PcSc67ZncTSQP0E 

warnings.filterwarnings("ignore")

def print_model_parm_flops(model, input, detail=False):
    list_conv = []

    def conv_hook(self, input, output):

        # batch_size, input_channels, input_time(ops) ,input_height, input_width = input[0].size()
        # output_channels,output_time(ops) , output_height, output_width = output[0].size()

        kernel_ops = (self.in_channels / self.groups) * 2 - 1  # add operations is one less to the mul operations
        for i in self.kernel_size:
            kernel_ops *= i
        bias_ops = 1 if self.bias is not None else 0

        params = kernel_ops + bias_ops
        flops = params * output[0].nelement()

        list_conv.append(flops)

    list_linear = []

    def linear_hook(self, input, output):
        weight_ops = (2 * self.in_features - 1) * output.nelement()
        bias_ops = self.bias.nelement()
        flops = weight_ops + bias_ops
        list_linear.append(flops)

    list_bn = []

    def bn_hook(self, input, output):
        # (x-x')/?? one sub op and one div op
        # and the shift ?? and ??
        list_bn.append(input[0].nelement() / input[0].size(0) * 4)

    list_relu = []

    def relu_hook(self, input, output):
        # every input's element need to cmp with 0
        list_relu.append(input[0].nelement() / input[0].size(0))

    list_pooling = []

    def max_pooling_hook(self, input, output):
        # batch_size, input_channels, input_height, input_width = input[0].size()
        # output_channels, output_height, output_width = output[0].size()

        # unlike conv ops. in pool layer ,if the kernel size is a int ,self.input will be a int,not a tuple.
        # so we need to deal with this problem
        if isinstance(self.kernel_size, tuple):
            kernel_ops = torch.prod(torch.Tensor([self.kernel_size]))
        else:
            kernel_ops = self.kernel_size * self.kernel_size
            if len(output[0].size()) > 3:  # 3D max pooling
                kernel_ops *= self.kernel_size
        flops = kernel_ops * output[0].nelement()
        list_pooling.append(flops)

    def avg_pooling_hook(self, input, output):
        # cmp to max pooling ,avg pooling has an additional sub op
        # unlike conv ops. in pool layer ,if the kernel size is a int ,self.input will be a int,not a tuple.
        # so we need to deal with this problem
        if isinstance(self.kernel_size, tuple):
            kernel_ops = torch.prod(torch.Tensor([self.kernel_size]))
        else:
            kernel_ops = self.kernel_size * self.kernel_size
            if len(output[0].size()) > 3:  # 3D  pooling
                kernel_ops *= self.kernel_size
        flops = (kernel_ops + 1) * output[0].nelement()
        list_pooling.append(flops)

    def adaavg_pooling_hook(self, input, output):
        kernel = torch.Tensor([*(input[0].shape[2:])]) // torch.Tensor(list((self.output_size,))).squeeze()
        kernel_ops = torch.prod(kernel)
        flops = (kernel_ops + 1) * output[0].nelement()
        list_pooling.append(flops)

    def adamax_pooling_hook(self, input, output):
        kernel = torch.Tensor([*(input[0].shape[2:])]) // torch.Tensor(list((self.output_size,))).squeeze()
        kernel_ops = torch.prod(kernel)
        flops = kernel_ops * output[0].nelement()
        list_pooling.append(flops)

    def foo(net):
        childrens = list(net.children())
        if not childrens:
            if isinstance(net, torch.nn.Conv2d) or isinstance(net, torch.nn.Conv3d):
                net.register_forward_hook(conv_hook)
            if isinstance(net, torch.nn.Linear):
                net.register_forward_hook(linear_hook)
            if isinstance(net, torch.nn.BatchNorm2d) or isinstance(net, torch.nn.BatchNorm3d):
                net.register_forward_hook(bn_hook)
            if isinstance(net, torch.nn.ReLU):
                net.register_forward_hook(relu_hook)
            if isinstance(net, torch.nn.MaxPool2d) or isinstance(net, torch.nn.MaxPool3d):
                net.register_forward_hook(max_pooling_hook)
            if isinstance(net, torch.nn.AvgPool2d) or isinstance(net, torch.nn.AvgPool3d):
                net.register_forward_hook(avg_pooling_hook)
            if isinstance(net, torch.nn.AdaptiveAvgPool2d) or isinstance(net, torch.nn.AdaptiveAvgPool3d):
                net.register_forward_hook(adaavg_pooling_hook)
            if isinstance(net, torch.nn.AdaptiveMaxPool2d) or isinstance(net, torch.nn.AdaptiveMaxPool3d):
                net.register_forward_hook(adamax_pooling_hook)
            return
        for c in childrens:
            foo(c)

    foo(model)
    out = model(input)
    total_flops = sum(list_conv) + sum(list_linear) + sum(list_bn) + sum(list_relu) + sum(list_pooling)
    print(' + Number of FLOPs: %.2fG' % (total_flops / 1e9))

    # if detail:
    #     print('  + Conv FLOPs: %.2fG' % (sum(list_conv) / 1e9))
    #     print('  + Linear FLOPs: %.2fG' % (sum(list_linear) / 1e9))
    #     print('  + Batch Norm FLOPs: %.2fG' % (sum(list_bn) / 1e9))
    #     print('  + Relu FLOPs: %.2fG' % (sum(list_relu) / 1e9))
    #     print('  + Pooling FLOPs: %.2fG' % (sum(list_pooling) / 1e9))

 
