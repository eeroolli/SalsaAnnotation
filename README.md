# Salsa Annotation

In this project we will create annotations/labels for cuban salsa videos using deep learning models. Salsa is a couple dance where movement patterns appear in counting of 4 steps.

We tried different sizes of elementary units and notation systems, and ended up with labelling the data with the kind of units that dancers are using too. So, our unit consists of elements that are as long the dancers counting 123-567- or two bars of music.  

The labeling problem and the unbalanced size of categories are solved by using a coreography where each dancer repeats each element twice, 
then turns 90-degrees so that the same choreography can be filmed from a different angle. We film in total of 4 different angles, so
each dancer repeats each figure a total of 8 times. 

We made a video with the choreography for the people who made us salsa videos.
https://drive.google.com/file/d/1tX5dczXymc4EjAB0A9-5mkPx-pvV412n/view?usp=sharing 

There is a FAQ for people making videos at http://salsa.eero.no 

## PreProcessing

The input data is videos from mobile phones.  In preprossing the videos are converted to same size and speed.  

The beginning of each unit/figure is manually marked with a mouse click. We are confident that this could be fully automated, but given the purpose of the project is done first, if we go further with the project and have thousands of vidoes to process.

Information of the dancer in the videos is simplified by capturing the key points with Openpose. 
We use OpenPose for posedetection[[1]](#1). OpenPose gives us the x- and y-coordinates for 25 different 
joints, their visibility. This temporal sequence of coordinates is used for the input of the model. 

We drop the parts of the frame where the dancer is never present and normalize the results, so that we have all dancers in the same scale despite the distance to camera. 

## The model to predict the labels

Here we face a supervised learning problem: giving a sequence of pose positions
covering 123-578 (features) predict the name of the sequence (label). 5 labels are possible in the first choreography:
"basic", "cuban-basic", "right-turn", "side" and "suzie-q".

The model is a deep network that consists of 2 Gate Recurrent Unit (GRU) layers of 64 and 32 units, repectively. 2 fully connected layers of 16 and 5 neurons are added at the end. 

To train the model the collected videos were splitted in training and validation data. 
From each choreography video we get 8 instances of a sequence.
After data augmentation the train and test sets have 384 and 25 instances per figure.

## Test the predictions yourself

The predictions of the model can be tested in 3 ways: 
1-From your local terminal, 2-Running Streamlit locally or 
3-Running Streamlit in the cloud. Because OpenPose needs a long computational time
without GPU (around 11 hours for all our videos), we provide the some videos that were already preprocessed
with OpenPose

For the first 2 methods you will need to create an appropriate working enviroment. In terminal:
```bat
git clone https://github.com/eeroolli/SalsaAnnotation.git
cd SalsaAnnotation
conda create --name testing_salsa python=3.8
conda activate testing_salsa
pip install -r requirements.txt
```

You cand find a more detailed guide in ./env/README.md

### From your local terminal
From the terminal run the following command

```bat
./run_prediction_in_python.sh predict Ana 4 True
```

### Local Streamlit
From the terminal run the following command

```bat
./streamlit run make_prediction_demo.sh 
```


### Cloud Streamlit
just go to https://share.streamlit.io/eeroolli/salsaannotation/development/make_prediction_demo.py 

## References
<a id="1">[1]</a> 
https://github.com/CMU-Perceptual-Computing-Lab/openpose
