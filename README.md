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

### `extract_pindel_vcf.py`

Extracts the Pindel VCF and renames TUMOUR to TUMOR. The final outputs are a
bgzipped vcf and its index.

```
extract_pindel_vcf.py -h
[INFO] [20190715 15:19:48] [extract_pindel_vcf] - --------------------------------------------------------------------------------
[INFO] [20190715 15:19:48] [extract_pindel_vcf] - extract_pindel_vcf.py
[INFO] [20190715 15:19:48] [extract_pindel_vcf] - Program Args: scripts/extract_pindel_vcf.py -h
[INFO] [20190715 15:19:48] [extract_pindel_vcf] - --------------------------------------------------------------------------------
usage: Utility for extracting pindel files from sanger results archive.
       [-h] --results_archive RESULTS_ARCHIVE --output_prefix OUTPUT_PREFIX

optional arguments:
  -h, --help            show this help message and exit
  --results_archive RESULTS_ARCHIVE
                        Sanger results tar archive.
  --output_prefix OUTPUT_PREFIX
                        Prefix for all outputs.
```

### `extract_ascat.py`

Extracts the caveman copynumber file from the ASCAT directory and reformats it to the GDC standard.
Extracts two values from the ASCAT samplestatistics file and prints them to stdout.

```
[INFO] [20190711 18:21:39] [extract_ascat] - --------------------------------------------------------------------------------
[INFO] [20190711 18:21:39] [extract_ascat] - extract_ascat.py
[INFO] [20190711 18:21:39] [extract_ascat] - Program Args: scripts/extract_ascat.py -h
[INFO] [20190711 18:21:39] [extract_ascat] - --------------------------------------------------------------------------------
usage: extract_ascat.py [-h] {reformat_copynumber,extract_stats} ...

Tool to process Sanger WGS pipeline TAR output and produce GDC standard files
and metrics.

positional arguments:
  {reformat_copynumber,extract_stats}

optional arguments:
  -h, --help            show this help message and exit

[INFO] [20190711 18:22:07] [extract_ascat] - --------------------------------------------------------------------------------
[INFO] [20190711 18:22:07] [extract_ascat] - extract_ascat.py
[INFO] [20190711 18:22:07] [extract_ascat] - Program Args: scripts/extract_ascat.py reformat_copynumber -h
[INFO] [20190711 18:22:07] [extract_ascat] - --------------------------------------------------------------------------------
usage: extract_ascat.py reformat_copynumber [-h] [--input INPUT]
                                            [--output OUTPUT]
                                            [--gdcaliquot GDCALIQUOT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        path to file output from Sanger pipeline
  --output OUTPUT, -o OUTPUT
                        path for output file
  --gdcaliquot GDCALIQUOT, -g GDCALIQUOT
                        GDC Aliquot ID used to generate the file

[INFO] [20190711 18:22:34] [extract_ascat] - --------------------------------------------------------------------------------
[INFO] [20190711 18:22:34] [extract_ascat] - extract_ascat.py
[INFO] [20190711 18:22:34] [extract_ascat] - Program Args: scripts/extract_ascat.py extract_stats -h
[INFO] [20190711 18:22:34] [extract_ascat] - --------------------------------------------------------------------------------
usage: extract_ascat.py extract_stats [-h] [--input INPUT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        path to file output from Sanger pipeline
```

### `extract_brass_bedpe.py`

Extracts the brass bedpe file, formats the header and outputs bgzipped + tabix indexed file.

```
 extract_brass_bedpe.py -h
[INFO] [20190712 16:15:18] [extract_brass_bedpe] - --------------------------------------------------------------------------------
[INFO] [20190712 16:15:18] [extract_brass_bedpe] - extract_brass_bedpe.py
[INFO] [20190712 16:15:18] [extract_brass_bedpe] - Program Args: extract_brass_bedpe.py -h
[INFO] [20190712 16:15:18] [extract_brass_bedpe] - --------------------------------------------------------------------------------
usage: Utility for extracting brass bedpe file from sanger results archive.
       [-h] --results_archive RESULTS_ARCHIVE --output_prefix OUTPUT_PREFIX

optional arguments:
  -h, --help            show this help message and exit
  --results_archive RESULTS_ARCHIVE
                        Sanger results tar archive.
  --output_prefix OUTPUT_PREFIX
                        Prefix for all outputs.
```