# NCBItax2lin

Convert NCBI taxonomy dump (taxdump, ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)
into lineages. An example for human is like

| tax_id | superkingdom | phylum   | class    | order    | family    | genus | species      | family1 | forma | genus1 | infraclass | infraorder  | kingdom | no rank            | no rank1     | no rank10            | no rank11 | no rank12 | no rank13 | no rank14 | no rank15     | no rank16 | no rank17 | no rank18 | no rank19 | no rank2  | no rank20 | no rank21 | no rank22 | no rank3  | no rank4      | no rank5   | no rank6      | no rank7   | no rank8     | no rank9      | parvorder  | species group | species subgroup | species1 | subclass | subfamily | subgenus | subkingdom | suborder    | subphylum | subspecies | subtribe | superclass | superfamily | superorder       | superorder1 | superphylum | tribe | varietas |
|--------|--------------|----------|----------|----------|-----------|-------|--------------|---------|-------|--------|------------|-------------|---------|--------------------|--------------|----------------------|-----------|-----------|-----------|-----------|---------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|---------------|------------|---------------|------------|--------------|---------------|------------|---------------|------------------|----------|----------|-----------|----------|------------|-------------|-----------|------------|----------|------------|-------------|------------------|-------------|-------------|-------|----------|
| 9606   | Eukaryota    | Chordata | Mammalia | Primates | Hominidae | Homo  | Homo sapiens |         |       |        |            | Simiiformes | Metazoa | cellular organisms | Opisthokonta | Dipnotetrapodomorpha | Tetrapoda | Amniota   | Theria    | Eutheria  | Boreoeutheria |           |           |           |           | Eumetazoa |           |           |           | Bilateria | Deuterostomia | Vertebrata | Gnathostomata | Teleostomi | Euteleostomi | Sarcopterygii | Catarrhini |               |                  |          |          | Homininae |          |            | Haplorrhini | Craniata  |            |          |            | Hominoidea  | Euarchontoglires |             |             |       |          |

## Download lineages

To download the latest version of pre-converted lineages, click
[here](https://gitlab.com/zyxue/ncbitax2lin-lineages/repository/archive.zip?ref=master).
For older versions, please see <a
href="https://gitlab.com/zyxue/ncbitax2lin-lineages/tags"
target="_blank">here</a>.

All pre-converted lineages are hosted on
[ncbitax2lin-lineages](https://gitlab.com/zyxue/ncbitax2lin-lineages/tree/master),
a [GitLab](https://gitlab.com/) repo, which allows pushing larger files without
[Git LFS](https://git-lfs.github.com/) and a bigger repo size limit.

## Regenerate the lineages yourself

Regeneration is straightforward, but it may incur quite a bit of memory (~20
GB). I generated `lineages.csv.gz` on a machine with 32 GB memory. Pull request
on refactoring to a lower memory usage is welcome. It's mainly about
[this line](https://github.com/zyxue/ncbitax2lin/blob/dev/ncbitax2lin.py#L184),
where the `pool.map` takes places.

If you really need an updated version but without the hardware resources, you
could also notify me on github, and I will update it for you.

### Install

```
git clone git@github.com:zyxue/ncbitax2lin.git
cd ncbitax2lin/
```

#### Set up a virtual environment

Currently, it only works with `python2.7`, and needs
[pandas](http://pandas.pydata.org/), so make sure you are in a proper virtual
environment. If you have already these had one available, just use that
one.

Otherwise, you can create a new one with
[miniconda](https://conda.io/miniconda.html)/[anaconda](https://www.continuum.io/downloads)
(recommended),

```
conda create -y -p venv/ --file env-conda.txt
# or effectively the same
# conda create -y -p venv python=2 pandas
source activate venv/
```

or with [virtualenv + pip](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

```
virtualenv venv/
source venv/bin/activate
pip install -r env-pip.txt
```

### Regenerate
Then run the following, this will download the latest taxdump from NCBI, and run
the scripts to regenerate all latest lineages from it

``` 
make
```

## Note on `taxdump.tar.gz.md5`

It appears that NCBI periodically regenerates `taxdump.tar.gz` and
`taxdump.tar.gz.md5` even when its content is still the same. I am not sure how
their regeneration works, but `taxdump.tar.gz.md5` will differ simply because 
of a different timestamp.

The included `lineage.csv.gz` could be outdated. I may regernate it once in a
while, but you are encouraged to regenerate it to be ensured with all latest
lineage information.
