#!/usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # disable ROOT internal argument parser

import argparse
import yaml
import os
import copy

from shape_producer.cutstring import Cut, Cuts
from shape_producer.channel import *
from shape_producer.estimation_methods_2016 import *
from shape_producer.era import Run2016

import logging
logger = logging.getLogger("write_dataset_config")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_arguments():
    logger.debug("Parse arguments.")
    parser = argparse.ArgumentParser(
        description=
        "Write dataset config for creation of training dataset for a specific channel."
    )
    parser.add_argument("--channel", required=True, help="Analysis channel")
    parser.add_argument(
        "--base-path", required=True, help="Path to Artus output files")
    parser.add_argument(
        "--output-path", required=True, help="Path to output directory")
    parser.add_argument(
        "--output-filename",
        required=True,
        help="Filename postifx of output filename")
    parser.add_argument(
        "--tree-path", required=True, help="Path to tree in ROOT files")
    parser.add_argument(
        "--event-branch", required=True, help="Branch with event numbers")
    parser.add_argument(
        "--training-weight-branch",
        required=True,
        help="Branch with training weights")
    parser.add_argument(
        "--output-config", required=True, help="Output dataset config file")
    parser.add_argument(
        "--database", required=True, help="Kappa datsets database.")
    return parser.parse_args()


