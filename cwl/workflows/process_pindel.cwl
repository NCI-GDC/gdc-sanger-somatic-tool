#!/usr/bin/env cwl-runner

cwlVersion: v1.0
doc: |
  Normalize and filter Pindel vcf.

class: Workflow

requirements:
  - class: InlineJavascriptRequirement
  - class: StepInputExpressionRequirement
  - class: SubworkflowFeatureRequirement
  - class: MultipleInputFeatureRequirement

inputs:
  output_prefix: string
  pindel_vcf:
    type: File
    secondaryFiles: [.tbi]
  reference:
    type: File
    secondaryFiles: [.fai, ^.dict]
  min_tumor_alt_dp:
    type: int?
    default: 3
    doc: If the tumor alt depth is less than this value filter it
  min_tumor_alt_dp_tag:
    type: string?
    default: TALTDP
    doc: The filter tag to use for the min_tumor_alt_dp filter
  usedecoy:
    type: boolean
    default: false
    doc: If specified, it will include all the decoy sequences in the faidx.

outputs:
    processed_pindel:
      type: File
      secondaryFiles: [.tbi]
      outputSource: gatk_filter/output_vcf

steps:
    prepare_intervals:
      run: ../tools/faidx_to_bed.cwl
      in:
        ref_fai:
          source: reference
          valueFrom: $(self.secondaryFiles[0])
        usedecoy: usedecoy
      out: [output_bed]

    select_variants:
      run: ../tools/gatk3-selectvariants.cwl
      in:
        input_vcf: pindel_vcf
        reference: reference
        intervals: prepare_intervals/output_bed
        output_filename:
          source: output_prefix
          valueFrom: $(self + '.raw_pindel.selected.raw_somatic_mutation.vcf.gz')
      out: [output_vcf]

    vt_normalization:
      run: ../tools/vt_norm.cwl
      in:
        input_vcf: select_variants/output_vcf
        reference_fasta: reference
        output_vcf:
          source: output_prefix
          valueFrom: $(self + '.raw_pindel.norm.raw_somatic_mutation.vcf')
      out: [output_vcf_file]

    gatk_filter:
      run: ../tools/gatk3-variant-filtration.cwl
      in:
        input_vcf: vt_normalization/output_vcf_file
        reference: reference
        min_tumor_alt_dp: min_tumor_alt_dp
        min_tumor_alt_dp_tag: min_tumor_alt_dp_tag
        output_filename:
          source: output_prefix
          valueFrom: $(self + '.raw_pindel.norm.filted.raw_somatic_mutation.vcf.gz')
      out: [output_vcf]
