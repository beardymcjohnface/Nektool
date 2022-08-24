# Nektool
Cookiecutter profile for making a NextFlow-based bioinformatics tool

__See [Snaketool](https://github.com/beardymcjohnface/Snaketool) for a Snakemake-based template__

## Motivation

Writing reliable command line tools requires a lot of boilerplate to ensure input and generated
files are valid, catch errors with subprocesses, log stderr messages etc. It's very time-consuming and annoying.
NextFlow does a lot of heavy lifting in this regard and is an obvious alternative to a command line tool.

Building a NextFlow pipeline with a convenience launcher offers many advantages:
- Developing command line applications is quicker and easier
- Installing, running, and rerunning is easier and more convenient
- You can have subcommands for utility scripts and NextFlow workflows
- You can trick Snakemake users into running NextFlow
- Your pipelines have a proper command line interface and help message!

## Who is this for?

People who are already familiar with NextFlow and want to create either a NextFlow-powered commandline 
tool or fancier NextFlow pipelines.

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

The directory `workflow/` contains an example NextFlow pipeline that will work with the example launcher.

## How the launcher works

The launcher first copies the default parameters and config files to the working directory which will allow the user to 
cusomise them if they wish. The launcher reads in these files and combines it with command-line arguments to pass on to 
Snakemake. In this example it only has one option to pass: `--input`. The Launcher updates the config files in the 
working directory which will be passed to NextFlow. The launcher uses the rest of the command line arguments 
to launch NextFlow. Most of the command line arguments are boilerplate for running NextFlow and do not require much if
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

## Publishing your tool

Add your tool to pip and bioconda like you would any other python package.
Better instructions TBA, watch this space!
