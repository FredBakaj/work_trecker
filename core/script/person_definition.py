import os
import pickle

import face_recognition
import numpy as np
from numpy import ndarray


class PersonDefinition:
    def __init__(self):
        self.files_dir = "data/persons_embeddings"
        self.file_name = "person"
        self.persons_embeddings = self.get_persons_embedding()

    def face_encoding(self, img, face_location: tuple) -> ndarray:
        x_min, y_min, x_max, y_max = face_location
        face_location_ = (y_min, x_min, y_max, x_max)
        face_location_ = {face_location_}
        biden_encoding = face_recognition.face_encodings(img, known_face_locations=face_location_)
        biden_encoding = biden_encoding[0]
        return biden_encoding

    def person_id_2_name(self, person_id: int) -> str:
        persons: dict[int, str] = {0: "Unknown", 1: "Fred", 2: "Yra"}
        return persons[person_id]

    def detect_human_id(self, face_embedding) -> int:
        persons_embedding = self.persons_embeddings["persons_embedding"]
        persons_id = self.persons_embeddings["persons_id"]

        matches = face_recognition.compare_faces(persons_embedding, face_embedding)
        person_id: int = 0

        face_distances = face_recognition.face_distance(persons_embedding, face_embedding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            person_id = persons_id[best_match_index]
        return person_id

    def save_person_embedding(self, person_id: int, person_embeddings: list[ndarray]) -> None:
        data: dict[str, list] = dict()
        file_path = f"{self.files_dir}/{self.file_name}_{person_id}.pickle"
        assert not os.path.isfile(file_path)
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
        except:
            data["persons_id"] = list()
        for i in range(len(person_embeddings)):
            data["persons_id"].append(person_id)
        data["persons_embedding"] = person_embeddings

        with open(file_path, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def get_persons_embedding(self) -> dict[str, list] | None:
        result: dict[str, list] = dict()
        person_file_names = self._get_persons_embedding_file_name()
        is_first_file = True
        for file_name in person_file_names:
            file_path = f'{self.files_dir}/{file_name}'
            with open(file_path, 'rb') as f:
                data: dict[str, list] = pickle.load(f)
                if is_first_file:
                    for data_key in data.keys():
                        result[data_key] = list()
                    is_first_file = False
                for data_key in data.keys():
                    result[data_key] += data[data_key]
        return result

    def _get_persons_embedding_file_name(self):
        image_extensions = ('.pickle',)
        files = os.listdir(self.files_dir)
        image_names = [file for file in files if file.lower().endswith(image_extensions)]

        return image_names
