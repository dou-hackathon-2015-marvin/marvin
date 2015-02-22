install_plugin:
	mkdir -p ~/.local/share/nautilus-python/extensions
	cp marvin/plugin/marvin_extension.py ~/.local/share/nautilus-python/extensions

restart:
	bash run.sh stop
	bash run.sh

restart_nautilus:
	killall nautilus

install: install_plugin restart restart_nautilus
	
