# gdc-sanger-somatic-tool
Support scripts for the sanger somatic workflows.

## Install

Using **python3**, run `pip install -r requirements.txt`

## Script Descriptions

### `extract_brass_vcf.py`

Extracts the brass VCF and renames TUMOUR to TUMOR. The final outputs are a
bgzipped vcf and its index.

```
extract_brass_vcf.py -h
[INFO] [20190710 15:11:25] [extract_brass_vcf] - --------------------------------------------------------------------------------
[INFO] [20190710 15:11:25] [extract_brass_vcf] - extract_brass_vcf.py
[INFO] [20190710 15:11:25] [extract_brass_vcf] - Program Args: scripts/extract_brass_vcf.py -h
[INFO] [20190710 15:11:25] [extract_brass_vcf] - --------------------------------------------------------------------------------
usage: Utility for extracting brass files from sanger results archive.
       [-h] --results_archive RESULTS_ARCHIVE --output_prefix OUTPUT_PREFIX

optional arguments:
  -h, --help            show this help message and exit
  --results_archive RESULTS_ARCHIVE
                        Sanger results tar archive.
  --output_prefix OUTPUT_PREFIX
                        Prefix for all outputs.
```

### `extract_caveman_vcf.py`

Extracts the caveman VCF and renames TUMOUR to TUMOR. The final outputs are a
bgzipped vcf and its index.

```
extract_caveman_vcf.py -h
[INFO] [20190710 15:11:25] [extract_caveman_vcf] - --------------------------------------------------------------------------------
[INFO] [20190710 15:11:25] [extract_caveman_vcf] - extract_caveman_vcf.py
[INFO] [20190710 15:11:25] [extract_caveman_vcf] - Program Args: scripts/extract_caveman_vcf.py -h
[INFO] [20190710 15:11:25] [extract_caveman_vcf] - --------------------------------------------------------------------------------
usage: Utility for extracting caveman files from sanger results archive.
       [-h] --results_archive RESULTS_ARCHIVE --output_prefix OUTPUT_PREFIX

optional arguments:
  -h, --help            show this help message and exit
  --results_archive RESULTS_ARCHIVE
                        Sanger results tar archive.
  --output_prefix OUTPUT_PREFIX
                        Prefix for all outputs.
```
