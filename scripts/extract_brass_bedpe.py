"""
Extracts and processes the brass bedpe file.

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
    Main wrapper for processing the brass bedpe outputs.
    """
    # Extract keys
    logger.info("Extracting brass bedpe file key from tarfile...")
    bedpe, bedpe_index = extract_tar_keys(args.results_archive)
    # process bedpe
    logger.info("Processing brass bedpe {0}...".format(bedpe))
    process_bedpe(args.results_archive, bedpe, bedpe_index, args.output_prefix)

def format_header(line):
    """
    Formats the bedpe column header line.
    """
    cols = []
    for n, item in enumerate(line.replace('#', '').strip().split('\t')):
        if item == 'name/id':
            cols.append('name')
        elif item == 'brass_score':
            cols.append('score')
        elif item.startswith('strand') and n > 9:
            if item == 'strand1':
                cols.append('transcript1_strand')
            elif item == 'strand2':
                cols.append('transcript2_strand')
            else:
                raise ValueError("Unknown strand value column {0} - {1}".format(n, item))
        else:
            cols.append(item.lower().replace(' ', '_').replace('/', '_').replace('-', '_'))
    return cols

def process_bedpe(archive, bedpe, bedpe_index, output_prefix):
    """
    Extracts and processes the brass bedpe file.
    """
    out_raw_bedpe = '{0}.tmp.bedpe.gz'.format(output_prefix)
    logger.info("Extracting raw bedpe to tmp file {0}".format(out_raw_bedpe))
    extract_file(archive, bedpe, out_raw_bedpe)

    out_raw_bedpe_index = '{0}.tmp.bedpe.gz.tbi'.format(output_prefix)
    logger.info("Extracting raw bedpe index to tmp file {0}".format(out_raw_bedpe_index))
    extract_file(archive, bedpe_index, out_raw_bedpe_index)

    out_formatted_bedpe = '{0}.bedpe.gz'.format(output_prefix)
    logger.info("Creating final bedpe {0}".format(out_formatted_bedpe))
    writer = pysam.BGZFile(out_formatted_bedpe, mode='wb')
    reader = pysam.BGZFile(out_raw_bedpe, mode='rb')
    try:
        meta_line = None
        process_header = False
        for line in reader:
            line = line.decode('utf-8')
            if line.startswith('#'):
                meta_line = line
            else:
                if not process_header:
                    hdr = format_header(meta_line)
                    assert len(hdr) == len(set(hdr)), \
                        "Duplicate header keys {0}".format(','.join(hdr))
                    writer.write(('#' + '\t'.join(hdr) + '\n').encode('utf-8'))
                    process_header = True

                new_line = line + '\n'
                writer.write(new_line.encode('utf-8'))
    finally:
        writer.close()
        reader.close()

    # tabix index
    logger.info("Creating final bedpe index {0}".format(out_formatted_bedpe + '.tbi'))
    pysam.tabix_index( out_formatted_bedpe, preset='bed', force=True )

    # clean up
    logger.info("Cleaning up tmp files...")
    os.remove(out_raw_bedpe)
    os.remove(out_raw_bedpe_index)

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
    bedpe = None
    bedpe_index = None
    with tarfile.open(tar, 'r') as tar_fh:
        for item in tar_fh.getnames():
            if '/brass/' in item:
                if item.endswith('.annot.bedpe.gz'):
                    bedpe = item
                    logger.info("Found brass bedpe key: {0}".format(bedpe))
                elif item.endswith('.annot.bedpe.gz.tbi'):
                    bedpe_index = item
                    logger.info("Found brass bedpe index key: {0}".format(bedpe_index))
                if bedpe and bedpe_index:
                    break
    assert bedpe is not None, 'Unable to find brass bedpe file in {0}'.format(tar)
    assert bedpe_index is not None, 'Unable to find brass bedpe index file in {0}'.format(tar)
    return bedpe, bedpe_index

def setup_logger():
    """
    Sets up the logger.
    """
    logger = logging.getLogger("extract_brass_bedpe")
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
    logger.info("extract_brass_bedpe.py")
    logger.info("Program Args: {0}".format(" ".join(sys.argv)))
    logger.info("-"*80)

    p = argparse.ArgumentParser('Utility for extracting brass bedpe file from sanger results archive.')
    p.add_argument('--results_archive', required=True, help='Sanger results tar archive.')
    p.add_argument('--output_prefix', required=True, help='Prefix for all outputs.')

    args = p.parse_args()

    # Process
    logger.info("Processing results tar archive {0}...".format(args.results_archive))
    main(args)

    # Done
    logger.info("Finished, took {0} seconds.".format(time.time() - start))
