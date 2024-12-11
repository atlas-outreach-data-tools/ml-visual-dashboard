#!/bin/sh

if !(conda info --envs | grep -q ml-visual-dashboard)
then conda env create -f environment.yml 
fi
conda activate ml-visual-dashboard
python source/RegenerateModels.py
