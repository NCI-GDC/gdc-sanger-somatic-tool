cwlVersion: v1.0
label: "GATK3 SelectVariants"
class: CommandLineTool

doc: |
    Runs GATK SelectVariants

requirements:
  - class: ShellCommandRequirement
  - class: InlineJavascriptRequirement
  - class: DockerRequirement
    dockerPull: quay.io/ncigdc/gatk3:3.6

inputs:
  input_vcf:
    type: File
    secondaryFiles: [.tbi]
    doc: Input PINDEL somatic VCF
    inputBinding:
      prefix: --variant
      position: 0

  reference:
    type: File
    doc: Reference fasta and incides
    inputBinding:
      prefix: -R
      position: 1
    secondaryFiles: [.fai, ^.dict]

  intervals:
    type: File
    inputBinding:
      prefix: -L
      position: 2

  output_filename:
    type: string
    doc: The name of out the output filtered VCF (automatically tabix-index if ends with gz)
    inputBinding:
      prefix: -o
      position: 3

outputs:
  output_vcf:
    type: File
    doc: The filtered VCF file
    outputBinding:
      glob: $(inputs.output_filename)
    secondaryFiles: [.tbi]

baseCommand: [java, -Xmx4G, -jar, /bin/GenomeAnalysisTK.jar, -T, SelectVariants, --disable_auto_index_creation_and_locking_when_reading_rods]
