import fitz
import os
import sys
from PIL import Image
if sys.platform == "win32":
    import ctypes



def showError(message: str) -> None:
    if sys.platform == "win32":
        ctypes.windll.user32.MessageBoxW(0, message, "Errore", 0x10)
    
    else:
        print(f"Errore: {message}")


def getInputPath() -> str:
    try:
        if len(sys.argv) > 1:
            pdf_path = sys.argv[1].strip()
        else:
            pdf_path = input("Inserisci il percorso del file PDF: ").strip()

        if not os.path.isfile(pdf_path):
            raise FileNotFoundError("Il file specificato non esiste.")
        if not pdf_path.lower().endswith(".pdf"):
            raise ValueError("Il file non è un PDF valido.")

        return pdf_path
    
    except Exception as e:
        showError(f"{e}")
        sys.exit(1)


def getPdfInput(pdf_path: str, scale: float = 5.0) -> list[Image.Image]:
    pdf_data: list[Image.Image] = []
    
    try:
        doc: fitz.Document = fitz.open(pdf_path)
    
        for page_num in range(len(doc)):
            page: fitz.Page = doc[page_num]
            pix: fitz.Pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
            page_data: Image.Image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            pdf_data.append(page_data)
        doc.close()

    except Exception as e:
        showError(f"Errore durante la conversione del PDF: {e}")
        sys.exit(1)

    return pdf_data


def pdf2png(pdf_path: str, output_folder: str, pages_data: list[Image.Image]) -> None:
    try:
        output_name: str = os.path.splitext(os.path.basename(pdf_path))[0]
        os.makedirs(output_folder, exist_ok=True)

        width, height = pages_data[0].size

        cropped_images: list[Image.Image] = [
            pages_data[0].crop((width // 2, 0, width, height)),
            pages_data[1].crop((0, 0, width // 2, height)),
            pages_data[1].crop((width // 2, 0, width, height)),
            pages_data[0].crop((0, 0, width // 2, height))
        ]

        for i, cropped_image in enumerate(cropped_images):
            page_path: str = os.path.join(output_folder, f"{output_name}_pag{i + 1}.png")
            cropped_image.save(page_path, "PNG")
    
    except IndexError:
        showError("Il PDF non ha abbastanza pagine per la suddivisione corretta.")
        sys.exit(1)

    except Exception as e:
        showError(f"Errore durante il salvataggio delle immagini: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        pdf_path: str = getInputPath()
        output_folder: str = "output_images"

        pdf_data: list[Image.Image] = getPdfInput(pdf_path)
        pdf2png(pdf_path, output_folder, pdf_data)

    except Exception as e:
        showError(f"Errore: {e}")
