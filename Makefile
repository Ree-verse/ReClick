# Variables
PYTHON := python
PIP := $(PYTHON) -m pip
PYINSTALLER := pyinstaller

# Directories
ASSETS_DIR := assets
SRC_DIR := src
ICON := $(ASSETS_DIR)/ReClick.ico
DIST_DIR := dist
BUILD_DIR := build

# Check if the icon exists, otherwise PyInstaller will throw an error
# Only apply icon on Windows
ICON_FLAG = $(shell if [ -f "$(ICON)" ] && [ "$(OS)" = "Windows_NT" ]; then echo "--icon=$(ICON)"; fi)

.PHONY: install build clean

# Install dependencies
install:
	$(PIP) install --upgrade pip
	$(PIP) install customtkinter keyboard mouse pyinstaller

# Build ReClick
build:
	@echo "Building ReClick..."
	$(PYINSTALLER) --noconfirm --onefile --windowed $(ICON_FLAG) --name "ReClick" $(SRC_DIR)/main.py

# Clean up build artifacts
clean:
	@echo "Cleaning up..."
	rm -rf $(DIST_DIR) $(BUILD_DIR) *.spec
	rm -rf __pycache__
