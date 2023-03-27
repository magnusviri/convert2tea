#!/usr/bin/env python

"""
"""

__author__ = "James Reynolds"
__email__ = "magnusviri@me.edu"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.0.1"

from pprint import pprint
import jinja2
import re
import requests
import sys

from genericAIModel import GenericAIModel
import parser


def getPrompt(brew_example, tea_example, example_project, brew_source, project):
    environment = jinja2.Environment()
    template = environment.from_string(
        """You are PackageGPT, a large language model that understands software packages and how to build them from source.

    Follow the instructions.

    Here's an example ruby formula for the brew package manager for the project {{ example_project }}:

{% filter indent(width=8) %}
{{ brew_example }}
{% endfilter %}

    Here's an example package.yml yml for the tea package manager for the project {{ example_project }} built from source:

{% filter indent(width=8) %}
{{ tea_example }}
{% endfilter %}

    Here's an example ruby formula for the brew package manager for the project {{ project }}:

{% filter indent(width=8) %}
{{ brew_source }}
{% endfilter %}

    Provide a package.yml yml for the tea package manager for the project {{ project }} built from source:

    """
    )

    return template.render(
        example_project=example_project,
        brew_example=brew_example,
        tea_example=tea_example,
        brew_source=brew_source,
        project=project,
    )


def cleanupBrewFormula(formula):
    die = [
        {
            "start": "^.*bottle do$",
            "end": "^.*end$",
        },
        {
            "start": "^.*resource .* do$",
            "end": "^.*end$",
        },
        {
            "start": '^.*desc *"',
        },
        {
            "start": '^.*sha256 *"',
        },
        {
            "start": '^.*license *"',
        },
    ]
    wait_for = ""
    cleanedFormula = ""
    last_line = "asdf"
    for line in formula.splitlines():
        if wait_for == "":
            notFound = True
            for look_for in die:
                matches = re.match(look_for["start"], line)
                if matches:
                    if "end" in look_for:
                        wait_for = look_for["end"]
                    notFound = False
                    break
            if notFound:
                if last_line != "" and line != "":
                    cleanedFormula += line + "\n"
                    last_line = line
        else:
            matches = re.match(wait_for, line)
            if matches:
                wait_for = ""
    return cleanedFormula


def convertFiles(options):
    project, language = options.project[0], options.language[0]
    matches = re.match(
        "^https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/(.*).rb",
        options.url[0],
    )
    if matches:
        source_url = options.url[0]
    else:
        sys.stderr.write(
            f"Your url must begin with 'https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/' and end with '.rb'\n"
        )
        exit(-1)

    # Get source
    session = requests.Session()
    response = session.get(source_url)
    brew_source = cleanupBrewFormula(response.text)

    # Get example files
    templates = {
        "ruby": {
            "brew": "https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/asciidoctor.rb",
            "tea": "https://raw.githubusercontent.com/teaxyz/pantry/main/projects/asciidoctor.org/package.yml",
            "name": "asciidoctor",
        },
        "python": {
            "brew": "https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/twine-pypi.rb",
            "tea": "https://raw.githubusercontent.com/teaxyz/pantry/main/projects/github.com/pypa/twine/package.yml",
            "name": "twine",
        },
        "go": {
            "brew": "https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/glow.rb",
            "tea": "https://raw.githubusercontent.com/teaxyz/pantry/main/projects/charm.sh/glow/package.yml",
            "name": "glow",
        },
        "c": {
            "brew": "https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/aria2.rb",
            "tea": "https://raw.githubusercontent.com/teaxyz/pantry/main/projects/aria2.github.io/package.yml",
            "name": "aria2",
        },
    }
    if language not in templates:
        sys.stderr.write(f"Unknown language: {language}\n")
        exit(-1)
    example_project = templates[language]["name"]

    # brew example
    example1_url = templates[language]["brew"]
    response = session.get(example1_url)
    brew_example = cleanupBrewFormula(response.text)

    # tea example
    example2_url = templates[language]["tea"]
    response = session.get(example2_url)
    tea_example = response.text

    prompt = getPrompt(brew_example, tea_example, example_project, brew_source, project)
    print(prompt)

    if not options.dry_run:
        model = GenericAIModel("openai", "gpt-3.5-turbo-0301")
        result = model.query(prompt)
        print(result)


def main():
    options = parser.parse(sys.argv[1:])
    if options.version:
        print(__version__)
    else:
        result = convertFiles(options)


if __name__ == "__main__":
    main()
