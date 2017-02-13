# reference to Makefile automatic variables:
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html


all: md5sum

md5sum: lineages.csv.gz
	md5sum -b $< > $<.md5

lineages.csv.gz: taxdump
	python ncbitax2lin.py \
		--nodes-file taxdump/taxdump/nodes.dmp \
		--names-file taxdump/taxdump/names.dmp \
		-o lineages

.PHONY: .FORCE

taxdump: .FORCE
	$(MAKE) -C taxdump all


clean:
	rm -fv *#
