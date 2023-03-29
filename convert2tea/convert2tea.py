#!/usr/bin/env python

"""
Converts a brew formula to tea using a trained AI model.
"""

__author__ = "James Reynolds"
__email__ = "magnusviri@me.edu"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.0.1"

from pprint import pprint
import random
from jinja2 import Environment, PackageLoader
import re
import requests
import sys
import os

from genericAIModel import GenericAIModel
import myParser
import examples


def getPrompt(brew_example, tea_example, example_project, brew_source, project):
    environment = Environment(loader=PackageLoader('convert2tea',))
    template = environment.get_template("prompt-1-example.jinja2")
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


def convertFiles(language, project, url, dry_run):
    matches = re.match(
        "^https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/(.*).rb",
        url,
    )
    if matches:
        source_url = url
    else:
        sys.stderr.write(
            f"Your url must begin with 'https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/' and end with '.rb'\n"
        )
        exit(-1)

    # Get source
    print(source_url)
    session = requests.Session()
    response = session.get(source_url)
    if response.status_code != 200:
        sys.stderr.write(f"Unable to get source from {source_url}\n")
        exit(-1)
    brew_source = cleanupBrewFormula(response.text)

    # Get example files
    if language not in examples.examples:
        sys.stderr.write(f"Unknown language: {language}\n")
        exit(-1)
    random_example = random.choice(examples.examples[language])
    example_project = random_example["name"]

    # brew example
    example1_url = "https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/{}".format(random_example["brew"])
    print(example1_url)
    response = session.get(example1_url)
    if response.status_code != 200:
        sys.stderr.write(f"Unable to get source from {example1_url}\n")
        exit(-1)
    brew_example = cleanupBrewFormula(response.text)

    # tea example
    example2_url = "https://raw.githubusercontent.com/teaxyz/pantry/main/projects/{}/package.yml".format(random_example["tea"])
    print(example2_url)
    response = session.get(example2_url)
    if response.status_code != 200:
        sys.stderr.write(f"Unable to get source from {example2_url}\n")
        exit(-1)
    tea_example = response.text

    prompt = getPrompt(brew_example, tea_example, example_project, brew_source, project)
    print(prompt)

    if not dry_run:
        repeat = 3
        while True:
            print(f"Querying model for {project}...")
            model = GenericAIModel("openai", "gpt-3.5-turbo-0301")
            result = model.query(prompt)
            print(result)
            if not os.path.exists(f"output/{project}"):
               os.makedirs(f"output/{project}")
            counter = 0
            while True:
                fname = f"output/{project}/package-{counter}.yml"
                fname2 = f"output/{project}/prompt-{counter}.txt"
                if not os.path.isfile(fname):
                    break
                counter += 1
            with open(fname, 'w') as file:
                file.write(result)
            with open(fname2, 'w') as file:
                file.write(prompt)
            success = re.search(r"distributable", result)
            if success:
                print("Success!")
                repeat -= 1
            if repeat == 0:
                break

def main():
    options = myParser.parse(sys.argv[1:])
    print(options)
    if options.version:
        print(__version__)
    else:
        convertFiles(options.project[0], options.language[0], options.url[0], options.dry_run)


if __name__ == "__main__":
    main()
