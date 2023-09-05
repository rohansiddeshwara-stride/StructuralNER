import os
import fitz


def extract_pragraphs(pdf_path):

    pdf_document = fitz.open(pdf_path)
    pragraphs=[]
    # Iterate through each page in the PDF
    for page_number in range(0,10):
        page = pdf_document[page_number]

        for i in page.get_text('blocks'):
            if len(i[4].split())>4 and len(i[4])>80:
                page.draw_rect(i[0:4],color=(0,1,0),width=2)
                bbox= i[0:4]
                text=i[4]
                pragraph={"page_no":page_number,"bbox":bbox,"text":text}
                pragraphs.append(pragraph)
            # elif len(i[4]) < 80 and height>11.5 :
            #   page.draw_rect(i[0:4],color=(1,0,0),width=2)

        # zoom_x = 2.0 
        # zoom_y = 2.0  
        # mat = fitz.Matrix(zoom_x, zoom_y)  
        # pix = page.get_pixmap(matrix=mat)  
        # pix.save("page-%i.png" % page.number)


    pdf_document.close()
    return pragraphs

# Open the PDF file
pdf_path = 'Wolters-Kluwer-2022-Annual Report-1.pdf'
list_pragraphs=extract_pragraphs(pdf_path)
print(list_pragraphs)