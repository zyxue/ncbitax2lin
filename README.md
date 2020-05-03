# NCBItax2lin

Convert NCBI taxonomy dump into lineages. An example for [human
(tax_id=9606)](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=9606)
is like

| tax_id | superkingdom | phylum   | class    | order    | family    | genus | species      | family1 | forma | genus1 | infraclass | infraorder  | kingdom | no rank            | no rank1     | no rank10            | no rank11 | no rank12 | no rank13 | no rank14 | no rank15     | no rank16 | no rank17 | no rank18 | no rank19 | no rank2  | no rank20 | no rank21 | no rank22 | no rank3  | no rank4      | no rank5   | no rank6      | no rank7   | no rank8     | no rank9      | parvorder  | species group | species subgroup | species1 | subclass | subfamily | subgenus | subkingdom | suborder    | subphylum | subspecies | subtribe | superclass | superfamily | superorder       | superorder1 | superphylum | tribe | varietas |
|--------|--------------|----------|----------|----------|-----------|-------|--------------|---------|-------|--------|------------|-------------|---------|--------------------|--------------|----------------------|-----------|-----------|-----------|-----------|---------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|---------------|------------|---------------|------------|--------------|---------------|------------|---------------|------------------|----------|----------|-----------|----------|------------|-------------|-----------|------------|----------|------------|-------------|------------------|-------------|-------------|-------|----------|
| 9606   | Eukaryota    | Chordata | Mammalia | Primates | Hominidae | Homo  | Homo sapiens |         |       |        |            | Simiiformes | Metazoa | cellular organisms | Opisthokonta | Dipnotetrapodomorpha | Tetrapoda | Amniota   | Theria    | Eutheria  | Boreoeutheria |           |           |           |           | Eumetazoa |           |           |           | Bilateria | Deuterostomia | Vertebrata | Gnathostomata | Teleostomi | Euteleostomi | Sarcopterygii | Catarrhini |               |                  |          |          | Homininae |          |            | Haplorrhini | Craniata  |            |          |            | Hominoidea  | Euarchontoglires |             |             |       |          |

### Install

ncbitax2lin requires python-3.7

```
pip install -U ncbitax2lin
```

### Generate lineages

First download taxonomy dump from NCBI:

```bash
wget -N ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
mkdir -p taxdump && tar zxf taxdump.tar.gz -C ./taxdump
```

Then, run ncbitax2lin

```bash
ncbitax2lin taxdump/nodes.dmp taxdump/names.dmp
```

By default, the generated lineages will be saved to
`ncbi_lineages_[date_of_utcnow].csv.gz`. The output file can be overwritten with
`--output` option.


## FAQ

**Q**: I have a large number of sequences with their corresponding accession
numbers from NCBI, how to get their lineages?

**A**: First, you need to map accession numbers (GI is deprecated) to tax IDs
based on `nucl_*accession2taxid.gz` files from
ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/. Secondly, you can trace a
sequence's whole lineage based on its tax ID. The tax-id-to-lineage mapping is
what NCBItax2lin can generate for you.

If you have any question about this project, please feel free to create a new
[issue](https://github.com/zyxue/ncbitax2lin/issues/new).

## Note on `taxdump.tar.gz.md5`

It appears that NCBI periodically regenerates `taxdump.tar.gz` and
`taxdump.tar.gz.md5` even when its content is still the same. I am not sure how
their regeneration works, but `taxdump.tar.gz.md5` will differ simply because
of a different timestamp.

## Used in

* Mahmoudabadi, G., & Phillips, R. (2018). A comprehensive and quantitative exploration of thousands of viral genomes. ELife, 7. https://doi.org/10.7554/eLife.31955
