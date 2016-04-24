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

### Sample records in `lineages.csv.gz`

Below are first 20 records in the generated linages.csv.gz ordered by taxonomy
id (`tax_id`).

```
$ zcat lineages.csv.gz | head -20
tax_id,superkingdom,phylum,class,order,family,genus,species,family1,forma,infraclass,infraorder,kingdom,no rank,no rank1,no rank10,no rank11,no rank12,no rank13,no rank14,no rank15,no rank16,no rank17,no rank18,no rank19,no rank2,no rank20,no rank21,no rank22,no rank3,no rank4,no rank5,no rank6,no rank7,no rank8,no rank9,parvorder,species group,species subgroup,subclass,subfamily,subgenus,subkingdom,suborder,subphylum,subspecies,subtribe,superclass,superfamily,superorder,superphylum,tribe,varietas
1,,,,,,,,,,,,,root,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
2,Bacteria,,,,,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
6,Bacteria,Proteobacteria,Alphaproteobacteria,Rhizobiales,Xanthobacteraceae,Azorhizobium,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
7,Bacteria,Proteobacteria,Alphaproteobacteria,Rhizobiales,Xanthobacteraceae,Azorhizobium,Azorhizobium caulinodans,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
9,Bacteria,Proteobacteria,Gammaproteobacteria,Enterobacteriales,Enterobacteriaceae,Buchnera,Buchnera aphidicola,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
10,Bacteria,Proteobacteria,Gammaproteobacteria,Cellvibrionales,Cellvibrionaceae,Cellvibrio,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
11,Bacteria,Actinobacteria,Actinobacteria,Micrococcales,Cellulomonadaceae,Cellulomonas,Cellulomonas gilvus,,,,,,cellular organisms,Terrabacteria group,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
13,Bacteria,Dictyoglomi,Dictyoglomia,Dictyoglomales,Dictyoglomaceae,Dictyoglomus,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
14,Bacteria,Dictyoglomi,Dictyoglomia,Dictyoglomales,Dictyoglomaceae,Dictyoglomus,Dictyoglomus thermophilum,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
16,Bacteria,Proteobacteria,Betaproteobacteria,Methylophilales,Methylophilaceae,Methylophilus,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
17,Bacteria,Proteobacteria,Betaproteobacteria,Methylophilales,Methylophilaceae,Methylophilus,Methylophilus methylotrophus,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
18,Bacteria,Proteobacteria,Deltaproteobacteria,Desulfuromonadales,Desulfuromonadaceae,Pelobacter,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,delta/epsilon subdivisions,,,,,,,,
19,Bacteria,Proteobacteria,Deltaproteobacteria,Desulfuromonadales,Desulfuromonadaceae,Pelobacter,Pelobacter carbinolicus,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,delta/epsilon subdivisions,,,,,,,,
20,Bacteria,Proteobacteria,Alphaproteobacteria,Caulobacterales,Caulobacteraceae,Phenylobacterium,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
21,Bacteria,Proteobacteria,Alphaproteobacteria,Caulobacterales,Caulobacteraceae,Phenylobacterium,Phenylobacterium immobile,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
22,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
23,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,Shewanella colwelliana,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
24,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,Shewanella putrefaciens,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
25,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,Shewanella hanedai,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
```


### About [taxdump](ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)

It appears that NCBI periodically regenerates `taxdump.tar.gz` and
`taxdump.tar.gz.md5` even though that its content are being the same. Not sure
how the regeneration works, but that `taxdump.tar.gz.md5` is different could
simply be due to different timestamp.
