# This script installs resources that are needed, and not successfully
# installed in to the environment by the requirements.txt

python3 -m venv salsa-env
source salsa-env/bin/activate
!sudo apt install ffmpeg

# if you do not want to use the script you can run the following commands:
!conda config --append channels conda-forge
!conda install -c conda-forge jupyterlab
!conda install -c anaconda ipykernel
!conda install plotly
# some people need: sudo apt install python3-pip
!python -m ipykernel install --user --name Team3 --display-name Team3
!pip install --upgrade pip
!pip install opencv-python
!pip install tensorflow
!pip install tensorboard
!pip install -r requirements.txt


