# Salsa Annotation

In this project we will create annotations/labels for cuban salsa videos. Salsa is a couple dance where movement patterns appear in counting of 4 steps.

We tried different sizes of elementary units and notation systems, and ended up with labelling the data with the kind of units that dancers are using too. So, our unit consists of elements that are as long the dancers counting 123-567- or two bars of music.  

The labeling problem, unbalanced category sizes are solved by
by using a coreography where each dancer repeats each element twice, 
then turns 90-degrees so that the same choreography can be filmed from a
different angle. We film in total of 4 different angles, so
each dancer repeats each figure a total of 8 times. 

We made a video with the choreography people are supposed to do.
https://drive.google.com/file/d/1tX5dczXymc4EjAB0A9-5mkPx-pvV412n/view?usp=sharing 

There is a FAQ for people making videos at http://salsa.eero.no 

The input data is videos from mobile phones.  In preprossing the videos are converted to same size and speed.  

Information of the dancer in the videos is simplified by capturing the key points with Openpose. 
We use OpenPose for posedetection. OpenPose gives us the x- and y-coordinates for 25 different 
joints and their visibility. We drop the parts of the frame where the dancer is never present and normalize the results, so that we have all dancers in the same scale despite the distance to camera.

These are used as input for activity detection with GRU, LSTM, RandomForest. 
Basically, we do machine learning in order to categorize the activity in a video segment. 

We expect 2 main outputs:

1. Given a video: obtain the annotations 
1. Given a seed movement: generate words or sentences that can continue the dance in autonomus way

## To run the prediction 

in bash  
'''
./Prediction_run.sh predict Gustavo 1 True
'''
where "predict" is the task, "Gustavo" is the folder with the video, 1 is the choreography and True refers to sample.  
TODO: 