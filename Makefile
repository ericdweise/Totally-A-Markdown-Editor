SHELL=/bin/bash
SITE_DIR="${HOME}/.tame"
TAME_DIR=${HOME}/.local/bin
TAME="$(TAME_DIR)/tame"


.PHONY: depends remove-depends install install-site install-tame uninstall

depends:
	apt install -y pandoc python3 python3-pip
	pip3 install -r requirements.txt

remove-depends:
	pip3 uninstall -r requirements.txt
	apt purge -y pandoc python3 python3-pip

install: install-site install-tame

install-site:
	if ! [[ -d ${SITE_DIR} ]]; then \
		mkdir -p ${SITE_DIR}; \
	fi
	cp index.html $(SITE_DIR)
	cp README.md $(SITE_DIR)
	cp -r assets $(SITE_DIR)
	cp -r htbin $(SITE_DIR)

install-tame:
	if ! [[ -d ${TAME_DIR} ]]; then \
		mkdir -p ${TAME_DIR}; \
	fi
	cp tame $(TAME)
	if ! [[ $(PATH) == *${TAME_DIR}* ]]; then \
		echo '' >> "${HOME}/.profile"; \
		echo PATH='"${TAME_DIR}:$$PATH"' >> "${HOME}/.profile"
	fi

uninstall:
	rm -r $(SITE_DIR)
	rm $(TAME)


# Copy tame file to somewhere on the $PATH

