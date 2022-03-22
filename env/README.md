

## Getting started

### Cloning the repo

In a folder of your choice. clone from repo the materials needed. It will create a new subdirectory:
```bash
git clone git@github.com:eeroolli/SalsaAnnotation.git
cd SalsaAnnotation
```

### Creating the environment
In oder to have a reproducible results first you need create an environment.   
```bash
# Create environment for running the model in: 
git clone https://github.com/eeroolli/SalsaAnnotation.git
cd SalsaAnnotation
conda create --name testing_salsa python=3.8
conda activate testing_salsa
pip install -r requirements.txt 


```
## The Notebooks
The code is in partly in IPython Notebooks in order to run OpenPose in Google Colab and partly in Python 3.8.  
OpenPose, which is a pretrained model that we use for posedetection, needs to be built. If you use Colab the notebook will build it before doing the posedetection.  If you are not using Colab, you probably need to build it yourself. 



