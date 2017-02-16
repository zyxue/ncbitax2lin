# NCBItax2lin

Convert NCBI taxonomy dump (taxdump, ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/)
into lineages.

Below are first 20 sample records in the generated `linages.csv.gz` ordered by
taxonomy id (`tax_id`).

```
$ zcat lineages.csv.gz | head -20
tax_id,superkingdom,phylum,class,order,family,genus,species,family1,forma,genus1,infraclass,infraorder,kingdom,no rank,no rank1,no rank10,no rank11,no rank12,no rank13,no rank14,no rank15,no rank16,no rank17,no rank18,no rank19,no rank2,no rank20,no rank21,no rank22,no rank3,no rank4,no rank5,no rank6,no rank7,no rank8,no rank9,parvorder,species group,species subgroup,species1,subclass,subfamily,subgenus,subkingdom,suborder,subphylum,subspecies,subtribe,superclass,superfamily,superorder,superorder1,superphylum,tribe,varietas
1,,,,,,,,,,,,,,root,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
2,Bacteria,,,,,,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
6,Bacteria,Proteobacteria,Alphaproteobacteria,Rhizobiales,Xanthobacteraceae,Azorhizobium,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
7,Bacteria,Proteobacteria,Alphaproteobacteria,Rhizobiales,Xanthobacteraceae,Azorhizobium,Azorhizobium caulinodans,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
9,Bacteria,Proteobacteria,Gammaproteobacteria,Enterobacterales,Erwiniaceae,Buchnera,Buchnera aphidicola,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
10,Bacteria,Proteobacteria,Gammaproteobacteria,Cellvibrionales,Cellvibrionaceae,Cellvibrio,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
11,Bacteria,Actinobacteria,Actinobacteria,Micrococcales,Cellulomonadaceae,Cellulomonas,Cellulomonas gilvus,,,,,,,cellular organisms,Terrabacteria group,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
13,Bacteria,Dictyoglomi,Dictyoglomia,Dictyoglomales,Dictyoglomaceae,Dictyoglomus,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
14,Bacteria,Dictyoglomi,Dictyoglomia,Dictyoglomales,Dictyoglomaceae,Dictyoglomus,Dictyoglomus thermophilum,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
16,Bacteria,Proteobacteria,Betaproteobacteria,Methylophilales,Methylophilaceae,Methylophilus,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
17,Bacteria,Proteobacteria,Betaproteobacteria,Methylophilales,Methylophilaceae,Methylophilus,Methylophilus methylotrophus,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
18,Bacteria,Proteobacteria,Deltaproteobacteria,Desulfuromonadales,Desulfuromonadaceae,Pelobacter,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,delta/epsilon subdivisions,,,,,,,,,
19,Bacteria,Proteobacteria,Deltaproteobacteria,Desulfuromonadales,Desulfuromonadaceae,Pelobacter,Pelobacter carbinolicus,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,delta/epsilon subdivisions,,,,,,,,,
20,Bacteria,Proteobacteria,Alphaproteobacteria,Caulobacterales,Caulobacteraceae,Phenylobacterium,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
21,Bacteria,Proteobacteria,Alphaproteobacteria,Caulobacterales,Caulobacteraceae,Phenylobacterium,Phenylobacterium immobile,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
22,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
23,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,Shewanella colwelliana,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
24,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,Shewanella putrefaciens,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
25,Bacteria,Proteobacteria,Gammaproteobacteria,Alteromonadales,Shewanellaceae,Shewanella,Shewanella hanedai,,,,,,,cellular organisms,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
```

Entries that involve *Homo sapiens* are

