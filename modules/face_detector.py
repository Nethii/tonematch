# modules/face_detector.py

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceDetector:
    def __init__(self):
        # Landmark indices for key skin regions
        self.LEFT_CHEEK = [116, 123, 147, 187, 207]
        self.RIGHT_CHEEK = [345, 352, 376, 411, 427]
        self.FOREHEAD = [10, 67, 69, 104, 108]

        # New MediaPipe API
        base_options = python.BaseOptions(
            model_asset_path=self._get_model_path()
        )
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=1,
            min_face_detection_confidence=0.5
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def _get_model_path(self):
        import os
        import urllib.request

        model_path = "face_landmarker.task"

        if not os.path.exists(model_path):
            print("Downloading face landmarker model...")
            url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
            urllib.request.urlretrieve(url, model_path)
            print("Model downloaded successfully")

        return model_path

    def detect(self, image_path):
        """
        Takes an image path, detects the face and returns
        landmark positions for skin region extraction.
        Returns None if no face is detected.
        """
        # Read the image
        image = cv2.imread(image_path)

        if image is None:
            return {"success": False, "error": "Could not read image"}

        # Get image dimensions
        height, width = image.shape[:2]

        # Convert BGR to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        # Process with MediaPipe
        results = self.detector.detect(mp_image)

        if not results.face_landmarks:
            return {"success": False, "error": "No face detected in image"}

        # Get the first face landmarks
        face_landmarks = results.face_landmarks[0]

        # Convert normalised landmarks to pixel coordinates
        landmarks = []
        for landmark in face_landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            landmarks.append((x, y))

        # Extract specific region coordinates
        left_cheek_points = [landmarks[i] for i in self.LEFT_CHEEK]
        right_cheek_points = [landmarks[i] for i in self.RIGHT_CHEEK]
        forehead_points = [landmarks[i] for i in self.FOREHEAD]

        return {
            "success": True,
            "image": image,
            "image_path": image_path,
            "landmarks": landmarks,
            "regions": {
                "left_cheek": left_cheek_points,
                "right_cheek": right_cheek_points,
                "forehead": forehead_points
            },
            "dimensions": {"width": width, "height": height}
        }