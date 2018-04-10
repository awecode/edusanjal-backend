DISTRICTS = [
    {
        "province": "1",
        "name": "Sagarmatha",
        "districts": [
            "Bhojpur",
            "Dhankuta",
            "Ilam",
            "Jhapa",
            "Khotang",
            "Morang",
            "Okhaldhunga",
            "Panchthar",
            "Sankhuwasabha",
            "Solukhumbu",
            "Sunsari",
            "Taplejung",
            "Terhathum",
            "Udayapur"
        ]
    },
    {
        "province": "2",
        "name": "Madhesh",
        "districts": [
            "Saptari",
            "Siraha",
            "Dhanusha",
            "Mahottari",
            "Sarlahi",
            "Rautahat",
            "Bara",
            "Parsa"
        ]
    },
    {
        "province": "3",
        "name": "Bagmati",
        "districts": [
            "Dolakha",
            "Ramechhap",
            "Sindhuli",
            "Kavrepalanchok",
            "Sindhupalchok",
            "Rasuwa",
            "Nuwakot",
            "Dhading",
            "Chitwan",
            "Makwanpur",
            "Bhaktapur",
            "Lalitpur",
            "Kathmandu"
        ]
    },
    {
        "province": "4",
        "name": "Gorkha",
        "districts": [
            "Baglung",
            "Gorkha",
            "Kaski",
            "Lamjung",
            "Manang",
            "Mustang",
            "Myagdi",
            "Nawalpur",
            "Parbat",
            "Syangja",
            "Tanahun"
        ]
    },
    {
        "province": "5",
        "name": "Lumbini",
        "districts": [
            "Arghakhanchi",
            "Banke",
            "Bardiya",
            "Dang",
            "Eastern Rukum",
            "Gulmi",
            "Kapilvastu",
            "Parasi",
            "Palpa",
            "Pyuthan",
            "Rolpa",
            "Rupandehi"
        ]
    },
    {
        "province": "6",
        "name": "Karnali",
        "districts": [
            "Dailekh",
            "Dolpa",
            "Humla",
            "Jajarkot",
            "Jumla",
            "Kalikot",
            "Mugu",
            "Salyan",
            "Surkhet",
            "Western Rukum"
        ]
    },
    {
        "province": "7",
        "name": "Khaptad",
        "districts": [
            "Achham",
            "Baitadi",
            "Bajhang",
            "Bajura",
            "Dadeldhura",
            "Darchula",
            "Doti",
            "Kailali",
            "Kanchanpur"
        ]
    }
]

ALL_DISTRICTS = [district for obj in DISTRICTS for district in obj['districts']]

DISTRICT_PAIRS = [(district, district) for district in ALL_DISTRICTS]
