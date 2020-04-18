from argparse import ArgumentParser, Namespace
from typing import NewType
from pysam import AlignmentHeader, AlignmentFile
from logging import Logger

# Argparser types
ArgParserT = NewType("ArgParserT", ArgumentParser)
NamespaceT = NewType("NamespaceT", Namespace)

# Pysam types
AlignmentFileT = NewType("AlignmentFileT", AlignmentFile)
AlignmentHeaderT = NewType("AlignmentHeaderT", AlignmentHeader)

# Logger types
LoggerT = NewType("LoggerT", Logger)
