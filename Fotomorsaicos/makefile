
run:
	@python3 src/Editor.py

ex:
	@pyinstaller --onefile src/Editor.py --hidden-import='PIL._tkinter_finder'

.PHONY: clean
clean:
	  @rm -rf build
		@rm -rf dist
		@rm -rf src/__pycache__

install:
	sudo apt install python3
	sudo apt install python-tk
	sudo apt install python-pip
	sudo pip install pillow
	sudo pip install numpy
	sudo pip install pyinstaller
