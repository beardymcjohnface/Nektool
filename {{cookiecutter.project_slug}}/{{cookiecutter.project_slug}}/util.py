"""MISC FUNCTIONS
You shouldn't need to tweak these much if at all
"""

import sys
import os
import subprocess
import yaml
from shutil import copyfile
from time import localtime, strftime

import click


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

        # display the runtime params
        msg_box('Runtime parameters', errmsg=yaml.dump(nf_config, Dumper=yaml.Dumper))

    if configfile:
        copy_config(local_config=configfile, system_config=nek_base(os.path.join('workflow', 'nextflow.config')))

        # add threads
        if threads:
            append_config_block(scope="executor", cpus=threads)

        # Use conda
        if use_conda:
            if conda_frontend == 'mamba':
                append_config_block(scope='conda', useMamba='"true"', cacheDir=f'"{conda_prefix}"')
            else:
                append_config_block(scope='conda', cacheDir=f'"{conda_prefix}"')

        nextflow_command += ['-c', configfile]

        # display the runtime configuration
        msg_box('Launcher Configuration', errmsg=open(configfile, 'r').read())

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