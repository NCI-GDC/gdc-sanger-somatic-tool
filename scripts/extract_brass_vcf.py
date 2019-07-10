"""
Extracts and processes the brass VCF file.

@author: Kyle Hernandez
"""
import os
import time
import sys
import tarfile
import pysam
import argparse
import logging 

def main(args):
    """
    Main wrapper for processing the brass VCF outputs.
    """
    # Extract keys
    logger.info("Extracting brass vcf file key from tarfile...")
    vcf, vcf_index = extract_tar_keys(args.results_archive)
    # process vcf
    logger.info("Processing brass vcf {0}...".format(vcf))
    process_vcf(args.results_archive, vcf, vcf_index, args.output_prefix)

def process_vcf(archive, vcf, vcf_index, output_prefix):
    """
    Extracts and processes the brass vcf file.
    """
    out_raw_vcf = '{0}.tmp.vcf.gz'.format(output_prefix)
    logger.info("Extracting raw vcf to tmp file {0}".format(out_raw_vcf))
    extract_file(archive, vcf, out_raw_vcf)

    out_raw_vcf_index = '{0}.tmp.vcf.gz.tbi'.format(output_prefix)
    logger.info("Extracting raw vcf index to tmp file {0}".format(out_raw_vcf_index))
    extract_file(archive, vcf_index, out_raw_vcf_index)

    # Update the sample name using BGZFile which doesn't assert any VCF format
    logger.info("Processing raw VCF to change TUMOUR -> TUMOR...")
    out_formatted_vcf = '{0}.vcf.gz'.format(output_prefix)
    logger.info("Creating final vcf {0}".format(out_formatted_vcf))
    writer = pysam.BGZFile(out_formatted_vcf, mode='wb')
    reader = pysam.BGZFile(out_raw_vcf, mode='rb') 
    try:
        for line in reader:
            line = line.decode('utf-8')
            if line.startswith('##'):
                if line.startswith('##SAMPLE=<ID=TUMOUR'):
                    new_line = line.replace('ID=TUMOUR', 'ID=TUMOR') + '\n'
                    writer.write(new_line.encode('utf-8'))
                else:
                    new_line = line + '\n'
                    writer.write(new_line.encode('utf-8') )
            elif line.startswith('#CHROM'):
                new_line = line.replace('TUMOUR', 'TUMOR') + '\n'
                writer.write(new_line.encode('utf-8'))
            else:
                new_line = line + '\n'
                writer.write(new_line.encode('utf-8'))
    finally:
        writer.close()
        reader.close()

    # tabix index
    logger.info("Creating final vcf index {0}".format(out_formatted_vcf + '.tbi'))
    pysam.tabix_index( out_formatted_vcf, preset='vcf', force=True )

    # clean up
    logger.info("Cleaning up tmp files...")
    os.remove(out_raw_vcf)
    os.remove(out_raw_vcf_index)

def extract_file(tar, key, output_path):
    """
    Extracts a file from the tar to a particular path.
    """
    with tarfile.open(tar, 'r') as tar_fh:
        fobj = tar_fh.extractfile(key)
        try:
            with open(output_path, 'wb') as o:
                while True:
                    chunk = fobj.read(1024)
                    if not chunk: break
                    o.write(chunk)
        finally:
            fobj.close()
     
def extract_tar_keys(tar):
    """
    Extracts the relevant brass keys from the tar archive.
    """
    vcf = None
    vcf_index = None
    with tarfile.open(tar, 'r') as tar_fh:
        for item in tar_fh.getnames():
            if '/brass/' in item:
                if item.endswith('.annot.vcf.gz'):
                    vcf = item
                    logger.info("Found brass vcf key: {0}".format(vcf))
                elif item.endswith('.annot.vcf.gz.tbi'):
                    vcf_index = item
                    logger.info("Found brass vcf index key: {0}".format(vcf_index))
                if vcf and vcf_index:
                    break
    assert vcf is not None, 'Unable to find brass vcf file in {0}'.format(tar)
    assert vcf_index is not None, 'Unable to find brass vcf index file in {0}'.format(tar)
    return vcf, vcf_index

def setup_logger():
    """
    Sets up the logger.
    """
    logger = logging.getLogger("extract_brass_vcf")
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
    logger.info("extract_brass_vcf.py")
    logger.info("Program Args: {0}".format(" ".join(sys.argv)))
    logger.info("-"*80)

    p = argparse.ArgumentParser('Utility for extracting brass files from sanger results archive.')
    p.add_argument('--results_archive', required=True, help='Sanger results tar archive.')
    p.add_argument('--output_prefix', required=True, help='Prefix for all outputs.')

    args = p.parse_args()

    # Process
    logger.info("Processing results tar archive {0}...".format(args.results_archive))
    main(args)

    # Done
    logger.info("Finished, took {0} seconds.".format(time.time() - start))
