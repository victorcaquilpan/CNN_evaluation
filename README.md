# CNN evaluation

This repository contains a set of experiments using CNN arquitectures to predict animal classes. Dataset used for this study consists in 5400 images provided by this [Kaggle page](https://www.kaggle.com/datasets/iamsouravbanerjee/animal-image-dataset-90-different-animals). This datasets has 90 different animal classes and some samples could be visualized in above. Despite real images had different sizes, for this study all images were resized to 300x300 size.

![Sample images](https://github.com/victorcaquilpan/CNN_evaluation/blob/main/images/Sample%20images.PNG)

Six different arquitectures were tested, which are described in the next table.

| Model         | Depth         | Number of parameters |  Best accuracy | Best Efficiency | Best accuracy setting | Jupyter link |
| ------------- | ------------- |--------------------- |----------------|-----------------|-----------------------|--------------|          
| Basic CNN     | 5             |                      |              |               |||
| AlexNet       | 8             |                      |              |               |||
| GoogleNet     | 22            |                      |              |               |||
| Resnet34      | 35            |                      |              |               |||
| Resnet151     | 152           |                      |              |  |||
| MobileNet-v2  | 53            |                      |              | |||
