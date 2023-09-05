
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
is_chart_model = load_model("model_weights/is_chart/keras_model.h5", compile=False)

# Load the labels
is_chart_class_names = open("model_weights/is_chart/labels.txt", "r").readlines()


# Load the model
model = load_model("model_weights/chart_classification/keras_model.h5", compile=False)

# Load the labels
class_names = open("model_weights/chart_classification/labels.txt", "r").readlines()


def processimages(image_path):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    return data


def is_chart(image_path):
    data =processimages(image_path)
    # Predicts the model
    prediction = is_chart_model.predict(data)
    index = np.argmax(prediction)
    class_name = is_chart_class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", int(class_name[2:]), end="")
    print("Confidence Score:", confidence_score)

    return True if int(class_name[2:]) == 1 else False

  

def chart_classif(image_path):
    data =processimages(image_path)
    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    # confidence_score = prediction[0][index]

    # # Print prediction and confidence score
    # print("Class:", class_name[2:], end="")
    # print("Confidence Score:", confidence_score)

    return class_name[2:]


def chart_extractor(pdf_path):
    folder_path = os.path.dirname(pdf_path)

    pdf_document = fitz.open(pdf_path)

    extracted_charts = []

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

            with open(path,'wb') as f:
              f.write(image_bytes)

            if is_chart(path):
              print(path)
              chart_type=chart_classif(path)
              chart_list={"page_no":page_number,"chart_type":chart_type[:-1],"chart_path":path}
              extracted_charts.append(chart_list)
            else:
              os.remove(path)

    return extracted_charts


list_ofcharts= chart_extractor("Wolters-Kluwer-2022-Annual Report-1 (1) (1).pdf")
print(list_ofcharts)