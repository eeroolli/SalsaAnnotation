# Salsa Annotation

In this project we will create annotations/labels for cuban salsa videos. Salsa is a couple dance where movement patterns appear in counting of 4 steps.
The elementary unit of movement (word) is assigned to one of these steps, while figures (sentences) correspond to a sequential arrangement of one or more 4 steps counting. 

Information of the dancing couple in the videos can be simplied by capturing the key points with Openpose. 

The labeling problem, unbalanced category sizes are solved by
by using a coreography where each dancer repeats each twice, 
then turns 90-degrees so that the same choreography can be filmed from a
different angle. We film in total of 4 different angles, so
each dancer repeats each figure a total of 8 times. 

We made a video with the choreography people are supposed to do.
https://drive.google.com/file/d/1tX5dczXymc4EjAB0A9-5mkPx-pvV412n/view?usp=sharing 

The input data is videos from mobile phones.

We use OpenPose for posedetection. OpenPose gives us the coordinates for 25 different 
joints and their visibility. 

These are used as input for activity detection with GRU, LSTM, RandomForest. 
Basically, we do machine learning in order to categorize the activity in a video segment. 


We expect 2 main outputs:

1. Given a video: obtain the annotations at different levels (words or sentences)
1. Given a seed movement: generate words or sentences that can continue the dance in autonomus way

## Tasks
  
  1. Item 1
  1. Item 2
