# -*- coding: utf-8 -*-

"""kacl.kacl-cli: provides entry point main()."""

import sys
import os
import kacl
import chalk

import click

@click.group()
@click.option('-c', '--config', required=False, default='.kacl.conf', type=click.Path(exists=False), help='Path to kacl config file', show_default=True)
@click.option('-f', '--file', required=False, default='CHANGELOG.md', type=click.Path(exists=False), help='Path to changelog file', show_default=True)
@click.pass_context
def cli(ctx, config, file):
    changelog_file = os.path.join(os.getcwd(), file)
    if not os.path.exists(changelog_file):
        click.echo( click.style("Error: ", fg='red')+ f"{changelog_file} not found" )
        sys.exit(1)

    kacl_changelog = kacl.load(changelog_file)
    ctx.obj['changelog'] = kacl_changelog
    ctx.obj['changelog_filepath'] = changelog_file

@cli.command()
@click.pass_context
@click.argument('section', type=str)
@click.argument('message', type=str)
@click.option('--inline', is_flag=True, help='This option will add the changes directly into changelog file')
def add(ctx, section, message, inline):
    kacl_changelog = ctx.obj['changelog']
    kacl_changelog_filepath = ctx.obj['changelog_filepath']

    # add changes to changelog
    kacl_changelog.add(section=section, content=message)
    kacl_changelog_content = kacl.dump(kacl_changelog)
    if inline:
        with open(kacl_changelog_filepath, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)

@cli.command()
@click.pass_context
@click.option('--json', required=False, default=False, type=bool, help='Print validation output as yaml')
@click.option('-o', '--output-file', required=False, type=click.Path(exists=False), help='Write verification output to file')
def verify(ctx, json, output_file):
    kacl_changelog = ctx.obj['changelog']
    kacl_changelog_filepath = ctx.obj['changelog_filepath']

    valid = kacl_changelog.is_valid()
    if not valid:
        validation = kacl_changelog.validate()

    for error in validation.errors():
        green = chalk.Chalk('green')
        red = chalk.Chalk('red')

        click.echo(kacl_changelog_filepath + ': ' + f'{error.line_number()}:0: ' + red + 'error: '  + chalk.RESET + error.error_message())
        if error.text():
            click.echo(error.text())
            click.echo(green + '^~~~~~~~~~~~~~~~~~~~' + chalk.RESET)

@cli.command()
@click.pass_context
@click.argument('version', type=str)
@click.option('--inline', is_flag=True, help='This option will add the changes directly into changelog file')
@click.option('-l', '--link', required=False, default=None, type=str, help='A url that the version will be linked with', show_default=True)
def release(ctx, version, inline, link):
    kacl_changelog = ctx.obj['changelog']
    kacl_changelog_filepath = ctx.obj['changelog_filepath']

    # release changes
    kacl_changelog.release(version=version, link=link)
    kacl_changelog_content = kacl.dump(kacl_changelog)
    if inline:
        with open(kacl_changelog_filepath, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)

def start():
    cli(obj={})

if __name__ == '__main__':
    start()