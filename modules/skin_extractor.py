# modules/skin_extractor.py

import cv2
import numpy as np


class SkinExtractor:
    def __init__(self):
        self.SAMPLE_RADIUS = 15  # pixel radius to sample around each landmark

    def extract_skin_colours(self, detection_result):
        """
        Takes the result from FaceDetector and extracts
        average colour values from skin regions.
        Returns colour data in RGB, HSV and LAB colour spaces.
        """
        if not detection_result["success"]:
            return {"success": False, "error": "No face data provided"}

        image = detection_result["image"]
        regions = detection_result["regions"]

        all_pixels = []

        # Sample pixels around each landmark point in all regions
        for region_name, points in regions.items():
            for (x, y) in points:
                pixels = self._sample_pixels(image, x, y)
                all_pixels.extend(pixels)

        if not all_pixels:
            return {"success": False, "error": "Could not extract skin pixels"}

        # Convert to numpy array
        pixels_array = np.array(all_pixels, dtype=np.uint8)

        # Calculate average colour in BGR (OpenCV default)
        avg_bgr = np.mean(pixels_array, axis=0).astype(int)

        # Convert average colour to different colour spaces
        avg_rgb = self._bgr_to_rgb(avg_bgr)
        avg_hsv = self._bgr_to_hsv(avg_bgr)
        avg_lab = self._bgr_to_lab(avg_bgr)

        return {
            "success": True,
            "avg_rgb": avg_rgb.tolist(),
            "avg_hsv": avg_hsv.tolist(),
            "avg_lab": avg_lab.tolist(),
            "hex_colour": self._rgb_to_hex(avg_rgb),
            "pixel_count": len(all_pixels)
        }

    def _sample_pixels(self, image, x, y):
        """Sample pixels in a small radius around a point."""
        height, width = image.shape[:2]
        pixels = []

        for dy in range(-self.SAMPLE_RADIUS, self.SAMPLE_RADIUS):
            for dx in range(-self.SAMPLE_RADIUS, self.SAMPLE_RADIUS):
                nx, ny = x + dx, y + dy
                # Stay within image bounds
                if 0 <= nx < width and 0 <= ny < height:
                    pixel = image[ny, nx]  # BGR format
                    pixels.append(pixel)

        return pixels

    def _bgr_to_rgb(self, bgr):
        """Convert BGR to RGB."""
        pixel = np.array([[bgr]], dtype=np.uint8)
        return cv2.cvtColor(pixel, cv2.COLOR_BGR2RGB)[0][0]

    def _bgr_to_hsv(self, bgr):
        """Convert BGR to HSV."""
        pixel = np.array([[bgr]], dtype=np.uint8)
        return cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)[0][0]

    def _bgr_to_lab(self, bgr):
        """Convert BGR to LAB."""
        pixel = np.array([[bgr]], dtype=np.uint8)
        return cv2.cvtColor(pixel, cv2.COLOR_BGR2LAB)[0][0]

    def _rgb_to_hex(self, rgb):
        """Convert RGB array to hex colour string."""
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))