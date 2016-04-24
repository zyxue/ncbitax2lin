NCBI_URL=ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy


all: taxdump.tar.gz taxdump_readme.txt
	rm -rfv taxdump && mkdir -p taxdump && tar zxf $< -C ./taxdump

.PHONY: .FORCE

taxdump.tar.gz: .FORCE
	wget -N \
		$(NCBI_URL)/$@ \
		$(NCBI_URL)/$@.md5 \
	&& md5sum -c $@.md5


taxdump_readme.txt: .FORCE
	wget -N \
     $(NCBI_URL)/$@
