#!/bin/bash

BINNING=shapes/binning.yaml
ERA=$1
CHANNELS=${@:2}

source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh
source utils/setup_samples.sh $ERA

# Calculate binning from data distributions
# NOTE: Binning is committed in this repository.
#./shapes/calculate_binning.sh et
#./shapes/calculate_binning.sh mt
#./shapes/calculate_binning.sh tt

# Produce shapes
for CHANNEL in $CHANNELS
do
    python shapes/produce_shapes.py \
        --directory $ARTUS_OUTPUTS \
        --et-friend-directory $ARTUS_FRIENDS_ET \
        --mt-friend-directory $ARTUS_FRIENDS_MT \
        --tt-friend-directory $ARTUS_FRIENDS_TT \
        --datasets $KAPPA_DATABASE \
        --binning $BINNING \
        --channels $CHANNEL \
        --era $ERA \
        --tag ${ERA}_${CHANNEL} \
        --num-threads 8 &
done

wait

hadd -f ${ERA}_shapes.root ${ERA}_*_shapes.root

# Convert shapes to synced format
python shapes/convert_to_synced_shapes.py ${ERA}_shapes.root .
