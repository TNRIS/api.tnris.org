
pack-%:
	echo $(VIRTUAL_ENV)/lib/python3.6/site-packages/.
	echo ./$(subst pack-,,$(subst --,%,$@))/
	cp -r $(VIRTUAL_ENV)/lib/python3.6/site-packages/. ./$(subst pack-,,$(subst --,%,$@))/


PASSWORD_FILE := vault-password.txt
SECRETS_BUCKET := "tnris-secrets"
APP_NAME := api.tnris.org

FORCE:

.vault/.push/%: FORCE
	mkdir -p $(dir $@)
	cp src/data_hub/$(notdir $@) $@
	ansible-vault encrypt --vault-password-file $(PASSWORD_FILE) $@
	aws s3 cp $@ s3://$(SECRETS_BUCKET)/$(APP_NAME)/.vault/$(notdir $@)

push-secrets: \
	.vault/.push/set-env-secrets.sh \
	.vault/.push/gspread_config.json

.vault/.pull/%: FORCE
	mkdir -p $(dir $@)
	aws s3 cp s3://$(SECRETS_BUCKET)/$(APP_NAME)/.vault/$(notdir $@) $@

src/data_hub/%: .vault/.pull/%
	mkdir -p $(dir $@)
	ansible-vault decrypt --vault-password-file $(PASSWORD_FILE) $<
	mv $< $@

pull-secrets: \
	src/data_hub/set-env-secrets.sh \
	src/data_hub/gspread_config.json