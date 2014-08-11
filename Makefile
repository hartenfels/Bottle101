PYTHON_FILES = $(wildcard *.py)

all: html

html: public/web_ui.html

clean:
	rm -f public/web_ui.html

public/web_ui.html:
	GET https://rawgit.com/hartenfels/WebUI101/master/dist/web_ui.html > public/web_ui.html

.PHONY: all clean html
