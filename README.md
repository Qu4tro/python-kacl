# python-kacl

A tool for verifying and modifying changelog in the **K**keep**AC**hange**l**og format.

## Status

## Installation

`python-kacl` and it `kacl-cli` can be installed either

- from source
- via the pip package `python-kacl`
- docker

All approaches are described in detail within this section.

### From Source

```bash
git clone https://github.com/mschmieder/python-kacl
cd python-kacl
```

***Global Install**

```bash
pip3 install .
```

***Developer Mode**

```bash
pip3 install -e .
```

### Pip Package

The package can simply be retrieves using 

```bash
pip3 install python-kacl
```

### Docker

The kacl-cli requires [pony-stable](https://github.com/ponylang/pony-stable) to be installed.

```bash
docker pull mschmieder/kacl-cli:latest
```

The `kacl-cli` is defined as entrypoint. Therefore the image can be used like this

```bash
docker -v $(pwd):$(pwd) -w $(pwd) mschmieder/kacl-cli:latest verify
```

## CLI

```
Usage: kacl-cli [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --config PATH  Path to kacl config file  [default: .kacl.conf]
  -f, --file PATH    Path to changelog file  [default: CHANGELOG.md]
  --help             Show this message and exit.

Commands:
  add      Adds a given message to a specified unreleased section.
  get      Returns a given version from the Changelog
  new      Creates a new changlog.
  release  Creates a release for the latest 'unreleased' changes.
  verify   Veryfies if the changelog is in "keep-a-changlog" format.
```


## Create a Changelog

```
Usage: kacl-cli new [OPTIONS]

  Creates a new changlog.

Options:
  -o, --output-file PATH  File to write the created changelog to.
  --help                  Show this message and exit.
```

**Usage**

```bash
kacl-cli new
```

Creates the following changelog

```markdown
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
```

## Verify a Changelog

```
Usage: kacl-cli verify [OPTIONS]

  Veryfies if the changelog is in "keep-a-changlog" format. Use '--json' get
  JSON formatted output that can be easier integrated into CI workflows.
  Exit code is the number of identified errors.

Options:
  --json  Print validation output as yaml
  --help  Show this message and exit.
```

**Usage**

```bash
kacl-cli verify
```

**JSON Output**

```bash
kacl-cli verify --json
```

```json
{
    "errors": [
        {
            "end_character_pos": 8,
            "error_message": "Versions need to be decorated with a release date in the following format 'YYYY-MM-DD'",
            "line": "## 1.0.0",
            "line_number": 8,
            "start_char_pos": 0
        },
        {
            "end_character_pos": 10,
            "error_message": "\"Hacked\" is not a valid section for a version. Options are [Added,Changed,Deprecated,Removed,Fixed,Security]",
            "line": "### Hacked",
            "line_number": 12,
            "start_char_pos": 4
        }
    ],
    "valid": false
}
```

## Print a single release changelog

**Usage**

```bash
kacl-cli get 0.2.2
```

```markdown
## [0.2.2] - 2018-01-16

### Added

- Many prior version. This was added as first entry in CHANGELOG when it was added to this project.
```

## Add an entry to an unreleased section

```
Usage: kacl-cli add [OPTIONS] SECTION MESSAGE

  Adds a given message to a specified unreleased section. Use '--modify' to
  directly modify the changelog file.

Options:
  -m, --modify  This option will add the changes directly into changelog file
  --help        Show this message and exit.
```

**Usage**

```bash
kacl-cli add fixed 'We fixed some bad issues' --modify
kacl-cli add added 'We just added some new cool stuff' --modify
kacl-cli add changed 'And changed things a bit' --modify
```

## Prepare a Changelog for a Release

```
Usage: kacl-cli release [OPTIONS] VERSION

  Creates a release for the latest 'unreleased' changes. Use '--modify' to
  directly modify the changelog file.

Options:
  -m, --modify     This option will add the changes directly into changelog
                   file
  -l, --link TEXT  A url that the version will be linked with
  --help           Show this message and exit.
```

**Usage**

```bash
kacl-cli release 0.13.1
```

Example CHANGELOG.md (before):
```markdown
```

Example CHANGELOG.md (after):
```
```