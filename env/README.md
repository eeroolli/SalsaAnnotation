

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
# replicate our environment for running the model: 
git clone https://github.com/eeroolli/SalsaAnnotation.git
cd SalsaAnnotation
conda create --name testing_salsa python=3.8
conda activate testing_salsa
pip install -r env/requirements.txt 
```
If you want to try using the latest versions of packages, you can change the last line above to:
```bash
pip install -r env/requirements_short.txt
```
But in that case, you better be prepared to edit the code.


## The Notebooks
The code is in partly in IPython Notebooks in order to run OpenPose in Google Colab and partly in Python 3.8.  
OpenPose, which is a pretrained model that we use for posedetection, needs to be built. If you use Colab the notebook will build it before doing the posedetection.  If you are not using Colab, you probably need to build it yourself. 

After we had the code working on Colab, we rewrote video processing, data processing, traning and validation and prediction to pure python. Some of the code is also running on Streamlit. 


