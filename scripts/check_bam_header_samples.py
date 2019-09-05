"""
Checks the bam header to make sure all rgs have the same sample. If not,
writes out a new header with the aliquot submitter id as the SM

@author: Kyle Hernandez
"""
import os
import time
import sys
import pysam
import argparse
import logging 

def main(args):
    """
    Main wrapper for processing bam file headers. 
    """
    # Extract keys
    logger.info("Extracting bam header...")
    extract_bam_header(args.input_bam, args.aliquot_id, args.output_header)

def extract_bam_header(bampath, aliquot_id, out_file):
    """
    Extracts the metadata from the bam header and 
    checks if all samples are the same.
    """
    bam = pysam.AlignmentFile(bampath, mode='rb')
    samples = [] 
    new_header = False

    fix_header = {} 

    try:
        for item in bam.header['RG']:
            if not item.get('SM'):
                logger.warn("Unable to find sample key in rg {0}".format(item)) 
                new_header = True
                break
            samples.append(item['SM'])
        if not new_header and len(set(samples)) != 1:
            logger.warn("Multiple sample IDs detected {0}".format(set(samples)))
            new_header = True 

        if new_header:
            logger.info("Detected RG problems, will create new header with SM {0}".format(
                aliquot_id))
            for key, vals in bam.header.items():
                if key not in fix_header: fix_header[key] = [] 
                if key == 'RG':
                    for item in vals: 
                        item['SM'] = aliquot_id 
                        fix_header[key].append(item) 
                else:
                    fix_header[key] = vals 
            obam = pysam.AlignmentFile(out_file, mode='w', header=fix_header) 
            obam.close()

        else:
            logger.info("No issues detected. No header written")

    finally:
        bam.close()

def setup_logger():
    """
    Sets up the logger.
    """
    logger = logging.getLogger("check_bam_header")
    LoggerFormat = '[%(levelname)s] [%(asctime)s] [%(name)s] - %(message)s'
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(LoggerFormat, datefmt='%Y%m%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
    
if __name__ == '__main__':
    """
    CLI Entrypoint.
    """
    start = time.time()
    logger = setup_logger()
    logger.info("-"*80)
    logger.info("check_bam_header_samples.py")
    logger.info("Program Args: {0}".format(" ".join(sys.argv)))
    logger.info("-"*80)

    p = argparse.ArgumentParser('Utility for checking samples in bam header and fixing if needed') 
    p.add_argument('--input_bam', required=True, help='Input bam file.')
    p.add_argument('--aliquot_id', required=True, help='Aliquot id to use for sample name if new header is needed.')
    p.add_argument('--output_header', required=True, help='Output header file name if a new header is needed.')

    args = p.parse_args()

    # Process
    logger.info("Processing bam file {0}...".format(args.input_bam))
    main(args)

    # Done
    logger.info("Finished, took {0} seconds.".format(time.time() - start))
