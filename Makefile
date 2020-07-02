DEVICE_PORT=/dev/tty.usbserial*


deploy: remove
	ampy --port $(DEVICE_PORT) put fusion/

# Remove ignores errors if not existing
# (initial - in the recipe does this)
remove:
	-ampy --port $(DEVICE_PORT) rmdir fusion/ --missing-okay

