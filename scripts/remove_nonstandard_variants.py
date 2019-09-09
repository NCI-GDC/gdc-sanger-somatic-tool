"""
VCF hard filter that removes non ACTG loci from the VCF.

@author: Kyle Hernandez
@Updated: Shenglai Li
"""
import time
import sys
import argparse
import logging
import pysam

def main(args, logger):
    """
    Main wrapper script for removing non-standard variants
    """
    # Allowed
    good = set(['A', 'T', 'C', 'G'])

    # Reader
    reader = pysam.VariantFile(args.input_vcf)

    # Writer
    mode = 'wz' if args.output_filename.endswith('gz') else 'w'
    writer = pysam.VariantFile(args.output_filename, mode=mode, header=reader.header)

    # Process
    try:
        for record in reader.fetch():
            alleles = list(record.alleles)
            alleles_set = set(list(''.join(alleles).upper()))
            check = alleles_set - good
            if check:
                logger.warning('Removing %s:%s:%s', record.chrom, record.pos, ','.join(alleles))
                continue
            else:
                writer.write(record)

    finally:
        reader.close()
        writer.close()

    if mode == 'wz':
        pysam.tabix_index(args.output_filename, preset='vcf', force=True)


def setup_logger():
    """
    Sets up the logger.
    """
    logger = logging.getLogger("remove_nonstandard_variants")
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
    logger_ = setup_logger()
    logger_.info("-"*80)
    logger_.info("remove_nonstandard_variants.py")
    logger_.info("Program Args: %s", " ".join(sys.argv))
    logger_.info("-"*80)

    p = argparse.ArgumentParser('Utility for hard filtering non-standard variants.')
    p.add_argument('--input_vcf', required=True, help='Input VCF file.')
    p.add_argument('--output_filename', required=True, help='File basename for output VCF file.')

    args_ = p.parse_args()

    # Process
    logger_.info("Processing input VCF file %s...", args_.input_vcf)
    main(args_, logger_)

    # Done
    logger_.info("Finished, took %s seconds.", str(time.time() - start))
