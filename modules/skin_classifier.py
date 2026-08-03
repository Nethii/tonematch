# modules/skin_classifier.py

import numpy as np


class SkinClassifier:
    def __init__(self):
        # Skin tone categories based on LAB colour space
        # L = lightness (0-100), a = green-red, b = blue-yellow
        self.skin_tones = [
            {
                "name": "Fair",
                "display": "Fair Skin",
                "l_range": (65, 100),
                "description": "Very light skin with cool or warm undertones"
            },
            {
                "name": "Light",
                "display": "Light Skin",
                "l_range": (55, 65),
                "description": "Light skin tone with visible undertones"
            },
            {
                "name": "Medium",
                "display": "Medium Skin",
                "l_range": (45, 55),
                "description": "Medium skin tone, neither too light nor too dark"
            },
            {
                "name": "Tan",
                "display": "Tan Skin",
                "l_range": (35, 45),
                "description": "Warm tan skin tone"
            },
            {
                "name": "Deep",
                "display": "Deep Skin",
                "l_range": (0, 35),
                "description": "Deep and rich skin tone"
            }
        ]

    def classify(self, skin_data):
        """
        Takes skin colour data and returns skin tone
        classification with undertone detection.
        """
        if not skin_data["success"]:
            return {"success": False, "error": "No skin data provided"}

        lab = skin_data["avg_lab"]
        rgb = skin_data["avg_rgb"]
        hsv = skin_data["avg_hsv"]

        # LAB values from OpenCV are scaled:
        # L: 0-255 (represents 0-100)
        # a: 0-255 (represents -128 to 127)
        # b: 0-255 (represents -128 to 127)

        # Convert OpenCV LAB to standard LAB
        l_value = (lab[0] / 255.0) * 100
        a_value = lab[1] - 128
        b_value = lab[2] - 128

        # Classify skin tone based on L value
        tone = self._classify_tone(l_value)

        # Detect undertone based on a and b values
        undertone = self._detect_undertone(a_value, b_value, rgb)

        return {
            "success": True,
            "skin_tone": tone["name"],
            "skin_tone_display": tone["display"],
            "description": tone["description"],
            "undertone": undertone["name"],
            "undertone_display": undertone["display"],
            "undertone_description": undertone["description"],
            "l_value": round(l_value, 2),
            "a_value": round(a_value, 2),
            "b_value": round(b_value, 2),
            "hex_colour": skin_data["hex_colour"],
            "avg_rgb": rgb
        }

    def _classify_tone(self, l_value):
        """Classify skin tone based on LAB lightness value."""
        for tone in self.skin_tones:
            if tone["l_range"][0] <= l_value <= tone["l_range"][1]:
                return tone
        # Default to medium if outside all ranges
        return self.skin_tones[2]

    def _detect_undertone(self, a_value, b_value, rgb):
        """
        Detect warm, cool or neutral undertone.
        - Warm: golden, peachy, yellow tones (high b, higher R)
        - Cool: pink, red, bluish tones (high a, higher B)
        - Neutral: balance of both
        """
        r, g, b_channel = rgb[0], rgb[1], rgb[2]

        # Calculate warm/cool indicators
        warm_score = b_value + (r - b_channel)
        cool_score = a_value + (b_channel - g)

        if warm_score > cool_score + 10:
            return {
                "name": "warm",
                "display": "Warm",
                "description": "Your skin has golden, peachy or yellow undertones"
            }
        elif cool_score > warm_score + 10:
            return {
                "name": "cool",
                "display": "Cool",
                "description": "Your skin has pink, red or bluish undertones"
            }
        else:
            return {
                "name": "neutral",
                "display": "Neutral",
                "description": "Your skin has a balanced mix of warm and cool undertones"
            }