def main(args):
    # Write arparse arguments to YAML config
    logger.debug("Write argparse arguments to YAML config.")
    output_config = {}
    output_config["base_path"] = args.base_path
    output_config["output_path"] = args.output_path
    output_config["output_filename"] = args.output_filename
    output_config["tree_path"] = args.tree_path
    output_config["event_branch"] = args.event_branch
    output_config["training_weight_branch"] = args.training_weight_branch

    # Define era
    era = Run2016(args.database)

    ############################################################################

    # Channel: mt
    if args.channel == "mt":
        channel = MT()

        # Set up `processes` part of config
        output_config["processes"] = {}

        # Additional cuts
        additional_cuts = Cuts(Cut("mt_1<50", "mt"))
        logger.warning("Use additional cuts for mt: %s",
                       additional_cuts.expand())

        # MC-driven processes
        # NOTE: Define here the mappig of the process estimations to the training classes
        classes_map = {
            "ggH": "htt",
            "qqH": "htt",
            "VH": "htt",
            "ZTT": "ztt",
            "ZL": "zll",
            "ZJ": "zll",
            "TTT": "tt",
            "TTJ": "tt",
            "W": "w"
        }
        for estimation in [
                ggHEstimation(era, args.base_path, channel),
                qqHEstimation(era, args.base_path, channel),
                VHEstimation(era, args.base_path, channel),
                ZTTEstimation(era, args.base_path, channel),
                ZLEstimationMT(era, args.base_path, channel),
                ZJEstimationMT(era, args.base_path, channel),
                TTTEstimationMT(era, args.base_path, channel),
                TTJEstimationMT(era, args.base_path, channel),
                WEstimation(era, args.base_path, channel)
        ]:
            output_config["processes"][estimation.name] = {
                "files": [
                    str(f).replace(args.base_path + "/", "")
                    for f in estimation.get_files()
                ],
                "cut_string": (estimation.get_cuts() + channel.cuts +
                               additional_cuts).expand(),
                "weight_string":
                estimation.get_weights().extract(),
                "class":
                classes_map[estimation.name]
            }

        # Same sign selection for data-driven QCD
        estimation = DataEstimation(era, args.base_path, channel)
        estimation.name = "QCD"
        channel_ss = copy.deepcopy(channel)
        channel_ss.cuts.get("os").invert()
        output_config["processes"][estimation.name] = {
            "files": [
                str(f).replace(args.base_path + "/", "")
                for f in estimation.get_files()
            ],
            "cut_string": (estimation.get_cuts() + channel_ss.cuts +
                           additional_cuts).expand(),
            "weight_string":
            estimation.get_weights().extract(),
            "class":
            "qcd"
        }

    ############################################################################

    # Channel: et
    if args.channel == "et":
        channel = ET()

        # Set up `processes` part of config
        output_config["processes"] = {}

        # Additional cuts
        additional_cuts = Cuts(Cut("mt_1<50", "mt"))
        logger.warning("Use additional cuts for et: %s",
                       additional_cuts.expand())

        # MC-driven processes
        # NOTE: Define here the mappig of the process estimations to the training classes
        classes_map = {
            "ggH": "htt",
            "qqH": "htt",
            "VH": "htt",
            "ZTT": "ztt",
            "ZL": "zll",
            "ZJ": "zll",
            "TTT": "tt",
            "TTJ": "tt",
            "W": "w"
        }
        for estimation in [
                ggHEstimation(era, args.base_path, channel),
                qqHEstimation(era, args.base_path, channel),
                VHEstimation(era, args.base_path, channel),
                ZTTEstimation(era, args.base_path, channel),
                ZLEstimationET(era, args.base_path, channel),
                ZJEstimationET(era, args.base_path, channel),
                TTTEstimationET(era, args.base_path, channel),
                TTJEstimationET(era, args.base_path, channel),
                WEstimation(era, args.base_path, channel)
        ]:
            output_config["processes"][estimation.name] = {
                "files": [
                    str(f).replace(args.base_path + "/", "")
                    for f in estimation.get_files()
                ],
                "cut_string": (estimation.get_cuts() + channel.cuts +
                               additional_cuts).expand(),
                "weight_string":
                estimation.get_weights().extract(),
                "class":
                classes_map[estimation.name]
            }

        # Same sign selection for data-driven QCD
        estimation = DataEstimation(era, args.base_path, channel)
        estimation.name = "QCD"
        channel_ss = copy.deepcopy(channel)
        channel_ss.cuts.get("os").invert()
        output_config["processes"][estimation.name] = {
            "files": [
                str(f).replace(args.base_path + "/", "")
                for f in estimation.get_files()
            ],
            "cut_string": (estimation.get_cuts() + channel_ss.cuts +
                           additional_cuts).expand(),
            "weight_string":
            estimation.get_weights().extract(),
            "class":
            "qcd"
        }

    ############################################################################

    # Channel: tt
    if args.channel == "tt":
        channel = TT()

        # Set up `processes` part of config
        output_config["processes"] = {}

        # Additional cuts
        additional_cuts = Cuts()
        logger.warning("Use additional cuts for tt: %s",
                       additional_cuts.expand())

        # MC-driven processes
        # NOTE: Define here the mappig of the process estimations to the training classes
        classes_map = {
            "ggH": "htt",
            "qqH": "htt",
            "VH": "htt",
            "ZTT": "ztt",
            "ZL": "zll",
            "ZJ": "zll",
            "TTT": "tt",
            "TTJ": "tt",
            "W": "w"
        }
        logger.critical("Using et estimation methods for tt. Fixme!")
        for estimation in [
                ggHEstimation(era, args.base_path, channel),
                qqHEstimation(era, args.base_path, channel),
                VHEstimation(era, args.base_path, channel),
                ZTTEstimation(era, args.base_path, channel),
                ZLEstimationET(era, args.base_path, channel),
                ZJEstimationET(era, args.base_path, channel),
                TTTEstimationET(era, args.base_path, channel),
                TTJEstimationET(era, args.base_path, channel),
                WEstimation(era, args.base_path, channel)
        ]:
            output_config["processes"][estimation.name] = {
                "files": [
                    str(f).replace(args.base_path + "/", "")
                    for f in estimation.get_files()
                ],
                "cut_string": (estimation.get_cuts() + channel.cuts +
                               additional_cuts).expand(),
                "weight_string":
                estimation.get_weights().extract(),
                "class":
                classes_map[estimation.name]
            }

        # Same sign selection for data-driven QCD
        estimation = DataEstimation(era, args.base_path, channel)
        estimation.name = "QCD"
        channel_ss = copy.deepcopy(channel)
        channel_ss.cuts.get("os").invert()
        output_config["processes"][estimation.name] = {
            "files": [
                str(f).replace(args.base_path + "/", "")
                for f in estimation.get_files()
            ],
            "cut_string": (estimation.get_cuts() + channel_ss.cuts +
                           additional_cuts).expand(),
            "weight_string":
            estimation.get_weights().extract(),
            "class":
            "qcd"
        }

    ############################################################################

    # Write output config
    logger.info("Write config to file: {}".format(args.output_config))
    yaml.dump(
        output_config, open(args.output_config, 'w'), default_flow_style=False)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
