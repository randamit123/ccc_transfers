from pdfgrabber import PDFGrabber
from databasemaker import DatabaseMaker


def main():
    print("check 0")
    grabber = PDFGrabber(120, 'Computer Science, B.S.', 'CS', 0.2)
    print("check 1")
    grabber = grabber.get_pdfs()
    print("check 2")
    # maker = DatabaseMaker('UCI', 'CS', id_to_key)
    # maker.add_classes()


if __name__ == '__main__':
    main()
