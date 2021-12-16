

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
conda create --name SalsaAnn python=3.8

# Use environment
conda activate SalsaAnn

```

# install packages
A machine learning model depents on a number of packages.   You have two choices. Either run a script or manually install the packages using commands below. 

```bash
# This script will install the needed packages:
bash inside_env_install_packages.sh
``` 
or

```bash
# if you do not want to use the script you can run the following commands:
conda config --append channels conda-forge
conda install -c conda-forge jupyterlab
conda install -c anaconda ipykernel
conda install plotly
# some people need: sudo apt install python3-pip
python -m ipykernel install --user --name Team3 --display-name Team3
pip install --upgrade pip
pip install -r requirements.txt
```

# Unpack the data


```
## The Notebooks
The code is in partly in IPython Notebooks in order to run OpenPose in Google Colab and partly in Python 3.8.  OpenPose, which is a pretrained model that we use for posedetection, needs to be built. If you use Colab the notebook will build it before doing the posedetection.  If you are not using Colab, you need to build yourself. 


## Help
For more help and information, please consult the 

