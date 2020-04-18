"""
Checks the bam header to make sure all rgs have the same sample. If not,
writes out a new header with the aliquot submitter id as the SM

@author: Kyle Hernandez <kmhernan@uchicago.edu>
"""
import pysam

from typing import Dict, Any

from gdc_sanger_tools.subcommands import Subcommand 
from gdc_sanger_tools.logger import Logger
from gdc_sanger_tools.utils import ArgParserT, NamespaceT, AlignmentHeaderT, LoggerT


class CheckBamHeader(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgParserT):
        """Add the arguments to the parser"""
        parser.add_argument("--input_bam", required=True,
                            help="Input BAM file to check.")
        parser.add_argument('--aliquot_id', required=True,
                            help="Aliquot id to use for sample name "
                                 "if new header is needed.")
        parser.add_argument('--output_header', required=True,
                            help='Output header file name if a '
                                 'new header is needed.')

    @classmethod
    def check_header(cls, header: AlignmentHeaderT, logger: LoggerT) -> bool:
        """
        Checks if all readgroups have the 'SM' key defined and
        match.
        """ 
        samples = []
        new_header = False
        for item in header['RG']:
            if not item.get('SM'):
                logger.warning("Unable to find 'SM' key in RG {0}".format(item))
                new_header = True
                break
            samples.append(item["SM"])

        if not new_header and len(set(samples)) != 1:
            logger.warning("Multiple sample IDs detected {0}".format(list(set(samples))))
            new_header = True

        return new_header

    @classmethod
    def build_new_header(cls, header: AlignmentHeaderT, aliquot_id: str) -> Dict[str, Any]:
        """
        Builds a dictionary of bam header items with updated SM value in
        readgroups.
        """
        new_header = {}
        for key, vals in header.items():
            if key not in new_header:
                new_header[key] = []

            if key == "RG":
                for item in vals:
                    curr = item.copy()
                    curr["SM"] = aliquot_id
                    new_header[key].append(curr)
            else:
                new_header[key] = vals.copy()
        return new_header

    @classmethod
    def main(cls, options: NamespaceT) -> None:
        """
        Entrypoint for subcommand. 
        """
        logger = Logger.get_logger(cls.__tool_name__())
        logger.info("CheckBamHeader - {}".format(cls.__get_description__()))

        # setup
        bam = pysam.AlignmentFile(options.input_bam, mode="rb")

        try:
            if cls.check_header(bam.header, logger):
                logger.info("Detected RG problems, will create new header with SM {0}".format(options.aliquot_id))
                # build new header
                new_header = cls.build_new_header(bam.header, options.aliquot_id) 
                obam = pysam.AlignmentFile(options.output_header, mode="w", header=new_header)
                obam.close()
            else:
                logger.info("No issues detected. No header written.")

        finally:
            bam.close()

    @classmethod
    def __get_description__(cls):
        """
        Optionally returns description
        """
        return ("Checks the bam header to make sure all rgs have "
               "the same sample. If not, writes out a new header "
               "with the aliquot submitter id as the SM.")
