all: md5sum
	mkdir -p taxdump && tar zxf taxdump.tar.gz -C ./taxdump

.PHONY: .FORCE

taxdump.tar.gz taxdump.tar.gz.md5 taxdump_readme.txt: .FORCE
	wget -N \
     ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz \
     ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz.md5 \
     ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump_readme.txt

md5sum: taxdump.tar.gz.md5
	md5sum -c taxdump.tar.gz.md5


