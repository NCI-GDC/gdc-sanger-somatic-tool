#!/usr/bin/env cwl-runner

class: CommandLineTool
label: "vt normalize"
cwlVersion: v1.0
doc: |
    Normalize PINDEL VCF

requirements:
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/variant-filtration-tool:2.5
  - class: InlineJavascriptRequirement

inputs:
  input_vcf:
    type: File
    doc: "input vcf file"
    inputBinding:
      position: 0

  reference_fasta:
    type: File
    inputBinding:
      prefix: -r
      position: 1
    secondaryFiles: [.fai, ^.dict]

  output_vcf:
    type: string
    doc: output basename of vcf
    inputBinding:
      position: 2
      prefix: -o

outputs:
  output_vcf_file:
    type: File
    outputBinding:
      glob: $(inputs.output_vcf)

baseCommand: [/opt/vt/vt, normalize]
