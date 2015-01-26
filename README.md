CS241 MD to Book
================
Hi! This is a Python script designed to be a mindless, painfree way to convert the CS241 wikibook into a pdf suitable for heavier reading.

## Installation ##
### Prerequisites ###
- [pandoc](http://johnmacfarlane.net/pandoc/installing.html) should be installed and somewhere on your path
- [pdflatex](https://www.tug.org/texlive/acquire-netinstall.html) should be installed and somewhere on your path
- [git](http://git-scm.com/downloads) optionally should also be installed and on path if you want the script to pull the wikibook automatically


## Usage
- You only need ```autobook.py``` and ```base.tex```.
- Run the script
    - If you want to provide the mds:
        - Download the mds and put them in a folder somewhere. On Windows, files with colons are not supported so you will have to delete the colons on a different platform before the mds can be used.
        - ```./autobook.py path_to_mds tex_source```
    - If you want the script to clone the mds for you:
        - ```./autobook.py -c md_source tex_source```
- The pdf will be output as ```tex_source/base.pdf```
- ```./autobook.py -h``` for help
- On Windows, you may have to prepend all commands with ```python ```

