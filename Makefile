
pack-%:
	echo $(VIRTUAL_ENV)/lib/python3.6/site-packages/.
	echo ./$(subst pack-,,$(subst --,%,$@))/
	cp -r $(VIRTUAL_ENV)/lib/python3.6/site-packages/. ./$(subst pack-,,$(subst --,%,$@))/
