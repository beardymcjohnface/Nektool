
nextflow.enable.dsl=2

printIn = params.input

process yeet {
  output:
    stdout
  conda 'conda-forge::zstd'
  shell:
  """
  echo $printIn
  """
}

workflow {
  yeet | view
}

