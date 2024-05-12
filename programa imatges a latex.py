import os
import subprocess
import shutil

# Funció per mostrar les imatges
def llistar_imatges(imatges):
    print("Llista d'imatges trobades:")
    for i, imatge in enumerate(imatges, start=1):
        print(f"{i}. {imatge}")

def preparar_imatges(imatges, directori_desti):
    if not os.path.exists(directori_desti):
        os.makedirs(directori_desti)

    imatges_reanomenades = []
    for i, imatge in enumerate(imatges, start=1):
        extensio = os.path.splitext(imatge)[1]
        nou_nom = f"Figura{i}{extensio}"
        shutil.copyfile(imatge, os.path.join(directori_desti, nou_nom))
        imatges_reanomenades.append(nou_nom)

    return imatges_reanomenades

# Funció per crear el document LaTeX
def crear_pdf(imatges, titol, autor, data):
    latex_document = [
        "\\documentclass{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage{graphicx}",
        "\\usepackage{hyperref}",
        "\\title{" + titol + "}",
        "\\author{" + autor + "}",
        "\\date{" + data + "}",
        "\\begin{document}",
        "\\maketitle",
        "\\listoffigures",
        "\\newpage"
    ]

    for i, imatge in enumerate(imatges, start=1):
        latex_document.append(
            "\\begin{figure}[h!]\\centering\\includegraphics[width=0.5\\textwidth]{" + 
            imatge + "}\\caption{Figura " + str(i) + "}\\end{figure}"
        )

    latex_document.append("\\end{document}")

    with open("document.tex", "w") as file:
        file.write("\n".join(latex_document))

    # Compilar el document LaTeX a PDF
    subprocess.run(["pdflatex", "document.tex"])

# Directori actual
directori = os.getcwd()

# Cerca d'imatges en el directori
extensio_imatges = [".png", ".jpg", ".jpeg"]
imatges = [f for f in os.listdir(directori) if os.path.splitext(f)[1].lower() in extensio_imatges]

# Llistar les imatges en el terminal
llistar_imatges(imatges)

confirmacio = input("Vols generar el PDF amb aquestes imatges? (Y/N): ")
if confirmacio.lower() == 'y':
    # Crear una nova carpeta per a les imatges reanomenades
    imatges_reanomenades = preparar_imatges(imatges, "imatges_latex")
    crear_pdf(imatges_reanomenades, "Exercicis sistema dièdric", "Martí Carrasco", "Gener 2024")
    print("PDF generat amb èxit.")
else:
    print("Generació de PDF cancel·lada.")