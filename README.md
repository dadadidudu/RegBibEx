# <APP_NAME_PLACEHOLDER>

RegBibEx (RBX):
An HTML to BibTex extractor based on regular expressions

## Use-Case

RBX reads and extracts text from HTML files based on selectors, and then extracts information from this text to variables based on regular expressions.
For binding regular expressions to variables, this app uses the [RegexVariableBinder (RVB)](TODO Link).
These variables can then be written to a file.
In this project, the intended output is BibTex files.

The current use-case is to extract BibTex information for as many publications as possible from the (very large) set of publications in the document found on the
[website of the COPIUS project](https://copius.univie.ac.at/tools.php).

## Detailed description

TODO

## Usage

TODO

### Options

#### Defining an options file

The file to pass options to the app should be an UTF-8 text document consisting of the following sections:

* ``options``: common options for the app
* ``defaults``: default definitions that should be used in case specific definitions were not set for a given file
* any other section name will be matched to an input file of the same name (without file extension), the options defined in this section will only apply to that file

The start of a new section is defined by a line starting with the file name and ending in a colon ``:``.
Any options following this definition will be assigned to this section.

#### Available options

For ``options``:

* ``replace``:(char/string to be replaced)=(char/string to replace with). This will be done before the regex is evaluated. Multiple replace can be supplied with a comma ``,`` between them.
* ``flags`` The regex flags to use. (Currently not supported)

For ``defaults``:

* ``entrytype``: The default entry type of a new BibTex publication entry (i.e., the string after the ``@``, e.g. ``article``, ``book``, ``inproceedings``, etc.)
* ``citekey``: The bound variable to use as default citation key for the entry (i.e., the first string after the ``{`` )
* any default regular expression for a field with the given name

For a file:

* ``entrytype``: The entry type for this file only. Overrides the default. Optional.
* ``citekey``:  The citation key to use for this file only. Overrides the default. Optional.
* ``replace``: A text replacement option to apply to the selected texts of this file only. This replacement will be handled after the common replacement option, before the regex is evaluated.
* any HTML selector path, followed by a colon ``:`` and the regular expression to use for evaluating **all** texts under this selector. This selector path can be prefixed with a plus ``+`` to denote that the fields bound with that definition should be added to ALL other found BibTex publication entries.

## Further information

This project was realised during the course "Digitales und Quantitatives Arbeiten" (Digital and Quantitative Studies) in the winter term 2024 at the Institute for Finno-Ugric Studies, University of Vienna.

Dieses Projekt entstand im Rahmen der LVA "Digitales und Quantitatives Arbeiten" im WS24 am Institut für Finno-Ugristik, Universität Wien.
