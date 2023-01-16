#!/bin/bash

ENVFILEVAL=$(head -n 1 env.yml)
ENVNAME=${ENVFILEVAL:6}

source ~/miniconda3/etc/profile.d/conda.sh
CONDAENVLIST=$(conda env list)

if grep -q "$ENVNAME " <<< "$CONDAENVLIST"; 
then
  printf "\n\n$ENVNAME environment exists\n"
else  
  conda env create -f env.yml --force
fi

conda activate $ENVNAME