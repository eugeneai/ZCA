rm -fr zca.*
rm -fr zca-??.*

# # English
# rst2html2 --stylesheet=zope3.css izca.txt > zca.html
# rst2latex2 --use-latex-docinfo --use-latex-toc --stylesheet=style.tex --documentclass=book --use-latex-footnotes izca.txt > zca.tex
# pdflatex zca.tex
# pdflatex zca.tex

# # Spanish translation
# rst2html2 --stylesheet=zope3.css izca-es.txt > zca-es.html
# rst2latex2 --use-latex-docinfo --use-latex-toc --stylesheet=style.tex --documentclass=book --use-latex-footnotes izca-es.txt > zca-es.tex
# pdflatex zca-es.tex
# pdflatex zca-es.tex

# # French translation
# rst2html2 --stylesheet=zope3.css izca-fr.txt > zca-fr.html
# rst2latex2 --use-latex-docinfo --use-latex-toc --stylesheet=style.tex --documentclass=book --use-latex-footnotes izca-fr.txt > zca-fr.tex
# pdflatex zca-fr.tex
# pdflatex zca-fr.tex

# # Russian translation
# rst2html2 --stylesheet=zope3.css izca-ru.txt > zca-ru.html
# rst2latex2 --use-latex-docinfo --use-latex-toc --stylesheet=style.tex --documentclass=book --use-latex-footnotes --output-encoding=utf8 --documentoptions=10pt,a4paper,english,russian --font-encoding=T2A izca-ru.txt > zca-ru.tex
# pdflatex zca-ru.tex
# pdflatex zca-ru.tex

# Russian translation adopred to handbook processing
rst2latex2 --use-latex-docinfo --use-latex-toc --stylesheet=stylehb.tex --documentclass=extbook --output-encoding=utf8 --documentoptions=14pt,a4paper,openany,twoside,final --toc-entry-backlinks --footnote-backlinks --no-section-numbering --strip-comments --use-latex-citations --attribution=none --use-latex-abstract izca-ru.txt > zca-hb-ru.tex
lualatex --shell-escape zca-hb-ru.tex
lualatex --shell-escape zca-hb-ru.tex
