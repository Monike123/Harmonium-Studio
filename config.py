# config.py

# ----------------------------------------
# 🎵 Basic Swar Frequencies (Middle Octave)
# ----------------------------------------
SWAR_FREQUENCIES = {
    'Sa': 261.63,
    'Re(k)': 277.18,
    'Re': 293.66,
    'Ga(k)': 311.13,
    'Ga': 329.63,
    'Ma': 349.23,
    'Ma(tivra)': 370.00,
    'Pa': 392.00,
    'Dha(k)': 415.30,
    'Dha': 440.00,
    'Ni(k)': 466.16,
    'Ni': 493.88,
    'Sa(upper)': 523.25
}

# ----------------------------------------
# Octave multipliers
# ----------------------------------------
OCTAVE_MULTIPLIERS = {
    'Mandra': 0.5,
    'Madhya': 1.0,
    'Tara': 2.0
}

# ----------------------------------------
# 🎨 Color Hue to Swar Mapping (0–179)
# ----------------------------------------
HUE_TO_SWAR = {
    (0, 10): 'Sa',     (11, 25): 'Re',   (26, 40): 'Ga',
    (41, 75): 'Ma',    (76, 100): 'Pa',  (101, 140): 'Dha',
    (141, 179): 'Ni'
}
SATURATION_THRESHOLD = 50
BRIGHTNESS_THRESHOLD = 50

