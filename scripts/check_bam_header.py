"""
Checks the bam header:

* to make sure all rgs have the same sample
* enforce PL to be ILLUMINA

Writes out a new header with the aliquot submitter id as the SM
and/or PL as ILLUMINA as needed.

@author: Kyle Hernandez
"""
import os
import time
import sys
import pysam
import argparse
import logging

PLATFORM = "ILLUMINA"


def main(args: argparse.Namespace) -> None:
    """
    Main wrapper for processing bam file headers.
    """
    logger.info("Extracting bam header...")
    bam = pysam.AlignmentFile(args.input_bam, mode="rb")
    try:
        pass_sm = check_samples(bam)
        pass_pl = check_platforms(bam)
        conditionally_generate_new_header(
            bam, pass_sm, pass_pl, args.aliquot_id, args.output_header
        )
    finally:
        bam.close()


def check_samples(bam: pysam.AlignmentFile) -> bool:
    """
    Checks the bam readgroups for missing SM fields and mismatched
    SMs.
    """
    samples = []
    for item in bam.header["RG"]:
        if not item.get("SM", "").strip():
            logger.warn("Unable to find sample in rg {}".format(item))
            return False
        else:
            samples.append(item["SM"])
    if len(set(samples)) != 1:
        logger.warn("Found multiple sample IDs! {}".format(set(samples)))
        return False
    return True


def check_platforms(bam: pysam.AlignmentFile) -> bool:
    """
    Checks whether the bam rgs all have PL set to PLATFORM
    """
    for item in bam.header["RG"]:
        if not item.get("PL", "").strip():
            logger.warn("Unable to find platform in rg {}".format(item))
            return False
        elif item["PL"] != PLATFORM:
            logger.warn(
                "Found readgroup with platform != '{}' - {}".format(PLATFORM, item)
            )
            return False
    return True


def conditionally_generate_new_header(
    bam: pysam.AlignmentFile,
    pass_sm: bool,
    pass_pl: bool,
    aliquot_id: str,
    out_file: str,
) -> None:
    """
    If pass_sm or pass_pl are False, generates the new bam header, otherwise does nothing.
    """
    if pass_sm and pass_pl:
        logger.info("No issues detected. No header written.")
    else:
        logger.info("Detected RG problems, will create new header.")
        fix_header = {}
        for key, vals in bam.header.items():
            if key not in fix_header:
                fix_header[key] = []
            if key == "RG":
                for item in vals:
                    if not pass_sm:
                        item["SM"] = aliquot_id
                    if not pass_pl:
                        item["PL"] = PLATFORM
                    fix_header[key].append(item)
            else:
                fix_header[key] = vals

        obam = pysam.AlignmentFile(out_file, mode="w", header=fix_header)
        obam.close()


def setup_logger():
    """
    Sets up the logger.
    """
    logger = logging.getLogger("check_bam_header")
    LoggerFormat = "[%(levelname)s] [%(asctime)s] [%(name)s] - %(message)s"
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(LoggerFormat, datefmt="%Y%m%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    """
    CLI Entrypoint.
    """
    start = time.time()
    logger = setup_logger()
    logger.info("-" * 80)
    logger.info("check_bam_header_samples.py")
    logger.info("Program Args: {0}".format(" ".join(sys.argv)))
    logger.info("-" * 80)

    p = argparse.ArgumentParser(
        "Utility for checking samples in bam header and fixing if needed"
    )
    p.add_argument("--input_bam", required=True, help="Input bam file.")
    p.add_argument(
        "--aliquot_id",
        required=True,
        help="Aliquot id to use for sample name if new header is needed.",
    )
    p.add_argument(
        "--output_header",
        required=True,
        help="Output header file name if a new header is needed.",
    )

    args = p.parse_args()

    # Process
    logger.info("Processing bam file {0}...".format(args.input_bam))
    main(args)

    # Done
    logger.info("Finished, took {0} seconds.".format(time.time() - start))
