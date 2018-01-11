# reference to Makefile automatic variables:
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html

OUTPUT_PREFIX := "lineages"
OUTPUT_FILE := "$(OUTPUT_PREFIX).csv.gz"
NAMES_OUTPUT_PREFIX := "names"
NAMES_OUTPUT_FILE := "$(NAMES_OUTPUT_PREFIX).csv.gz"
TAXID_LINEAGES_OUTPUT_PREFIX := "taxid-lineages"
TAXID_LINEAGES_OUTPUT_FILE := "$(TAXID_LINEAGES_OUTPUT_PREFIX).csv.gz"
TAXID_LINEAGES_OUTPUT_SHELF := "$(TAXID_LINEAGES_OUTPUT_PREFIX).db"

all: md5sum

md5sum: $(OUTPUT_FILE)
	md5sum -b $< > $<.md5

$(OUTPUT_FILE) $(NAMES_OUTPUT_PREFIX) $(TAXID_LINEAGES_OUTPUT_FILE) $(TAXID_LINEAGES_OUTPUT_SHELF): taxdump
	python ncbitax2lin.py \
		--nodes-file taxdump/taxdump/nodes.dmp \
		--names-file taxdump/taxdump/names.dmp \
		-o $(OUTPUT_PREFIX) \
                --names-output-prefix $(NAMES_OUTPUT_PREFIX) \
                --taxid-lineages-output-prefix $(TAXID_LINEAGES_OUTPUT_PREFIX)

.PHONY: .FORCE
