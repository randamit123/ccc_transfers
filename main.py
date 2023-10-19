from pdfgrabber import PDFGrabber
from databasemaker import DatabaseMaker
from pdfminer.high_level import extract_text
from pdfcleaner import PDFCleaner


def main():
    print("Program Start:")
    grabber = PDFGrabber('UCI', 120, 'Computer Science, B.S.', 'CS', 0.2)
    grabber.get_pdfs()
    # cleaner = PDFCleaner()
    # cleaner.extract_text()

    # maker = DatabaseMaker('UCI', 'CS', id_to_key)
    # print("Database made succesfully")
    # maker.add_classes()
    # print("Program Ended")


if __name__ == '__main__':
    main()
