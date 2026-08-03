# modules/recommender.py

class Recommender:
    def __init__(self):
        self.recommendations = {

            # ── FAIR SKIN ──────────────────────────────────────────
            "Fair": {
                "warm": {
                    "makeup": {
                        "foundation": ["Ivory", "Warm Ivory", "Porcelain"],
                        "lipstick": ["Peach", "Coral", "Warm Rose", "Nude Pink"],
                        "eyeshadow": ["Champagne", "Gold", "Bronze", "Warm Brown"]
                    },
                    "clothing": ["Warm White", "Peach", "Coral", "Camel",
                                 "Terracotta", "Olive Green", "Warm Beige"],
                    "hair": ["Golden Blonde", "Strawberry Blonde",
                             "Warm Auburn", "Honey Brown"]
                },
                "cool": {
                    "makeup": {
                        "foundation": ["Porcelain", "Cool Ivory", "Pink Ivory"],
                        "lipstick": ["Berry", "Rose", "Mauve", "Pink"],
                        "eyeshadow": ["Silver", "Lavender", "Soft Pink", "Cool Grey"]
                    },
                    "clothing": ["Pure White", "Icy Blue", "Lavender", "Soft Pink",
                                 "Navy", "Emerald", "Cool Grey"],
                    "hair": ["Platinum Blonde", "Ash Blonde",
                             "Cool Brown", "Blue Black"]
                },
                "neutral": {
                    "makeup": {
                        "foundation": ["Ivory", "Neutral Ivory", "Porcelain"],
                        "lipstick": ["Nude", "Soft Pink", "Light Rose", "Peach"],
                        "eyeshadow": ["Taupe", "Soft Brown", "Rose Gold", "Cream"]
                    },
                    "clothing": ["Off White", "Soft Pink", "Light Blue",
                                 "Mint", "Lavender", "Light Grey"],
                    "hair": ["Light Brown", "Neutral Blonde",
                             "Soft Auburn", "Chestnut"]
                }
            },

            # ── LIGHT SKIN ─────────────────────────────────────────
            "Light": {
                "warm": {
                    "makeup": {
                        "foundation": ["Warm Beige", "Natural Beige", "Sand"],
                        "lipstick": ["Coral", "Warm Peach", "Terracotta", "Warm Nude"],
                        "eyeshadow": ["Gold", "Bronze", "Copper", "Warm Taupe"]
                    },
                    "clothing": ["Camel", "Terracotta", "Warm Orange", "Olive",
                                 "Mustard Yellow", "Rust", "Warm Brown"],
                    "hair": ["Golden Brown", "Caramel", "Warm Chestnut",
                             "Honey Blonde"]
                },
                "cool": {
                    "makeup": {
                        "foundation": ["Cool Beige", "Rose Beige", "Pink Sand"],
                        "lipstick": ["Rose", "Berry", "Plum", "Cool Pink"],
                        "eyeshadow": ["Mauve", "Cool Taupe", "Silver", "Dusty Rose"]
                    },
                    "clothing": ["Navy Blue", "Royal Blue", "Emerald", "Burgundy",
                                 "Cool Grey", "Lavender", "Soft Teal"],
                    "hair": ["Ash Brown", "Cool Chestnut", "Dark Ash Blonde",
                             "Cool Auburn"]
                },
                "neutral": {
                    "makeup": {
                        "foundation": ["Beige", "Natural", "Warm Sand"],
                        "lipstick": ["Mauve", "Dusty Rose", "Neutral Nude",
                                     "Soft Coral"],
                        "eyeshadow": ["Taupe", "Warm Grey", "Rose", "Soft Gold"]
                    },
                    "clothing": ["Blush Pink", "Sage Green", "Dusty Blue",
                                 "Warm Taupe", "Soft Coral", "Cream"],
                    "hair": ["Medium Brown", "Soft Chestnut",
                             "Warm Ash Brown", "Neutral Auburn"]
                }
            },

            # ── MEDIUM SKIN ────────────────────────────────────────
            "Medium": {
                "warm": {
                    "makeup": {
                        "foundation": ["Golden Beige", "Warm Caramel", "Honey"],
                        "lipstick": ["Burnt Orange", "Warm Red", "Copper",
                                     "Deep Peach"],
                        "eyeshadow": ["Bronze", "Deep Gold", "Copper",
                                      "Warm Burgundy"]
                    },
                    "clothing": ["Orange", "Warm Red", "Yellow",
                                 "Olive Green", "Rust", "Deep Coral", "Brown"],
                    "hair": ["Caramel Brown", "Dark Honey", "Warm Dark Brown",
                             "Auburn"]
                },
                "cool": {
                    "makeup": {
                        "foundation": ["Cool Caramel", "Rose Tan", "Cool Honey"],
                        "lipstick": ["Deep Rose", "Plum", "Berry", "Wine"],
                        "eyeshadow": ["Purple", "Cool Bronze", "Navy",
                                      "Deep Mauve"]
                    },
                    "clothing": ["Cobalt Blue", "Purple", "Emerald",
                                 "Deep Teal", "Fuchsia", "Cool Brown"],
                    "hair": ["Cool Dark Brown", "Espresso",
                             "Deep Burgundy", "Blue Black"]
                },
                "neutral": {
                    "makeup": {
                        "foundation": ["Caramel", "Warm Tan", "Natural Honey"],
                        "lipstick": ["Terracotta", "Warm Mauve", "Brick Red",
                                     "Neutral Brown"],
                        "eyeshadow": ["Warm Brown", "Bronze", "Olive",
                                      "Neutral Gold"]
                    },
                    "clothing": ["Teal", "Deep Purple", "Forest Green",
                                 "Warm White", "Burnt Sienna", "Dusty Rose"],
                    "hair": ["Dark Brown", "Warm Espresso",
                             "Neutral Dark Auburn", "Soft Black"]
                }
            },

            # ── TAN SKIN ───────────────────────────────────────────
            "Tan": {
                "warm": {
                    "makeup": {
                        "foundation": ["Warm Tan", "Golden Tan", "Caramel"],
                        "lipstick": ["Deep Coral", "Warm Brown", "Brick",
                                     "Warm Copper"],
                        "eyeshadow": ["Deep Bronze", "Gold", "Warm Copper",
                                      "Deep Brown"]
                    },
                    "clothing": ["Bright Orange", "Deep Yellow", "Warm Red",
                                 "Olive", "Deep Rust", "Camel", "Brown"],
                    "hair": ["Deep Caramel", "Warm Dark Brown",
                             "Rich Auburn", "Deep Honey"]
                },
                "cool": {
                    "makeup": {
                        "foundation": ["Cool Tan", "Rose Brown", "Cool Caramel"],
                        "lipstick": ["Deep Plum", "Wine", "Deep Berry",
                                     "Cool Red"],
                        "eyeshadow": ["Deep Purple", "Navy", "Teal",
                                      "Cool Deep Brown"]
                    },
                    "clothing": ["Royal Purple", "Deep Teal", "Cobalt",
                                 "Fuchsia", "Deep Emerald", "Burgundy"],
                    "hair": ["Deep Cool Brown", "Blue Black",
                             "Deep Burgundy", "Cool Espresso"]
                },
                "neutral": {
                    "makeup": {
                        "foundation": ["Tan", "Neutral Tan", "Golden Brown"],
                        "lipstick": ["Brick Red", "Deep Nude", "Warm Wine",
                                     "Mocha"],
                        "eyeshadow": ["Bronze", "Deep Taupe", "Warm Gold",
                                      "Copper Brown"]
                    },
                    "clothing": ["Deep Teal", "Warm Burgundy", "Forest Green",
                                 "Deep Coral", "Rich Purple", "Warm Navy"],
                    "hair": ["Espresso", "Deep Auburn",
                             "Neutral Dark Brown", "Rich Black"]
                }
            },

            # ── DEEP SKIN ──────────────────────────────────────────
            "Deep": {
                "warm": {
                    "makeup": {
                        "foundation": ["Deep Golden", "Rich Ebony", "Warm Deep"],
                        "lipstick": ["Deep Orange", "Warm Burgundy", "Rich Copper",
                                     "Deep Brick"],
                        "eyeshadow": ["Rich Gold", "Deep Copper", "Warm Bronze",
                                      "Deep Orange"]
                    },
                    "clothing": ["Bright Yellow", "Bright Orange", "Warm Red",
                                 "Bright Green", "Deep Gold", "Rich Brown"],
                    "hair": ["Deep Auburn", "Rich Warm Brown",
                             "Warm Black", "Deep Copper"]
                },
                "cool": {
                    "makeup": {
                        "foundation": ["Cool Ebony", "Deep Cool Brown", "Rich Cool"],
                        "lipstick": ["Deep Plum", "Rich Berry", "Deep Wine",
                                     "Cool Burgundy"],
                        "eyeshadow": ["Deep Purple", "Royal Blue", "Teal",
                                      "Deep Jewel"]
                    },
                    "clothing": ["Bright White", "Royal Blue", "Deep Purple",
                                 "Bright Teal", "Hot Pink", "Emerald"],
                    "hair": ["Jet Black", "Deep Cool Brown",
                             "Deep Purple Tint", "Blue Black"]
                },
                "neutral": {
                    "makeup": {
                        "foundation": ["Ebony", "Rich Deep", "Neutral Deep Brown"],
                        "lipstick": ["Deep Mocha", "Rich Nude", "Warm Deep Red",
                                     "Deep Rose"],
                        "eyeshadow": ["Deep Bronze", "Rich Brown", "Deep Gold",
                                      "Neutral Deep"]
                    },
                    "clothing": ["Jewel Tones", "Deep Teal", "Rich Purple",
                                 "Warm White", "Deep Coral", "Forest Green"],
                    "hair": ["Natural Black", "Deep Espresso",
                             "Rich Dark Brown", "Deep Burgundy"]
                }
            }
        }

    def recommend(self, classification):
        """
        Takes classification result and returns
        personalised colour recommendations.
        """
        if not classification["success"]:
            return {"success": False, "error": "No classification data provided"}

        skin_tone = classification["skin_tone"]
        undertone = classification["undertone"]

        # Get recommendations for this skin tone and undertone
        if skin_tone in self.recommendations:
            if undertone in self.recommendations[skin_tone]:
                recs = self.recommendations[skin_tone][undertone]
            else:
                recs = self.recommendations[skin_tone]["neutral"]
        else:
            return {"success": False, "error": "Could not find recommendations"}

        return {
            "success": True,
            "skin_tone": classification["skin_tone_display"],
            "undertone": classification["undertone_display"],
            "undertone_description": classification["undertone_description"],
            "hex_colour": classification["hex_colour"],
            "makeup": recs["makeup"],
            "clothing": recs["clothing"],
            "hair": recs["hair"]
        }