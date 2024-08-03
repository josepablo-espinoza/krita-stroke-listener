# Define variables
TARGET = Krita-Stroke-Listener-Docker.zip
DIR = strokeListener

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Zip target
$(TARGET): $(DIR)/strokeListener.py $(DIR)/__init__.py $(DIR)/Manual.html strokeListener.desktop LICENSE
	@echo $(info Creating zip archive...)
	@mkdir -p tmp/$(DIR)
	@cp $(DIR)/strokeListener.py tmp/$(DIR)/
	@cp $(DIR)/__init__.py tmp/$(DIR)/
	@cp $(DIR)/Manual.html tmp/$(DIR)/
	@cp LICENSE tmp/$(DIR)/
	@cp strokeListener.desktop tmp/
	@cd tmp && zip -r ../$(TARGET) .
	@rm -rf tmp
	@echo $(info Zip archive created: $(TARGET))

# Clean target
clean:
	@echo "Cleaning up..."
	@rm -f $(TARGET)
	@rm -rf tmp
	@echo "Cleanup complete."
