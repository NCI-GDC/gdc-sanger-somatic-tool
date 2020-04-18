"""Tests for `gdc_sanger_tools.subcommands.CheckBamHeader`"""
import unittest
import pysam
import attr
import tempfile
import os

from gdc_sanger_tools.subcommands import CheckBamHeader
from gdc_sanger_tools.__main__ import main
from gdc_sanger_tools.logger import Logger 

from utils import captured_output, get_test_data_path, cleanup_files


@attr.s
class MockArgs:
    input_bam = attr.ib()
    aliquot_id = attr.ib()
    output_header = attr.ib()

class TestCheckBamHeader(unittest.TestCase):
    def test_check_header(self):
        mock_header = {'RG': [
            {'ID': '1', 'SM': 'AB'}
            ]
        }
        with captured_output() as (_, _):
            logger = Logger.get_logger("CheckBamHeader")
            res = CheckBamHeader.check_header(mock_header, logger)
            self.assertFalse(res)

        mock_header = {'RG': [
            {'ID': '1', 'SM': 'AB'},
            {'ID': '2'},
            ]
        }
        with captured_output() as (_, stderr):
            logger = Logger.get_logger("CheckBamHeader")
            res = CheckBamHeader.check_header(mock_header, logger)
            self.assertTrue(res)
        stderr = stderr.getvalue()
        self.assertTrue('WARNING' in stderr)
        self.assertTrue("Unable to find 'SM' key in RG" in stderr)

        mock_header = {'RG': [
            {'ID': '1', 'SM': 'AB'},
            {'ID': '2', 'SM': 'AA'},
            ]
        }
        with captured_output() as (_, stderr):
            logger = Logger.get_logger("CheckBamHeader")
            res = CheckBamHeader.check_header(mock_header, logger)
            self.assertTrue(res)
        stderr = stderr.getvalue()
        self.assertTrue('WARNING' in stderr)
        self.assertTrue("Multiple sample IDs detected" in stderr)


        ibam = get_test_data_path("test_bam_header_good.bam")
        bam = pysam.AlignmentFile(ibam, mode='rb')
        try:
            with captured_output() as (_, _):
                logger = Logger.get_logger("CheckBamHeader")
                res = CheckBamHeader.check_header(bam.header, logger)
                self.assertFalse(res)
        finally:
            bam.close()

    def test_build_new_header(self):
        mock_header = {'SQ': [{'SN': 'chr1', 'LN': 100}],
        'RG': [
            {'ID': '1', 'SM': 'AB'},
            {'ID': '2'},
            {'ID': '3', 'SM': 'BB'},
            ]
        }

        exp_header = {'SQ': [{'SN': 'chr1', 'LN': 100}],
        'RG': [
            {'ID': '1', 'SM': 'AB'},
            {'ID': '2', 'SM': 'AB'},
            {'ID': '3', 'SM': 'AB'},
            ]
        }
        aid = 'AB'
        res = CheckBamHeader.build_new_header(mock_header, aid)
        self.assertEqual(res, exp_header) 

        exp_header = {'HD': {'VN': '1.5', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chr1', 'LN': 100}], 'RG': [{'ID': '1', 'SM': 'AB'}, {'ID': '2', 'SM': 'AB'}]}
        ibam = get_test_data_path("test_bam_header_good.bam")
        bam = pysam.AlignmentFile(ibam, mode='rb')
        try:
            res = CheckBamHeader.build_new_header(bam.header, aid)
            self.assertEqual(res, exp_header) 
        finally:
            bam.close()

    def test_main(self):
        (fd, fn) = tempfile.mkstemp(suffix=".sam")
        ibam = get_test_data_path("test_bam_header_good.bam")
        aid = 'ABC'
        args = MockArgs(ibam, aid, fn) 
        try:
            with captured_output() as (_, stderr):
                CheckBamHeader.main(args)
            stderr = stderr.getvalue()
            self.assertTrue("No issues detected. No header written." in stderr) 
            self.assertEqual(os.stat(fn).st_size, 0)
        finally:
            cleanup_files(fn)

        (fd, fn) = tempfile.mkstemp(suffix=".sam")
        ibam = get_test_data_path("test_bam_header_bad.bam")
        aid = 'ABC'
        args = MockArgs(ibam, aid, fn) 
        exp = """@HD	VN:1.5	SO:coordinate
              @SQ	SN:chr1	LN:100
              @RG	ID:1	SM:ABC
              @RG	ID:2	SM:ABC
              @RG	ID:3	SM:ABC
              """
        try:
            with captured_output() as (_, stderr):
                CheckBamHeader.main(args)
            stderr = stderr.getvalue()
            self.assertTrue("Multiple sample IDs detected" in stderr) 
            self.assertTrue("Detected RG problems, will create new header with SM ABC" in stderr)
            curr = pysam.AlignmentFile(fn)
            self.assertEqual(list(curr.header.keys()), ['HD', 'SQ', 'RG']) 
            self.assertEqual(len(curr.header['RG']), 3)
            self.assertEqual(list(set([i['SM'] for i in curr.header['RG']])), ['ABC'])
            curr.close()
        finally:
            cleanup_files(fn)

    def test_cli(self):
        (fd, fn) = tempfile.mkstemp(suffix=".sam")
        ibam = get_test_data_path("test_bam_header_good.bam")
        aid = 'ABC'
        try:
            with captured_output() as (_, stderr):
                main(args=['CheckBamHeader', '--input_bam', ibam, '--aliquot_id', aid, '--output_header', fn]) 
            stderr = stderr.getvalue()
            self.assertTrue("No issues detected. No header written." in stderr)
            self.assertTrue("[gdc_sanger_tools.main] - Finished!" in stderr)
            self.assertEqual(os.stat(fn).st_size, 0)
        finally:
            cleanup_files(fn)

        #(fd, fn) = tempfile.mkstemp(suffix=".sam")
        #ibam = get_test_data_path("test_bam_header_bad.bam")
        #aid = 'ABC'
        #args = MockArgs(ibam, aid, fn)
        #exp = """@HD    VN:1.5  SO:coordinate
        #      @SQ   SN:chr1 LN:100
        #      @RG   ID:1    SM:ABC
        #      @RG   ID:2    SM:ABC
        #      @RG   ID:3    SM:ABC
        #      """
        #try:
        #    with captured_output() as (_, stderr):
        #        CheckBamHeader.main(args)
        #    stderr = stderr.getvalue()
        #    self.assertTrue("Multiple sample IDs detected" in stderr)
        #    self.assertTrue("Detected RG problems, will create new header with SM ABC" in stderr)
        #    curr = pysam.AlignmentFile(fn)
        #    self.assertEqual(list(curr.header.keys()), ['HD', 'SQ', 'RG'])
        #    self.assertEqual(len(curr.header['RG']), 3)
        #    self.assertEqual(list(set([i['SM'] for i in curr.header['RG']])), ['ABC'])
        #    curr.close()
        #finally:
        #    cleanup_files(fn)
