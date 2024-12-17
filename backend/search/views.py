from django.http import JsonResponse

def search_professor(request):
    data = {
        "name": "John Doe",
        "rmpGrade": "4.5",
        "rmpLink": "http://ratemyprofessors.com/johndoe",
        "gradeDistribution": [
            {"grade": "A", "count": 50},
            {"grade": "B", "count": 30},
            {"grade": "C", "count": 10},
        ],
    }
    return JsonResponse(data)
