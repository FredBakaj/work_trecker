import os
import face_recognition
from core.script.person_definition import PersonDefinition

def get_image_names(folder_path):
    # Підтримувані розширення зображень
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    # Отримуємо список файлів у вказаній папці
    files = os.listdir(folder_path)
    # Відбираємо тільки файли з розширеннями зображень
    image_names = [file for file in files if file.lower().endswith(image_extensions)]

    return image_names

if __name__ == "__main__":
    person_id = int(input("person id => "))
    person_definition = PersonDefinition()
    persons_images_dir = "data/persons_images"
    image_names = get_image_names(persons_images_dir)
    person_embeddings = list()
    for img_name in image_names:
        file_path = f"{persons_images_dir}/{img_name}"
        img = face_recognition.load_image_file(file_path)
        person_embeddings.append(face_recognition.face_encodings(img)[0])

    person_definition.save_person_embedding(person_id, person_embeddings)