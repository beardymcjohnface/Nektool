nextflow.enable.dsl=2

process yeet {
  output: 
    stdout

  script:
  """
  echo ${params.input}
  """
}

workflow {
  yeet | view
}

