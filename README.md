# RegBibEx (RBX): An HTML to BibTex extractor based on regular expressions

## Description and use-case

RBX reads and extracts text from an HTML file based on HTML selectors, and then extracts information from this text to variables based on regular expressions.
For binding regular expressions to variables, this app uses the [RegexVariableBinder (RVB)](TODO Link to own project).
These variables can then be written to a file.
In this project, the intended output is BibTex files.
Other writers can also be defined, as writing the files is decoupled from the extraction/conversion/binding process.

The current use-case is to extract BibTex information for as many publications as possible from the (very large) set of publications in the document found on the
[website of the COPIUS project](https://copius.univie.ac.at/tools.php).
This document has been exported to HTML from Microsoft Word. Both the original HTML file as well as the exported HTML file are supplied in this repository.

### Motivation

This project was realised during the course "Digitales und Quantitatives Arbeiten" (Digital and Quantitative Studies) in the winter term 2024 at the Institute for Finno-Ugric Studies, University of Vienna.

Dieses Projekt entstand im Rahmen der LVA "Digitales und Quantitatives Arbeiten" im WS24 am Institut für Finno-Ugristik, Universität Wien.

## Quickstart guide

1. Clone this repository: ``git clone https://github.com/dadadidudu/digiquant_FU.git``
2. Switch to the folder you just cloned into: ``cd digiquant_FU``
3. (optional, only if you want to use a python env) create environment: ``python3 -m venv .env``
4. Install dependencies: ``pip install -r requirements.txt``
5. Create an options file, file type can be any plaintext format. (See [next section](#defining-an-options-file) for defining the options file. See ``example_options.txt`` for an example file.)
6. Run program, supplying the options file as argument: ``py main.py example_options.txt``
7. For further options, run the program with the help flag: ``py main.py --help``

## Options

See ``example_options.txt`` for an example file.

### Defining an options file

The file to pass options to the app should be an UTF-8 text document consisting of the following sections:

* ``options``: Common options for the app
* ``defaults``: Default definitions that should be used in case specific definitions were not set for a given file
* Any other section name will be matched to an input file of the same name (without file extension), the options defined in this section will only apply to that file

The start of a new section is defined by a line starting with the file name and ending in a colon ``:``.
Any options following this definition will be assigned to this section.

### Available options

For ``options``:

* ``replace``:(char/string to be replaced)=(char/string to replace with). A string replacement that will be done for _every_ string read from the input during the binding step. Replacement will be done before the regex is evaluated. Multiple replace can be supplied with a comma ``,`` between them.
* ``flags`` The regex flags to use. (Currently not supported)

For ``defaults``:

* ``entrytype``: The default entry type of a new BibTex publication entry (i.e., the string after the ``@``, e.g. ``article``, ``book``, ``inproceedings``, etc.)
* ``citekey``: The bound variable to use as default citation key for the entry (i.e., the first string after the ``{`` in the BibTex entry)
* Any default regular expression for a field with the given name

For a file:

* ``entrytype``: The entry type for this file only. Overrides the default. Optional.
* ``citekey``:  The citation key to use for this file only. Overrides the default. Optional.
* ``replace``: A text replacement option to apply to the selected texts of this file only. This replacement will be handled after the common replacement option, before the regex is evaluated.
* any HTML selector path, followed by a colon ``:`` and the regular expression to use for evaluating **all** texts under this selector. This selector path can be prefixed with a plus ``+`` to denote that the fields bound with that definition should be added to ALL other found BibTex publication entries. If you want to define multiple regular expressions for the same HTML selector, it has to be a new key/value entry with the same HTML selector as key, but the new RegEx as value.

## Workflow: Detailed description

This is the current workflow of RBX

### Extraction of publications

Extracts the supplied HTML file to multiple HTML files each, according to a specific HTML tag.
Writes these to a given folder.
Optionally ignores certain indices of these files. E.g.: In the COPIUS input, the first index is the description, the second index is the TOC.

### Conversion of extracted files to UTF-8

The extracted HTML files will be converted from encoding `cp1252` used in the COPIUS input to `utf-8`. This is handled by BeautifulSoup.

### Get text under given HTML tags

All text found under the HTML tags given as path keys in the options file will be returned.

### Replace steps

First, the common replacement rules (``options.replace`` in options), then the file-specific replacement rules (``[filename].replace``) will be applied.

### Bind regex to variables

The regular expression(s) defined for the selector will be bound to variables with the given names.
Multiple regular expressions for one HTML selector can be defined by using the same selector path as key and the new RegEx as value. For this step, a seperate log-file (`binding.log`) will be written

### Choose "most plausible" regex result (if multiple RegEx defined)

If there are multiple regular expressions defined for the same HTML selector, the "most plausible" one will be [selected as described](#heuristic-selection-of-most-plausible-result). For this step, a seperate log-file (`selection.log`) will be written.

### Write variables to BibTex output

The variables found and bound according to the given regular expressions will be output to a `.bibtex` file for each file given in options.

## Current problems

### RegEx and the cyrillic alphabet

As regular expressions are predominantly anglo-spheric, it's much easier to define regular expressions for finding latin alphabet characters (esp. the ones used in the english alphabet) compared to non-english alphabet characters like e.g. `ß`, any combining characters, or characters from the cyrillic alphabet.

Compare, for example, that the RegEx `\w` for "any word character" _only_ matches `[a-zA-Z0-9_]`, which doesn't account for the aforementioned characters.

### Look-alike characters

Characters in the input HTML from COPIUS might look like a certain character, but might be coded as a different one than assumed (like e.g. `–` and `-`, as specified in the example options file).
Therefore, it might happen that no match is found even though the regular expression seems correct.

To mitigate that problem:

1. the replace feature has been implemented.
2. the `_binding.log` and `_selection.log` files will be written to the output directory. These will help to debug your regular expressions.

## Features and improvements for future development

### More testing for input/output encoding

The input/output encoding settings haven't yet been tested extensively.
The current defaults work well with the COPIUS dataset input.

### Commas not replaceable

Currently, commas can't be replaced (as comma is used as a seperator)

### RegEx flags not implemented

Implement regex flags (currently not supported, but also not needed explicitly)

### Support other formats than BibTex

Output files to a different format than BibTex

### Support more input encoding formats

Support for more input encoding formats

### HTML tags inside words will split the words

Currently, all plain text found under a given HTML selector will be collected as a line for every sub-selector each. This means, if for some reason, OCR or otherwise, words are split by a HTML tag mid-word (e.g. ````<p>Long<b>Word</b>WithTagsIn<p>si</p>de````), this translates to:

````txt
Long
Word
WithTagsIn
si
de
````

This makes the binding process fail in most cases.

__Possible solution__: It might be possible to concatenate these HTML sub-tags with one space instead of a line break. This would need testing.

### Heuristic selection of "most plausible result"

The selection of the "most plausible" result, if multiple RegEx are defined for the same HTML selector, is currently **very** heuristic and dependent on the quality of the regular expression. Currently it chooses the first object with the highest number of found variables.

This can maybe be improved in the future.
