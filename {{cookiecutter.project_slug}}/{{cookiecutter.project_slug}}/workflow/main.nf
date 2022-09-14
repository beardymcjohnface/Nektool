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


process any2fasta {
  //conda environemnt
  conda 'bioconda::any2fasta=0.4.2'
  
  //singularity image
  container 'https://depot.galaxyproject.org/singularity/any2fasta:0.4.2--hdfd78af_3' 
  
  ////docker image
  //container 'quay.io/biocontainers/any2fasta:0.4.2--hdfd78af_3'                       

  input: path(FQ)

  output: stdout

  script:
  """
  which any2fasta
  any2fasta $FQ 
  """
}


workflow convert2fasta {
  Channel.fromPath(params.input) | any2fasta | view
}
