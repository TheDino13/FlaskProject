from django.shortcuts import render

def home_view(request):
    if request.user.is_authenticated:
        print(f"User  logged in: {request.user.username}")
    else:
        print("User not logged in")
    return render(request, 'home.html')
