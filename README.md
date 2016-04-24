# NCBItax2lin

Convert NCBI taxonomy ([taxdump](ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)) into
lineages.

## Install

It only works with `python2.7` currently, and needs
[pandas](http://pandas.pydata.org/).

```
git clone git@github.com:zyxue/ncbitax2lin.git
```


### Regenerate `lineages.csv``

First, make sure you're in a proper py27 virtual environment with pandas. Then,

```
cd ncbitax2lin
make
```
