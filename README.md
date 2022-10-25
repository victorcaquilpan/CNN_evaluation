# CNN evaluation

This repository contains a set of experiments using CNN arquitectures to predict animal classes. Dataset used for this study consists in 5400 images provided by this [Kaggle page](https://www.kaggle.com/datasets/iamsouravbanerjee/animal-image-dataset-90-different-animals). This datasets has 90 different animal classes and some samples could be visualized in above. Despite real images had different sizes, for this study all images were resized to 300x300 size.

![Sample images](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/images/Sample%20images.PNG)

A standard setting was utilized to preprocess images and it was showed below. 

```
# Transformation
train_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.RandomHorizontalFlip(),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
```

A total of six different arquitectures were tested, which are described in the next table.

| Model         | Depth         | Number of parameters | G-Flops (efficiency) | Best accuracy | Best accuracy setting | Jupyter link |
| ------------- | ------------- |--------------------- |----------------|-----------------|-----------------------|--------------|          
| Basic CNN     | 5             |                      |    3.07          |     0.4389          ||[Basic CNN](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/code/basic_cnn.ipynb)|
| AlexNet       | 8             |                      |  1.39            |               |||
| GoogleNet     | 22            |                      |              |               |||
| Resnet34      | 35            |                      |              |               |||
| Resnet151     | 152           |                      |              |  |||
| MobileNet-v2  | 53            |                      |              | |||
