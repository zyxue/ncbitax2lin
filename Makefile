# reference to Makefile automatic variables:
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html

OUTPUT_PREFIX := "lineages-$(shell date +"%Y-%m-%d")"
OUTPUT_FILE := "$(OUTPUT_PREFIX).csv.gz"

all: md5sum

md5sum: $(OUTPUT_FILE)
	md5sum -b $< > $<.md5

$(OUTPUT_FILE): taxdump
	python ncbitax2lin.py \
		--nodes-file taxdump/taxdump/nodes.dmp \
		--names-file taxdump/taxdump/names.dmp \
		-o $(OUTPUT_PREFIX)

.PHONY: .FORCE

taxdump: .FORCE
	$(MAKE) -C taxdump all
