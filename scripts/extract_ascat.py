#!/usr/bin/env python3

"""
Extract and Process ASCAT outputs in the Sanger TAR file.

@author Daniel Miller <dmiller15@uchicago.edu>
"""

import argparse
import json
import logging
import sys
import tarfile
import time

def get_file_from_tar(tar_path, file_name):
    """
    Using a partial or full file name, get the full path of the file within the tar.
    @param tar_path: path to a tar file
    @param file_name: full file name or end of the filename to find
    @return the path for the file
    """
    with tarfile.open(tar_path, 'r') as tar_fh:
        for i in tar_fh.getmembers():
            if i.name.endswith(file_name):
                return i.name

def reformat_copynumber(args):
    """
    Take the Sanger output ascat caveman copy number file and add columns to make it match GDC format.
    @param input: path to Sanger output tar file
    @param output: path to write the output
    @param gdcaliquot: aliquot id used to generate the Sanger tar
    @return writes a file
    """
    seg_path = get_file_from_tar(args.input, 'copynumber.caveman.csv')
    with tarfile.open(args.input, 'r') as tar_fh:
        fobj = tar_fh.extractfile(seg_path)
        try:
            with open(args.output, 'w') as o:
                o.write('\t'.join(["GDC_Aliquot","Chromosome","Start","End","Copy_Number","Major_Copy_Number","Minor_Copy_Number\n"]))
                while True:
                    rline = fobj.readline()
                    if not rline: break
                    line = rline.strip().decode('utf-8').split(',')
                    chrom = 'chr' + line[1]
                    start = line[2]
                    end = line[3]
                    copy_number = int(line[6])
                    minor_cn = int(line[7])
                    major_cn = copy_number - minor_cn 
                    wline = '\t'.join([args.gdcaliquot, chrom, start, end, str(copy_number), str(major_cn), str(minor_cn)])
                    o.write(wline+'\n')
        finally:
            fobj.close()

def extract_stats(args):
    """
    Take the Sanger output ascat sample statistics file and extract two values.
    @param input: path to Sanger output tar file
    @return output_json: stdout json object containing stats for tumor_purity and ploidy
    """
    output_json = {}
    stats_path = get_file_from_tar(args.input, 'samplestatistics.txt')
    with tarfile.open(args.input, 'r') as tar_fh:
       fobj = tar_fh.extractfile(stats_path)
       try:
           lines = fobj.readlines()
           for line in lines:
               if line.strip().decode('utf-8').split(' ')[0] == 'NormalContamination':
                   output_json['tumor_purity'] = 1 - float(line.strip().decode('utf-8').split(' ')[1])
               elif line.strip().decode('utf-8').split(' ')[0] == 'Ploidy':
                   output_json['ploidy'] = float(line.strip().decode('utf-8').split(' ')[1])
       finally:
           fobj.close()   
    print(json.dumps(output_json))

def setup_logger():
    """
    Sets up the logger.
    @return logger
    """
    logger = logging.getLogger("extract_ascat")
    LoggerFormat = '[%(levelname)s] [%(asctime)s] [%(name)s] - %(message)s'
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(LoggerFormat, datefmt='%Y%m%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def main():
    """
    Main wrapper for the program.
    """

    start = time.time()
    logger = setup_logger()
    logger.info("-"*80)
    logger.info("extract_ascat.py")
    logger.info("Program Args: {0}".format(" ".join(sys.argv)))
    logger.info("-"*80)

    description = 'Tool to process Sanger WGS pipeline TAR output and produce GDC standard files and metrics.'
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers()

    seg_subparser = subparsers.add_parser('reformat_copynumber')
    seg_subparser.add_argument('--input', '-i', help='path to file output from Sanger pipeline')
    seg_subparser.add_argument('--output', '-o', help='path for output file')
    seg_subparser.add_argument('--gdcaliquot', '-g', help='GDC Aliquot ID used to generate the file')
    seg_subparser.set_defaults(func=reformat_copynumber)

    stat_subparser = subparsers.add_parser('extract_stats')
    stat_subparser.add_argument('--input', '-i', help='path to file output from Sanger pipeline')
    stat_subparser.set_defaults(func=extract_stats)

    args = parser.parse_args()

    logger.info("Processing results tar archive {0}...".format(args.input))
    args.func(args) 

    logger.info("Finished, took {0} seconds.".format(time.time() - start))

if __name__ == '__main__':
    main()
