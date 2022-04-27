#!/bin/bash

if [ "$1" == "train" ]
then
   echo "Preparing for training ..."
elif [ "$1" == "predict" ]
then
   cd src
   python Prediction_pipeline.py --video $2 --coreo $3 --sample $4
   cd .. 
else 
   echo "Choose an option"
fi
