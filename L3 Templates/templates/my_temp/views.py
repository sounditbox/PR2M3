from django.http import HttpResponseNotFound
from django.shortcuts import render

users = {
    1: {
        'id': 1,
        'username': 'Alex',
        'age': 30,
        'occupation': 'Software Engineer',
        'experience': 0.5,
        'rating': 4.4,
        'image': 'avatar-1.webp',
        'hobbies': ['coding', 'reading', 'hiking', 'swimming'],
        'address': {'street': '123 Main St', 'city': 'Anytown', 'state': 'CA',
                    'zip': '12345'},
    },
    2: {
        'id': 2,
        'username': 'Jane',
        'age': 25,
        'occupation': 'Data Scientist',
        'experience': 1.5,
        'rating': 9.4,
        'image': 'avatar-2.jpg',
        'hobbies': ['coding', 'reading', 'hiking', 'swimming'],
        'address': {'street': '456 Main St', 'city': 'Anytown', 'state': 'CA',
                    'zip': '12345'},
    },
    3: {
        'id': 3,
        'username': 'John',
        'age': 28,
        'occupation': 'Product Manager',
        'experience': 2.5,
        'rating': 2.5,
        'image': 'avatar-3.jpg',
        'hobbies': ['coding', 'reading', 'hiking', 'swimming'],
        'address': {'street': '789 Main St', 'city': 'Anytown', 'state': 'CA',
                    'zip': '12345'},
    },
    4: {
        'id': 4,
        'username': 'Bob',
        'age': 32,
        'occupation': 'QA Engineer',
        'experience': 3.5,
        'rating': 8.4,
        'image': 'avatar-4.jpg',
        'hobbies': [],
        'address': {'street': '101 Main St', 'city': 'Anytown', 'state': 'CA',
                    'zip': '12345'},
    }
}


def index(request):
    context = {
        "title": "Home",
    }
    return render(request, "index.html", context)


def show_user_profile(request, user_id):
    if user_id not in users:
        return HttpResponseNotFound('User not found')

    context = {
        'user_data': users[user_id],
        'title': 'User Profile',
    }
    return render(request, 'user_profile.html', context)


def profiles(request):
    context = {
        'profiles': users,
        'title': 'Profiles',
    }
    return render(request, 'profiles.html', context)
