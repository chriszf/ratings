PANDOC=pandoc
BASE_CSS=normalize.css
CUSTOM_CSS=tutorial.css
SOURCES=index.html stage1.html tipsy_03.html

all: $(SOURCES)

%.html: %.md
	$(PANDOC) $< -o $@ -c $(BASE_CSS) -c $(CUSTOM_CSS)
