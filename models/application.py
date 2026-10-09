STATUS = ("applied", "interview")
ALLOWED_KEYS = ("company", "title", "date_applied", "status", "date_interview")

all_applications = [
    { 
        "id": 1, 
        "company": "Monefy", 
        "title": "Full-stack Developer", 
        "date_applied": "9/25/2026", 
        "status": "interview", 
        "date_interview": "10/6/2026" 
    },
    { 
        "id": 2, 
        "company": "Nagarro", 
        "title": "Junior Software Developer", 
        "date_applied": "10/7/2026", 
        "status": "applied", 
        "date_interview": None 
    }
]

# TODO Application model/class for ORM