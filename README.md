# Nektool
[Cookiecutter](https://github.com/cookiecutter/cookiecutter) profile for making a Nextflow-based bioinformatics tool

__See [Snaketool](https://github.com/beardymcjohnface/Snaketool) for a Snakemake-based template__

## Motivation

Writing reliable command line tools requires a lot of boilerplate to ensure input and generated
files are valid, catch errors with subprocesses, log stderr messages etc. It's very time-consuming and annoying.
Nextflow does a lot of heavy lifting in this regard and is an obvious alternative to a command line tool.

Building a Nextflow pipeline with a convenience launcher offers many advantages:
- Developing command line applications is quicker and easier
- Installing, running, and rerunning is easier and more convenient
- You can have subcommands for utility scripts and Nextflow workflows
- You can trick Snakemake users into running Nextflow
- Your pipelines have a proper command line interface and help message!

## Who is this for?

People who are already familiar with Nextflow and want to create either a Nextflow-powered command line 
tool or fancier Nextflow pipelines.

## Citation

This template is currently published as a preprint:

[https://doi.org/10.31219/osf.io/8w5j3](https://doi.org/10.31219/osf.io/8w5j3)

## Usage

To create a new tool from this template, use Cookiecutter and follow the prompts.

```shell
cookiecutter https://github.com/beardymcjohnface/Nektool.git
```

and here's what you get:

```text
my_nektool/
├── my_nektool
│   ├── __init__.py
│   ├── __main__.py
│   ├── util.py
│   ├── my_nektool.LICENSE
│   ├── my_nektool.VERSION
│   └── workflow
│       ├── nextflow.config
│       ├── params.yaml
│       └── workflow.nf
└── setup.py
```

The file `__main__.py` is the entry point.
Once installed with pip it will be accessible on command line, in this example as `my_nektool`.
Customise this file to add your own commandline options, help message etc.
If you only have one Snakefile you wish to run then this file will need very little customisation.

The directory `workflow/` contains an example Nextflow pipeline that will work with the example launcher.

## How the launcher works

The launcher first copies the default parameters and config files to the working directory which will allow the user to 
cusomise them if they wish. The launcher reads in these files and combines it with command-line arguments to pass on to 
Snakemake. In this example it only has one option to pass: `--input`. The Launcher updates the config files in the 
working directory which will be passed to Nextflow. The launcher uses the rest of the command line arguments 
to launch Nextflow. Most of the command line arguments are boilerplate for running Nextflow and do not require much if
any customisation.

## Customising your tool

__[Check out the wiki page](https://github.com/beardymcjohnface/Nektool/wiki/Customising-your-Nektool) for a detailed example on customising your Nektool.__

## Installing and testing your tool

For development, cd to your Snaketool directory and install with pip:

```shell
cd my_nektool/
pip install -e .
my_nektool --help
my_nektool run --help
```

Test run the template:

```shell
my_nektool run --input yeet
```

A slightly more interesting test using [any2fasta](https://github.com/tseemann/any2fasta) (in a conda environment) to convert a tiny FASTQ file to FASTA. 

```sh
my_nektool run --use-conda --input my_nektool/workflow/tiny.fastq -entry convert2fasta 
```

## Publishing your tool

Add your tool to pip and bioconda like you would any other python package.
Better instructions TBA, watch this space!
