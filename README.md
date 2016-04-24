# NCBItax2lin

Convert NCBI taxonomy ([taxdump](ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)) into
lineages.

## Install

It only works with `python2.7` currently, and needs
[pandas](http://pandas.pydata.org/).

```
git clone git@github.com:zyxue/ncbitax2lin.git
```


### Regenerate `lineages.csv.gz`

First, make sure you're in a proper py27 virtual environment with pandas. Then,

```
cd ncbitax2lin
make
```


### About [taxdump](ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)

It appears that NCBI periodically regenerates `taxdump.tar.gz` and
`taxdump.tar.gz.md5` even though that its content are being the same. Not sure
how the regeneration works, but that `taxdump.tar.gz.md5` is different could
simply be due to different timestamp.
