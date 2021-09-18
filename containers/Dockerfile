FROM texlive/texlive@sha256:023943e37a1812a8541284e12e0ace66a7600f36f468fd894aff4d473d91e0c4

RUN tlmgr install luatex85
RUN tlmgr install tikz-feynman
RUN tlmgr install standalone
RUN apt-get update -y && apt-get install -y pdf2svg librsvg2-bin

WORKDIR /app
COPY run run
RUN chmod +x run

# force download the fonts
WORKDIR /testapp
COPY warmpup.tex warmpup.tex
RUN lualatex warmpup.tex

WORKDIR /app
