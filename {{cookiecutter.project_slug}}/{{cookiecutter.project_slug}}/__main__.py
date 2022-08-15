
"""
Entrypoint for {{cookiecutter.project_name}}
"""

import sys
import os
import subprocess
import yaml
from shutil import copyfile
from time import localtime, strftime

import click


"""MISC FUNCTIONS
You shouldn't need to tweak these much if at all
- Set a different default system config file in copy_config() if you need to"""


def nek_base(rel_path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), rel_path)


def print_version():
    with open(nek_base('{{cookiecutter.project_slug}}.VERSION'), 'r') as f:
        version = f.readline()
    click.echo('\n' + '{{cookiecutter.project_name}} version ' + version + '\n')


def msg(err_message):
    tstamp = strftime('[%Y:%m:%d %H:%M:%S] ', localtime())
    click.echo(tstamp + err_message)


def msg_box(splash, errmsg=None):
    msg('-' * (len(splash) + 4))
    msg(f'| {splash} |')
    msg(('-' * (len(splash) + 4)))
    if errmsg:
        click.echo('\n' + errmsg)


def append_config_block(nf_config = 'nextflow.config', scope=None, **kwargs):
    with open(nf_config, 'a') as f:
        f.write(scope.rstrip() + '{' + '\n')
        for k in kwargs:
            f.write(f'{k} = {kwargs[k]}\n')
        f.write('}\n')


def copy_config(local_config=None, system_config=None):
    msg(f'Copying system default config to {local_config}')
    copyfile(system_config, local_config)
    # if not os.path.isfile(local_config):
    #     msg(f'Copying system default config to {local_config}')
    #     copyfile(system_config, local_config)
    # else:
    #     msg(f'Config file {local_config} already exists. Using existing config file.')


def read_config(file):
    with open(file, 'r') as stream:
        _config = yaml.safe_load(stream)
    return _config


def write_config(_config, file):
    msg(f'Writing runtime config file to {file}')
    with open(file, 'w') as stream:
        yaml.dump(_config, stream)


class OrderedCommands(click.Group):
    """Preserve the order of subcommands when printing --help"""
    def list_commands(self, ctx: click.Context):
        return list(self.commands)


"""RUN A NEXTFLOW FILE
Hopefully you shouldn't need to tweak this function at all.
- You must provide a NextFlow file, all else is optional
- Highly recommend supplying a params file and a config file"""


def run_nextflow(paramsfile=None, configfile=None, nextfile_path=None, merge_config=None, threads=None, use_conda=False,
                  conda_frontend=None, conda_prefix=None, next_extra=None):
    """Run a NextFlow workfile"""
    nextflow_command = ['nextflow', 'run', nextfile_path]

    if paramsfile:
        # copy sys default params if needed
        copy_config(local_config=paramsfile, system_config=nek_base(os.path.join('workflow', 'params.yaml')))

        # read the params
        nf_config = read_config(paramsfile)

        # merge in command line params if provided
        if merge_config:
            nf_config.update(merge_config)

        # update params file
        write_config(nf_config, paramsfile)
        nextflow_command += ['-params-file', paramsfile]

        # display the runtime configuration
        msg_box('Runtime parameters', errmsg=yaml.dump(nf_config, Dumper=yaml.Dumper))

    if configfile:
        copy_config(local_config=configfile, system_config=nek_base(os.path.join('workflow', 'nextflow.config')))

        # add threads
        if threads:
            append_config_block(scope="executor", cpus=threads)

        # Use conda
        if use_conda:
            if conda_frontend == 'mamba':
                append_config_block(scope='conda', useMamba="true", cacheDir=conda_prefix)
            else:
                append_config_block(scope='conda', cacheDir=conda_prefix)

    # add any additional NextFlow commands
    if next_extra:
        nextflow_command += list(next_extra)

    # Run NextFlow!!!
    nextflow_command = ' '.join(str(nf) for nf in nextflow_command)
    msg_box('NextFlow command', errmsg=nextflow_command)
    if not subprocess.run(nextflow_command, shell=True).returncode == 0:
        msg('Error: NextFlow failed')
        sys.exit(1)
    else:
        msg('NextFlow finished successfully')
    return 0


"""COMMON OPTIONS
Any click options that will be used in more than one subcommand can be defined here.
"""


def common_options(func):
    """Common options decorator for use with click commands."""
    options = [
        click.option('--paramsfile', default='params.yaml', help='Custom config file', show_default=True),
        click.option('--configfile', default='nextflow.config', help='Custom config file', show_default=True),
        click.option('--threads', help='Number of threads to use', default=1, show_default=True),
        click.option('--use-conda/--no-use-conda', default=True, help='Use conda for NextFlow rules',
                     show_default=True),
        click.option('--conda-frontend',
                     type=click.Choice(['mamba', 'conda'], case_sensitive=True),
                     default='{{cookiecutter.conda_frontend}}', help='Specify Conda frontend', show_default=True),
        click.option('--conda-prefix', default=nek_base(os.path.join('workflow', 'conda')),
                     help='Custom conda env directory', type=click.Path(), show_default=False),
        click.argument('nf_args', nargs=-1)
    ]
    for option in reversed(options):
        func = option(func)
    return func


"""COMMAND LINE ARGS
Customise your launcher!
"""


@click.group(cls=OrderedCommands)
def cli():
    """For more options, run:
    {{cookiecutter.project_slug}} command --help"""
    pass


"""MAIN SCRIPT run()
Add or edit any command line args related to running the main script here, customise the epilog etc.
The only required input is --input which is simple passed to the config.
"""


EPILOG = """
\b
CLUSTER EXECUTION:
{{cookiecutter.project_slug}} run ... -profile [profile],[profile],...
For information on NextFlow config and profiles see:
https://www.nextflow.io/docs/latest/config.html#config-profiles
\b
RUN EXAMPLES:
Required:           {{cookiecutter.project_slug}} run --input [file]
Specify threads:    {{cookiecutter.project_slug}} run ... --threads [threads]
Disable conda:      {{cookiecutter.project_slug}} run ... --no-use-conda 
Add NextFlow args:  {{cookiecutter.project_slug}} run ... -log logDir -dockerize
Available targets:
    all             Run everything (default)
    print_targets   List available targets
"""


@click.command(epilog=EPILOG, context_settings={"ignore_unknown_options": True})
@click.option('--input', '_input', help='Input file/directory', type=str, required=True)
@common_options
def run(_input, paramsfile, configfile, threads, use_conda, conda_frontend, conda_prefix, nf_args, **kwargs):
    """Run {{cookiecutter.project_name}}"""
    # Config to add or update in configfile
    merge_config = {
        'input': _input,
    }

    # run!
    run_nextflow(
        nextfile_path=nek_base(os.path.join('workflow', 'workflow.nf')),   # Full path to NextFlow file
        paramsfile=paramsfile,
        configfile=configfile,
        merge_config=merge_config,
        threads=threads,
        use_conda=use_conda,
        conda_frontend=conda_frontend,
        conda_prefix=conda_prefix,
        next_extra=nf_args,
    )


"""SUBCOMMAND EXAMPLE
Copy the system default config file to working directory.
"""


@click.command()
@click.option('--configfile', default='config.yaml', help='Copy template config to file', show_default=True)
def config(configfile, **kwargs):
    """Copy the system default config file"""
    copy_config(configfile)


cli.add_command(run)
cli.add_command(config)


def main():
    print_version()
    cli()


if __name__ == '__main__':
    main()
