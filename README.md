# NCBItax2lin

Convert NCBI taxonomy dump (taxdump, ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)
into lineages. An example for [human (tax_id=9606)](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=9606) is like

| tax_id | superkingdom | phylum   | class    | order    | family    | genus | species      | family1 | forma | genus1 | infraclass | infraorder  | kingdom | no rank            | no rank1     | no rank10            | no rank11 | no rank12 | no rank13 | no rank14 | no rank15     | no rank16 | no rank17 | no rank18 | no rank19 | no rank2  | no rank20 | no rank21 | no rank22 | no rank3  | no rank4      | no rank5   | no rank6      | no rank7   | no rank8     | no rank9      | parvorder  | species group | species subgroup | species1 | subclass | subfamily | subgenus | subkingdom | suborder    | subphylum | subspecies | subtribe | superclass | superfamily | superorder       | superorder1 | superphylum | tribe | varietas |
|--------|--------------|----------|----------|----------|-----------|-------|--------------|---------|-------|--------|------------|-------------|---------|--------------------|--------------|----------------------|-----------|-----------|-----------|-----------|---------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|---------------|------------|---------------|------------|--------------|---------------|------------|---------------|------------------|----------|----------|-----------|----------|------------|-------------|-----------|------------|----------|------------|-------------|------------------|-------------|-------------|-------|----------|
| 9606   | Eukaryota    | Chordata | Mammalia | Primates | Hominidae | Homo  | Homo sapiens |         |       |        |            | Simiiformes | Metazoa | cellular organisms | Opisthokonta | Dipnotetrapodomorpha | Tetrapoda | Amniota   | Theria    | Eutheria  | Boreoeutheria |           |           |           |           | Eumetazoa |           |           |           | Bilateria | Deuterostomia | Vertebrata | Gnathostomata | Teleostomi | Euteleostomi | Sarcopterygii | Catarrhini |               |                  |          |          | Homininae |          |            | Haplorrhini | Craniata  |            |          |            | Hominoidea  | Euarchontoglires |             |             |       |          |

## Download lineages

All pre-converted lineages are hosted on <a
href="https://gitlab.com/zyxue/ncbitax2lin-lineages/tree/master"
target="_blank">ncbitax2lin-lineages</a>, a [GitLab](https://gitlab.com/) repo,
which allows pushing larger files without [Git LFS](https://git-lfs.github.com/)
and a bigger repo size limit.

**Current release of generated lineage file:**

Available at **[https://gitlab.com/zyxue/ncbitax2lin-lineages/blob/master/lineages-2018-06-13.csv.gz](https://gitlab.com/zyxue/ncbitax2lin-lineages/blob/master/lineages-2018-06-13.csv.gz)**


## Regenerate the lineages yourself

Regeneration is straightforward, but it may incur quite a bit of memory (~20
GB). I generated `lineages.csv.gz` on a machine with 32 GB memory. Pull request
on refactoring to a lower memory usage is welcome. It's mainly about
[this line](https://github.com/zyxue/ncbitax2lin/blob/master/ncbitax2lin.py#L184),
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

## FAQ

**Q**: I have a large number of sequences with their corresponding accession
numbers from NCBI, how to get their lineages?

**A**: First, you need to map accession numbers (GI is deprecated) to tax IDs
based on `nucl_*accession2taxid.gz` files from
ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/. Secondly, you can trace a
sequence's whole lineage based on its tax ID. The tax-id-to-lineage mapping is
what NCBItax2lin generates for you, and it is available on <a
href="https://gitlab.com/zyxue/ncbitax2lin-lineages/tree/master"
target="_blank">ncbitax2lin-lineages</a>.

If you have any question about this project, please feel free to create a new
[issue](https://github.com/zyxue/ncbitax2lin/issues/new).

## Note on `taxdump.tar.gz.md5`

It appears that NCBI periodically regenerates `taxdump.tar.gz` and
`taxdump.tar.gz.md5` even when its content is still the same. I am not sure how
their regeneration works, but `taxdump.tar.gz.md5` will differ simply because 
of a different timestamp.
