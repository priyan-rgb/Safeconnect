def analyze_complaint(text: str):
    """
    SafeConnect AI complaint analysis.

    Detects:
    - Category
    - Priority
    - Responsible authority
    """

    text_lower = text.lower()

    # -------------------------------
    # CYBER CRIME
    # -------------------------------
    cyber_keywords = [
        "cyber",
        "online fraud",
        "online scam",
        "scam",
        "fraud",
        "fake account",
        "fake social media",
        "social media account",
        "hacked",
        "hacking",
        "hack",
        "phishing",
        "otp",
        "password",
        "instagram",
        "facebook",
        "whatsapp",
        "digital fraud",
        "internet fraud",
        "upi fraud",
        "bank fraud"
    ]

    # -------------------------------
    # WOMEN SAFETY
    # -------------------------------
    women_safety_keywords = [
        "harass",
        "harassed",
        "harassing",
        "harassment",
        "stalk",
        "stalking",
        "stalked",
        "molestation",
        "women safety",
        "woman safety",
        "sexual harassment",
        "eve teasing",
        "threatening a woman",
        "abuse",
        "abused",
        "domestic violence"
    ]

    # -------------------------------
    # EMERGENCY SAFETY
    # -------------------------------
    emergency_keywords = [
        "emergency",
        "danger",
        "attack",
        "violence",
        "fight",
        "murder",
        "kidnap",
        "kidnapping",
        "robbery",
        "theft",
        "assault"
    ]

    # -------------------------------
    # STUDENT GRIEVANCE
    # -------------------------------
    student_keywords = [
        "student",
        "college",
        "school",
        "exam",
        "teacher",
        "professor",
        "faculty",
        "marks",
        "scholarship",
        "hostel",
        "education"
    ]

    # -------------------------------
    # LEGAL ASSISTANCE
    # -------------------------------
    legal_keywords = [
        "legal",
        "lawyer",
        "court",
        "case",
        "legal advice",
        "legal help",
        "law",
        "notice"
    ]

    # -------------------------------
    # PUBLIC SAFETY
    # -------------------------------
    public_safety_keywords = [
        "street light",
        "road",
        "pothole",
        "traffic",
        "garbage",
        "drainage",
        "water",
        "electricity",
        "public safety",
        "broken road",
        "street"
    ]

    # -------------------------------
    # CLASSIFICATION
    # -------------------------------

    if any(keyword in text_lower for keyword in cyber_keywords):

        category = "Cyber Crime"
        priority = "High"
        authority = "Cyber Crime Police"

    elif any(keyword in text_lower for keyword in women_safety_keywords):

        category = "Women Safety"
        priority = "High"
        authority = "Women Safety Police"

    elif any(keyword in text_lower for keyword in emergency_keywords):

        category = "Emergency Safety"
        priority = "High"
        authority = "Police Department"

    elif any(keyword in text_lower for keyword in student_keywords):

        category = "Student Grievance"
        priority = "Medium"
        authority = "Educational Institution"

    elif any(keyword in text_lower for keyword in legal_keywords):

        category = "Legal Assistance"
        priority = "Medium"
        authority = "Legal Services Authority"

    elif any(keyword in text_lower for keyword in public_safety_keywords):

        category = "Public Safety"
        priority = "Medium"
        authority = "Local Administration"

    else:

        category = "General"
        priority = "Medium"
        authority = "Local Administration"

    return {
        "category": category,
        "priority": priority,
        "authority": authority
    }