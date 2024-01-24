import tabula
import pandas as pd
import os

def convert_pdf_to_excel(pdf_path, excel_path, pages="all"):
    csv_path = "temp.csv"
    tabula.convert_into(pdf_path, csv_path, output_format="csv", pages=pages)
    df = pd.read_csv(csv_path)
    df.to_excel(excel_path, index=False)
    os.remove(csv_path)


if __name__ == "__main__":

    pdf_file = "/home/lollo/Downloads/ESITO_QUIZ_6.pdf"
    excel_file = "ESITO_QUIZ_6.xlsx"

    for i in range(6, 11):
        pdf_file = "/home/lollo/Downloads/ESITO QUIZ {}.pdf".format(i)
        excel_file = "ESITO_QUIZ_{}.xlsx".format(i)
        convert_pdf_to_excel(pdf_file, excel_file)