# ----------------------------------------
# 🎼 Raga Library (20 ragas)
# ----------------------------------------
RAGA_LIBRARY = {
    'Yaman': {
        'thaat': 'Kalyan',
        'swars': ["Sa","Re","Ga","Ma(tivra)","Pa","Dha","Ni"],
        'aroha': ["Ni","Re","Ga","Ma(tivra)","Pa","Dha","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha","Pa","Ma(tivra)","Ga","Re","Sa"],
        'pakad': ["Ni","Re","Ga","Ma(tivra)"]
    },
    'Bhairavi': {
        'thaat': 'Bhairavi',
        'swars': ["Sa","Re(k)","Ga","Ma","Pa","Dha(k)","Ni(k)"],
        'aroha': ["Sa","Re(k)","Ga","Ma","Pa","Dha(k)","Ni(k)","Sa"],
        'avaroha': ["Sa","Ni(k)","Dha(k)","Pa","Ma","Ga","Re(k)","Sa"],
        'pakad': ["Sa","Re(k)","Ga","Ma"]
    },
    'Malkauns': {
        'thaat': 'Bhairav',
        'swars': ["Sa","Ga(k)","Ma","Dha(k)","Ni(k)"],
        'aroha': ["Sa","Ga(k)","Ma","Dha(k)","Ni(k)","Sa"],
        'avaroha': ["Sa","Ni(k)","Dha(k)","Ma","Ga(k)","Sa"],
        'pakad': ["Ga(k)","Ma","Dha(k)"]
    },
    'Kafi': {
        'thaat': 'Kafi',
        'swars': ["Sa","Re","Ga(k)","Ma","Pa","Dha","Ni(k)"],
        'aroha': ["Sa","Re","Ga(k)","Ma","Pa","Dha","Ni(k)","Sa"],
        'avaroha': ["Sa","Ni(k)","Dha","Pa","Ma","Ga(k)","Re","Sa"],
        'pakad': ["Sa","Re","Ga(k)"]
    },
    'Bageshri': {
        'thaat': 'Kafi',
        'swars': ["Sa","Re","Ga(k)","Ma","Pa","Dha","Ni(k)"],
        'aroha': ["Sa","Ga(k)","Ma","Dha","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha","Pa","Ma","Ga(k)","Re","Sa"],
        'pakad': ["Ma","Dha","Ni"]
    },
    'Darbari Kanada': {
        'thaat': 'Asavari',
        'swars': ["Sa","Re","Ga(k)","Ma","Pa","Dha(k)","Ni"],
        'aroha': ["Sa","Re","Ga(k)","Ma","Pa","Dha(k)","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha(k)","Pa","Ma","Ga(k)","Re","Sa"],
        'pakad': ["Re","Ga(k)","Re","Sa"]
    },
    'Puriya Dhanashri': {
        'thaat': 'Purvi',
        'swars': ["Sa","Re","Ga(k)","Ma(tivra)","Pa","Dha","Ni(k)"],
        'aroha': ["Ni","Re","Ga(k)","Ma(tivra)","Pa","Dha","Ni","Sa"],
        'avaroha': ["Sa","Ni(k)","Dha","Pa","Ma(tivra)","Ga(k)","Re","Sa"],
        'pakad': ["Re","Ga(k)","Ma"]
    },
    'Bhopali': {
        'thaat': 'Kalyan',
        'swars': ["Sa","Re","Ga","Pa","Dha"],
        'aroha': ["Sa","Re","Ga","Pa","Dha","Sa"],
        'avaroha': ["Sa","Dha","Pa","Ga","Re","Sa"],
        'pakad': ["Sa","Re","Ga"]
    },
    'Marwa': {
        'thaat': 'Marwa',
        'swars': ["Sa","Re(k)","Ga","Ma(tivra)","Pa","Dha","Ni"],
        'aroha': ["Sa","Re(k)","Ga","Ma(tivra)","Pa","Dha","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha","Pa","Ma(tivra)","Ga","Re(k)","Sa"],
        'pakad': ["Re(k)","Ga","Ma(tivra)"]
    },
    'Todi': {
        'thaat': 'Todi',
        'swars': ["Sa","Re(k)","Ga(k)","Ma(tivra)","Pa","Dha(k)","Ni"],
        'aroha': ["Sa","Re(k)","Ga(k)","Ma(tivra)","Pa","Dha(k)","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha(k)","Pa","Ma(tivra)","Ga(k)","Re(k)","Sa"],
        'pakad': ["Re(k)","Ga(k)","Ma(tivra)"]
    },
    'Bhairav': {
        'thaat': 'Bhairav',
        'swars': ["Sa","Re(k)","Ga","Ma","Pa","Dha(k)","Ni"],
        'aroha': ["Sa","Re(k)","Ga","Ma","Pa","Dha(k)","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha(k)","Pa","Ma","Ga","Re(k)","Sa"],
        'pakad': ["Sa","Re(k)","Ga"]
    },
    'Shree': {
        'thaat': 'Kalyan',
        'swars': ["Sa","Re","Ga","Ma","Pa","Dha(k)","Ni"],
        'aroha': ["Sa","Re","Ga","Ma","Pa","Dha(k)","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha(k)","Pa","Ma","Ga","Re","Sa"],
        'pakad': ["Pa","Ga","Ma"]
    },
    'Jaunpuri': {
        'thaat': 'Asavari',
        'swars': ["Sa","Re","Ga(k)","Ma","Pa","Dha","Ni(k)"],
        'aroha': ["Sa","Re","Ga(k)","Ma","Pa","Dha","Ni(k)","Sa"],
        'avaroha': ["Sa","Ni(k)","Dha","Pa","Ma","Ga(k)","Re","Sa"],
        'pakad': ["Ni(k)","Dha","Pa"]
    },
    'Charukeshi': {
        'thaat': 'Kafi',
        'swars': ["Sa","Re","Ga","Ma","Pa","Dha","Ni"],
        'aroha': ["Sa","Re","Ga","Ma","Pa","Dha","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha","Pa","Ma","Ga","Re","Sa"],
        'pakad': ["Ga","Ma","Pa"]
    },
    'Kedar': {
        'thaat': 'Kalyan',
        'swars': ["Sa","Re","Ga","Ma(tivra)","Pa","Dha","Ni"],
        'aroha': ["Sa","Re","Ga","Ma(tivra)","Pa","Ma(tivra)","Pa","Dha","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha","Pa","Ma(tivra)","Ga","Re","Sa"],
        'pakad': ["Ma(tivra)","Pa","Ma(tivra)"]
    },
    'Hamsadhwani': {
        'thaat': 'Kalyan',
        'swars': ["Sa","Re","Ga","Pa","Ni"],
        'aroha': ["Sa","Re","Ga","Pa","Ni","Sa"],
        'avaroha': ["Sa","Ni","Pa","Ga","Re","Sa"],
        'pakad': ["Sa","Re","Ni"]
    },
    'Durga': {
        'thaat': 'Kalyan',
        'swars': ["Sa","Re","Ma","Pa","Dha"],
        'aroha': ["Sa","Re","Ma","Pa","Dha","Sa"],
        'avaroha': ["Sa","Dha","Pa","Ma","Re","Sa"],
        'pakad': ["Sa","Re","Ma"]
    },
    'Bihag': {
        'thaat': 'Kalyan',
        'swars': ["Sa","Re","Ga","Ma","Pa","Dha","Ni"],
        'aroha': ["Sa","Re","Ga","Pa","Dha","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha","Pa","Ma","Ga","Re","Sa"],
        'pakad': ["Ga","Pa","Ga"]
    },
    'Bageshri Kanada': {
        'thaat': 'Asavari',
        'swars': ["Sa","Re","Ga(k)","Ma","Pa","Dha","Ni"],
        'aroha': ["Sa","Ga(k)","Pa","Ni","Sa"],
        'avaroha': ["Sa","Ni","Dha","Pa","Ma","Ga(k)","Re","Sa"],
        'pakad': ["Ga(k)","Pa","Ni"]
    }
}

# RAGA_LIBRARY now holds 20 ragas
