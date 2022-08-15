
nextflow.enable.dsl=2

printIn = params.input

process yeet {
  output:
    stdout
  shell:
  """
  echo $printIn
  """
}

workflow {
  yeet | view
}