```
$ zcat lineages.csv.gz | \grep -i 'homo sapiens'
9606,Eukaryota,Chordata,Mammalia,Primates,Hominidae,Homo,Homo sapiens,,,,,Simiiformes,Metazoa,cellular organisms,Opisthokonta,Dipnotetrapodomorpha,Tetrapoda,Amniota,Theria,Eutheria,Boreoeutheria,,,,,Eumetazoa,,,,Bilateria,Deuterostomia,Vertebrata,Gnathostomata,Teleostomi,Euteleostomi,Sarcopterygii,Catarrhini,,,,,Homininae,,,Haplorrhini,Craniata,,,,Hominoidea,Euarchontoglires,,,,
63221,Eukaryota,Chordata,Mammalia,Primates,Hominidae,Homo,Homo sapiens,,,,,Simiiformes,Metazoa,cellular organisms,Opisthokonta,Dipnotetrapodomorpha,Tetrapoda,Amniota,Theria,Eutheria,Boreoeutheria,,,,,Eumetazoa,,,,Bilateria,Deuterostomia,Vertebrata,Gnathostomata,Teleostomi,Euteleostomi,Sarcopterygii,Catarrhini,,,,,Homininae,,,Haplorrhini,Craniata,Homo sapiens neanderthalensis,,,Hominoidea,Euarchontoglires,,,,
741158,Eukaryota,Chordata,Mammalia,Primates,Hominidae,Homo,Homo sapiens,,,,,Simiiformes,Metazoa,cellular organisms,Opisthokonta,Dipnotetrapodomorpha,Tetrapoda,Amniota,Theria,Eutheria,Boreoeutheria,,,,,Eumetazoa,,,,Bilateria,Deuterostomia,Vertebrata,Gnathostomata,Teleostomi,Euteleostomi,Sarcopterygii,Catarrhini,,,,,Homininae,,,Haplorrhini,Craniata,Homo sapiens ssp. Denisova,,,Hominoidea,Euarchontoglires,,,,
1035824,Eukaryota,Nematoda,Enoplea,Trichocephalida,Trichuridae,Trichuris,Trichuris sp. ex Homo sapiens JP-2011,,,,,,Metazoa,cellular organisms,Opisthokonta,,,,,,,,,,,Eumetazoa,,,,Bilateria,Protostomia,Ecdysozoa,,,,,,,,,Dorylaimia,,,,,,,,,,,,,,
1131344,Eukaryota,Chordata,Mammalia,,,,Homo sapiens x Mus musculus hybrid cell line,,,,,,Metazoa,cellular organisms,Opisthokonta,Dipnotetrapodomorpha,Tetrapoda,Amniota,unclassified Mammalia,,,,,,,Eumetazoa,,,,Bilateria,Deuterostomia,Vertebrata,Gnathostomata,Teleostomi,Euteleostomi,Sarcopterygii,,,,,,,,,,Craniata,,,,,,,,,
1383439,Eukaryota,Chordata,Mammalia,,,,Homo sapiens/Mus musculus xenograft,,,,,,Metazoa,cellular organisms,Opisthokonta,Dipnotetrapodomorpha,Tetrapoda,Amniota,unclassified Mammalia,,,,,,,Eumetazoa,,,,Bilateria,Deuterostomia,Vertebrata,Gnathostomata,Teleostomi,Euteleostomi,Sarcopterygii,,,,,,,,,,Craniata,,,,,,,,,
1573476,Eukaryota,Chordata,Mammalia,,,,Homo sapiens/Rattus norvegicus xenograft,,,,,,Metazoa,cellular organisms,Opisthokonta,Dipnotetrapodomorpha,Tetrapoda,Amniota,unclassified Mammalia,,,,,,,Eumetazoa,,,,Bilateria,Deuterostomia,Vertebrata,Gnathostomata,Teleostomi,Euteleostomi,Sarcopterygii,,,,,,,,,,Craniata,,,,,,,,,
```

So it's not a just single entry. The taxonomoy is not big, but kind of complex, have fun!

## Introduction

It appears that NCBI periodically regenerates `taxdump.tar.gz` and
`taxdump.tar.gz.md5` even when its content is still the same. I am not sure how
their regeneration works, but `taxdump.tar.gz.md5` will differ simply because 
of a different timestamp.

The included `lineage.csv.gz` could be outdated. I may regernate it once in a
while, but you are encouraged to regenerate it to be ensured with all latest
lineage information.

## Regenerate `lineages.csv.gz`

Regeneration is straightforward, but it may incur quite a bit of memory (~20
GB). I generated `lineages.csv.gz` on a machine with 32 GB memory. Pull request
on refactoring to a lower memory usage is welcome. It's mainly about this line
`lineages_dd = pool.map(find_lineage, df.tax_id.values)`. If anything, you
could notify me on github and I could regenerate it for you.

### Install

```
git clone git@github.com:zyxue/ncbitax2lin.git
cd ncbitax2lin/
```

#### Setting up a virtual environment

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

### Regeneration
Then run the following, this will download the latest taxdump from NCBI, and run
the scripts to regenerate all latest lineages from it

``` 
make
```

