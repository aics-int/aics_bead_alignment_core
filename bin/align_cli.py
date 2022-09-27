import argparse
import logging
import os
import pwd
import sys
import traceback

from aics_bead_alignment_core.align import (
    align,
)

log = logging.getLogger()


class Args(argparse.Namespace):
    def __init__(self):
        self.debug = False
        self.raw_image_path_one = str(),
        self.raw_image_path_two =str(),
        self.__parse()

    def __parse(self):
        p = argparse.ArgumentParser(
            prog="BeadAlignment",
            description="Generates alignment coordinates between two images",
        )

        p.add_argument(
            "--raw_image_path_one",
            dest="raw_image_path_one",
            type=str,
            help="Image file location on local computer (Image for Processing)",
            required=True,
        )

        p.add_argument(
            "--raw_image_path_two",
            dest="raw_image_path_two",
            type=str,
            help="Image file location on local computer (Image for Processing)",
            required=True,
        )

        # Optionals
        p.add_argument(
            "--scene",
            type=str,
            help= "String representation of scene",
            default= "",
            required=False,
        )
        
        p.add_argument(
            "--eval_method",
            type=str,
            help= "opencv evaluation method",
            default= "'cv.TM_CCOEFF_NORMED'",
            required=False,
        )

        p.parse_args(namespace=self)

    ###############################################################################


def main():
    args = Args()
    debug = args.debug

    try:
        align(
            raw_image_path_one = args.raw_image_path_one,
            raw_image_path_two = args.raw_image_path_two,
            scene = args.scene,
            eval_method = args.eval_method
        )

    except Exception as e:
        log.error("=============================================")
        if debug:
            log.error("\n\n" + traceback.format_exc())
            log.error("=============================================")
        log.error("\n\n" + str(e) + "\n")
        log.error("=============================================")
        sys.exit(1)


###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
