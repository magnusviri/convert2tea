#!/usr/bin/env python

"""
Converts a brew formula to tea using a trained AI model.
"""

__author__ = "James Reynolds"
__email__ = "magnusviri@me.edu"
__copyright__ = "2023"
__license__ = "MIT"
__version__ = "0.1.1"

from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from langchain.llms import OpenAI
import os
import random
import re
import sys

import examples
import myParser


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


def convertFiles(language, project, filepath, dry_run):
    print(language, project, filepath, dry_run)
    # Get source
    print(filepath)
    brewfile = open(filepath, "r")
    brew_source = cleanupBrewFormula(brewfile.read())

    # initialize LLM
    #     llm = HuggingFaceHub(
    #         repo_id='google/flan-t5-xl',
    #         model_kwargs={'temperature':1e-10}
    #     )
    llm = OpenAI(temperature=0.9)

    repeat = 1
    while True:
        # Get example files
        if language not in examples.examples:
            sys.stderr.write(f"Unknown language: {language}\n")
            exit(-1)
        random_example = random.choice(examples.examples[language])
        example_project = random_example["name"]

        # brew example
        example1_url = "homebrew-core/Formula/{}".format(random_example["brew"])
        print(example1_url)
        example1file = open(example1_url, "r")
        brew_example = cleanupBrewFormula(example1file.read())

        # tea example
        example2_url = "pantry/projects/{}/package.yml".format(random_example["tea"])
        print(example2_url)
        example2file = open(example2_url, "r")
        tea_example = example2file.read()

        if not dry_run:
            prompt = PromptTemplate.from_file(
                input_variables=[
                    "brew_example",
                    "tea_example",
                    "example_project",
                    "brew_source",
                    "project",
                ],
                template_file="convert2tea/templates/prompt-1-example.lctemplate",
            )
            llm_chain = LLMChain(
                prompt=prompt,
                llm=llm,
            )
            print(f"Querying model for {project}, attempt {repeat}...")
            result = llm_chain.run(
                example_project=example_project,
                brew_example=brew_example,
                tea_example=tea_example,
                brew_source=brew_source,
                project=project,
            )
            print(result)

            # Ask it how well it did
            # result = llm_chain.run()

            if not os.path.exists(f"output/{project}"):
                os.makedirs(f"output/{project}")
            counter = 0
            while True:
                fname = f"output/{project}/package-{counter}.yml"
                fname2 = f"output/{project}/prompt-{counter}.txt"
                if not os.path.isfile(fname):
                    break
                counter += 1
            with open(fname, "w") as file:
                file.write(result)
            with open(fname2, "w") as file:
                file.write(
                    example_project + "\n\n" +
                    brew_example + "\n\n" +
                    tea_example + "\n\n" +
                    brew_source + "\n\n" +
                    project
                )

            success = re.search(r"distributable", result)
            if success:
                print("Success!")
                repeat += 1
        else:
            print("Success!")
            repeat += 1
        if repeat == 4:
            break


def main():
    options = myParser.parse(sys.argv[1:])
    print(options)
    if options.version:
        print(__version__)
    else:
        convertFiles(
            options.language[0],
            options.project[0],
            options.filepath[0],
            options.dry_run,
        )


if __name__ == "__main__":
    main()
