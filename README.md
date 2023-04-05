# convert2tea

Tries to convert from other package managers to tea package.yml

## Setup

	git clone https://github.com/magnusviri/convert2tea.git
	cd convert2tea
    git submodule init
    git submodule update
	pipenv shell

## Usage

Save openai api key.

	export OPENAI_API_KEY=sk-secret123ABC

Convert a lot of formula

	./convert2tea/convertLots.py

Convert 1 formula

	convert2tea language project filepath

- Language is one of: c, python, ruby, go, 
- project is the name of the folder to save the results
- filepath is the path to the brew .rb file to convert

Example.

	./convert2tea/convert2tea.py python ansible.com filepath homebrew-core/Formula/ansible.rb

It will print out the prompt it will use and then it will send it to ChatGPT and save the prompt to output/ansible.com/prompt-0.yml and result to output/ansible.com/package-0.yml.It will repeat this 3 times.

## Detailed usage

```
usage: convert2tea [-h] [-v] [-n] language project filepath

Convert formula to tea using AI

positional arguments:
  language       Language: i.e. c, python, ruby, go
  project        Project name
  filepath       Path to Homebrew .rb formula to convert

options:
  -h, --help     show this help message and exit
  -v, --version  print version and exit
  -n, --dry-run  print prompt and exit
```