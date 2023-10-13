from pdfgrabber import PDFGrabber
from databasemaker import DatabaseMaker


def main():
    print("Program Start:")
    grabber = PDFGrabber(120, 'Computer Science, B.S.', 'CS', 0.2)
    id_to_key = grabber.get_pdfs()
    # maker = DatabaseMaker('UCI', 'CS', id_to_key)
    print("check 3")
    # maker.add_classes()
    print("check 4")


if __name__ == '__main__':
    main()
