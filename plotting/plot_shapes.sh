#!/bin/bash

source utils/setup_cmssw.sh
source utils/setup_python.sh

./plotting/plot_shapes.py -i datacard_shapes_prefit.root -c $@
./plotting/plot_shapes.py -i datacard_shapes_prefit.root --png -c $@
./plotting/plot_shapes.py -i datacard_shapes_postfit_sb.root -c $@
./plotting/plot_shapes.py -i datacard_shapes_postfit_sb.root --png -c $@
