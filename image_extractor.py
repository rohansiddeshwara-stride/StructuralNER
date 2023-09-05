import fitz  # PyMuPDF
import json
# import cv2
import os 

def extract_images(pdf_path):
    folder_path = os.path.dirname(pdf_path)

    if "images" not in os.listdir():
        os.mkdir("images")
    folder_path = os.path.join(folder_path,'images')
    pdf_document = fitz.open(pdf_path)

    extracted_images = []

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        image_list = page.get_images(full=True)

        # page_bboxes = []

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            ext=base_image["ext"]
            path=os.path.join(folder_path,f"image_{img_index}_{page_number}.{ext}")

            with open(path,'wb+') as f: 
                f.write(image_bytes)

            image_dict={"page_no":page_number,"image_path":path}
            extracted_images.append(image_dict)
            


    pdf_document.close()
    return extracted_images


pdf_path = "Wolters-Kluwer-2022-Annual Report-1.pdf"  # Replace with your PDF file path

list=extract_images(pdf_path)
print(list)


