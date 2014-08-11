Implementation for [101 Companies](http://101companies.org/wiki/Contribution:bottle) for details.

Requirements
============

You will need [Python 3](https://www.python.org/) to run this contribution at all. If you are on a Unix system (e.g. Linux or Mac OSX), chances are that you already have it installed. The program will probably also appear to run with Python 2, but it'll start choking on strings coming from the web UI and blow up eventually.

You will also need [Bottle](http://bottlepy.org/) and [PyYAML](http://pyyaml.org/). Those can probably be installed with your distribution's package manager or Python's package manager pip.

Testing
=======

To ensure everything works, `cd` into this project's folder and run `test101.py`. This will test all available features and report the result.

Bottling
========

To run the most interesting feature of this contribution, namely the web UI, once again `cd` into the project's folder, run `bottle101.py` and then point your browser to [http://localhost:3000/], with JavaScript enabled.
