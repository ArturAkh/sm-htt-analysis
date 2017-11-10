#!/usr/bin/env python

from classes.JDLCreator import JDLCreator
import yaml
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=str, help="Output path")
    parser.add_argument(
        "--binning",
        type=str,
        default="gof/binning.yaml",
        help="Binning config")
    return parser.parse_args()


def main(args):
    jobs = JDLCreator("condocker")

    jobs.executable = "gof/job.sh"
    jobs.wall_time = 1 * 60 * 60
    jobs.memory = 2048
    jobs.accounting_group = "cms.higgs"
    jobs.image = "stwunsch/slc6-condocker:smhtt"

    # Build list of arguments
    arguments = []
    config = yaml.load(open(args.binning))
    for channel in config["gof"]:
        for variable in config["gof"][channel]:
            arguments.append("{} {}".format(channel, variable))
    jobs.arguments = arguments

    # The job requires lots of CPU resources
    # NOTE: This selects the sg machines.
    jobs.requirements = '(Target.ProvidesCPU == True) && (Target.ProvidesEKPResources == True) && (Target.Cloudsite =?= "ekpsupermachines")'
    jobs.job_folder = args.output
    jobs.WriteJDL()


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
