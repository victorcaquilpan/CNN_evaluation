# CNN evaluation

This repository contains a set of experiments using CNN arquitectures to predict animal classes. Dataset used for this study consists in **5400** images provided by this [Kaggle page](https://www.kaggle.com/datasets/iamsouravbanerjee/animal-image-dataset-90-different-animals). This datasets has 90 different animal classes and some samples could be visualized in above. Despite real images had different sizes, for this study all images were resized to 300x300 size.

![Sample images](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/images/Sample%20images.PNG)

A standard setting was utilized to preprocess images and it was showed below. For running each Jupyter notebook, Google Colab was used taking the chance to use GPU. 

```
# Transformations applied
train_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.RandomHorizontalFlip(),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
```

```
# Dataset size
train_size = 4590
val_size = 270
test_size = 540

# General setup
loss_function = cross-entropy
batch_size = 12
number_epochs = 20
```

Six different arquitectures were tested combined with different setting of learning rates (0.1 and 0.001) and optimizers (SGD and Adam), and even considering cases with and without transfer learning (pretrained model) turning out in 44 trials. Top-1 accuracy and GFlops are shown as results. Estimation of GFlops is given by a code from this [Github repository](https://github.com/JJBOY/FLOPs). Moreover, it was tested cases with and without transfer learning. The best cases for each arquitecture are described in the next table.

| Model         | Depth          | G-Flops (efficiency) | Best accuracy (%)| Best accuracy setting | Jupyter link |
| ------------- | ------------- |----------------|-----------------|-----------------------|--------------|          
| Basic CNN     | 5                                |    3.07          |     43.89          |Optimizer: SGD + Lr: 0.001|[Basic CNN](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/code/basic_cnn.ipynb)
| AlexNet       | 8                                   |  1.39            | 75.19          |Optimizer: SGD + Lr: 0.001 + pretrained | [AlexNet](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/code/alexnet.ipynb)|
| GoogLeNet     | 22                                |2.97              |       91.85        |Optimizer: SGD + Lr: 0.001 + pretrained|[GoogLeNet](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/code/googlenet.ipynb)|
| Resnet34      | 35                                 |    7.28        | 93.70              |Optimizer: SGD + Lr: 0.001 + pretrained|[Resnet34](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/code/resnet34.ipynb) |
| Resnet101     | 102                                | 15.61              |95.00  |Optimizer: SGD + Lr: 0.001 + pretrained|[Resnet101](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/code/resnet101.ipynb)|
| MobileNet-v2  | 53                                 | 0.6             |87.78 |Optimizer: SGD + Lr: 0.001 + pretrained |[MobileNet-v2](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/code/mobilenetv2.ipynb)|
