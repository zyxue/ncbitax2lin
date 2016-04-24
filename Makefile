ncbitax2lin: taxdump
	python ncbitax2lin.py \
		--nodes-file taxdump/taxdump/nodes.dmp \
		--names-file taxdump/taxdump/names.dmp \
		-o lineages

.PHONY: .FORCE

taxdump: .FORCE
	$(MAKE) -C taxdump all
