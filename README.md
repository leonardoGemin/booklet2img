# booklet2img – Converti PDF Opuscolo in Immagini 🖼️
`booklet2img` è un tool Python che converte automaticamente file PDF formato opuscolo in immagini, semplificando la gestione e l’estrazione delle pagine.

## Utilizzo da linea di comando
```bash
$ python booklet2img.py /path/to/input.pdf
```

## Utilizzo con file eseguibile
- Compila il sorgente con `pyinstaller`
```bash
$ pip install pyinstaller
$ pyinstaller --onefile --windowed booklet2img.py
```

- Converti l'opuscolo PDF in immagini trascinando il file da convertire sopra l'icona del file eseguibile

## Requisiti
- Sistema Operativo: Windows, macOS, Linux
- Python: 3.8+

Librerie di Python necessarie:
```bash
$ pip install pymupdf pillow
```
