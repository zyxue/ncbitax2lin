This directory contains the following NCBI Taxonomy database dump files:

   taxdmp.zip
   taxdump.tar.Z
   taxdump.tar.gz

All these files containes exactly the same information and are arranged so
for the convenience of unpacking them on various operating environments.
In addition there are files:

   taxdmp.zip.md5
   taxdump.tar.Z.md5
   taxdump.tar.gz.md5

which contain MD5 sums for the corresponding archive files. These files
might be used to check correctness of the download of corresponding 
archive file.

taxdmp.zip
----------

Is intended for zip-capable utilities such as pkunzip, unzip, and WinZip.
These utilities are widely available in almost all operating environments.
To unpack it command-line pkunzip and unzip:

        pkunzip taxdmp.zip
or
        unzip taxdmp.zip

Note: pkunzip and/or unzip executables must be in the executable search path
and taxdmp.zip must be in the current directory. Files will be unzipped into
current directory. For desired dump files placement and more please refer to
the manual and/or option descriptions of pkunzip and unzip utilities.

taxdump.tar.Z
-------------

This file is to be unpacked by uncompress utility and subsequent tar 
archiver. These utilities are usually used in UNIX-like environment. 
Unpacking instructions follows:

           uncompress -c taxdump.tar.Z | tar xf - 

taxdump.tar.gz
--------------

This file is to be unpacked by GNU unzip utility and subsequent tar 
archiver. These utilities are usually used in UNIX-like environment. 
Unpacking instructions follows:

           gunzip -c taxdump.tar.gz | tar xf - 

The content of the archive
--------------------------

It may look like this:

citations.dmp
delnodes.dmp
division.dmp
gencode.dmp
merged.dmp
names.dmp
nodes.dmp
readme.txt

The readme.txt file gives a brief description of *.dmp files. These files
contain taxonomic information and are briefly described below. Each of the
files store one record in the single line that are delimited by "\t|\n"
(tab, vertical bar, and newline) characters. Each record consists of one 
or more fields delimited by "\t|\t" (tab, vertical bar, and tab) characters.
The brief description of field position and meaning for each file follows.

nodes.dmp
---------

This file represents taxonomy nodes. The description for each node includes 
the following fields:

	tax_id					-- node id in GenBank taxonomy database
 	parent tax_id				-- parent node id in GenBank taxonomy database
 	rank					-- rank of this node (superkingdom, kingdom, ...) 
 	embl code				-- locus-name prefix; not unique
 	division id				-- see division.dmp file
 	inherited div flag  (1 or 0)		-- 1 if node inherits division from parent
 	genetic code id				-- see gencode.dmp file
 	inherited GC  flag  (1 or 0)		-- 1 if node inherits genetic code from parent
 	mitochondrial genetic code id		-- see gencode.dmp file
 	inherited MGC flag  (1 or 0)		-- 1 if node inherits mitochondrial gencode from parent
 	GenBank hidden flag (1 or 0)            -- 1 if name is suppressed in GenBank entry lineage
 	hidden subtree root flag (1 or 0)       -- 1 if this subtree has no sequence data yet
 	comments				-- free-text comments and citations

names.dmp
---------
Taxonomy names file has these fields:

	tax_id					-- the id of node associated with this name
	name_txt				-- name itself
	unique name				-- the unique variant of this name if name not unique
	name class				-- (synonym, common name, ...)

division.dmp
------------
Divisions file has these fields:
	division id				-- taxonomy database division id
	division cde				-- GenBank division code (three characters)
	division name				-- e.g. BCT, PLN, VRT, MAM, PRI...
	comments

gencode.dmp
-----------
Genetic codes file:

	genetic code id				-- GenBank genetic code id
	abbreviation				-- genetic code name abbreviation
	name					-- genetic code name
	cde					-- translation table for this genetic code
	starts					-- start codons for this genetic code

delnodes.dmp
------------
Deleted nodes (nodes that existed but were deleted) file field:

	tax_id					-- deleted node id

merged.dmp
----------
Merged nodes file fields:

	old_tax_id                              -- id of nodes which has been merged
	new_tax_id                              -- id of nodes which is result of merging

citations.dmp
-------------
Citations file fields:

	cit_id					-- the unique id of citation
	cit_key					-- citation key
	pubmed_id				-- unique id in PubMed database (0 if not in PubMed)
	medline_id				-- unique id in MedLine database (0 if not in MedLine)
	url					-- URL associated with citation
	text					-- any text (usually article name and authors)
						-- The following characters are escaped in this text by a backslash:
						-- newline (appear as "\n"),
						-- tab character ("\t"),
						-- double quotes ('\"'),
						-- backslash character ("\\").
	taxid_list				-- list of node ids separated by a single space
