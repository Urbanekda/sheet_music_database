from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Sheet
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Homepage view, registered users only
@login_required(login_url='login')
def home(request):
    sheets = Sheet.objects.all()
    genre = request.GET.get('genre')
    difficulty = request.GET.get('difficulty')
    year = request.GET.get('year')

    if genre and genre != 'all':
        sheets = sheets.filter(genre=genre)
    if difficulty and difficulty != 'all':
        sheets = sheets.filter(difficulty_level=difficulty)
    if year and year != 'all':
        sheets = sheets.filter(publication_year=year)

    return render(request, "home.html", {
        "sheets": sheets,
        "genre_choices": Sheet.GENRE_CHOICES,
        "difficulty_choices": Sheet.DIFFICULTY_CHOICES,
        "years": Sheet.objects.values_list('publication_year', flat=True).distinct().order_by('publication_year'),
        "selected_genre": genre or 'all',
        "selected_difficulty": difficulty or 'all',
        "selected_year": year or 'all',
    })

# User registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='login')
def add_sheet(request):
    if request.method == "POST":
        try:
            #Extract form data
            new_sheet = Sheet(
                title=request.POST["title"],
                composer=request.POST["composer"],
                genre=request.POST.get("genre", ""),
                difficulty_level=request.POST.get("difficulty_level", ""),
                publication_year=request.POST.get("publication_year"),
                publisher=request.POST.get("publisher", ""),
                isbn=request.POST.get("isbn", ""),
                description=request.POST.get("description", ""),
                created_by=request.user,
                modified_by=request.user,
                sheet_file=request.FILES["sheet_file"],
                public=("public" in request.POST),
                preview_image=request.FILES["preview_image"]
            )
            
            #Handle optional fields
            if not new_sheet.arranger:
                new_sheet.arranger = None
            if not new_sheet.genre:
                new_sheet.genre = None
            if not new_sheet.difficulty_level:
                new_sheet.difficulty_level = None
            if not new_sheet.publication_year:
                new_sheet.publication_year = None
            if not new_sheet.publisher:
                new_sheet.publisher = None
            if not new_sheet.isbn:
                new_sheet.isbn = None
            if not new_sheet.description:
                new_sheet.description = None
            if not new_sheet.preview_image:
                new_sheet.preview_image = None
            
            #Save the book using in-built save method
            new_sheet.save()
            
            messages.success(request, f"Successfully added '{new_sheet.title}'")
            
            #Return back to home page
            return redirect('home')
        #Error handling    
        except Exception as e:
            messages.error(request, f"Error adding book: {str(e)}")
            return render(request, "add_sheet.html", {
                "genre_choices": Sheet.GENRE_CHOICES,
                "difficulty_choices": Sheet.DIFFICULTY_CHOICES,
            })
    
    # If GET request, just show the form
    return render(request, "add_sheet.html", {
                "genre_choices": Sheet.GENRE_CHOICES,
                "difficulty_choices": Sheet.DIFFICULTY_CHOICES,
            })

@login_required(login_url='login')
def delete_sheet(request, pk):
    sheet = get_object_or_404(Sheet, pk=pk)
    if request.method == "POST":
        sheet.delete()
        messages.success(request, f"Successfully deleted '{sheet.title}'")
        return redirect('home')
    return render(request, "confirm_delete.html", {"sheet": sheet})

@login_required(login_url='login')
def edit_sheet(request, pk):
    sheet = get_object_or_404(Sheet, pk=pk)
    if request.method == "POST":
        try:
            sheet.title = request.POST["title"]
            sheet.composer = request.POST["composer"]
            sheet.genre = request.POST.get("genre") or None
            sheet.difficulty_level = request.POST.get("difficulty_level") or None
            pub_year = request.POST.get("publication_year")
            sheet.publication_year = int(pub_year) if pub_year else None
            sheet.publisher = request.POST.get("publisher") or None
            sheet.isbn = request.POST.get("isbn") or None
            sheet.description = request.POST.get("description") or None
            sheet.modified_by = request.user
            sheet.public = "public" in request.POST

            if "sheet_file" in request.FILES and request.FILES["sheet_file"]:
                sheet.sheet_file = request.FILES["sheet_file"]

            if "preview_image" in request.FILES and request.FILES["preview_image"]:
                sheet.preview_image = request.FILES["preview_image"]

            sheet.save()
            messages.success(request, f"Successfully updated '{sheet.title}'")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error updating book: {str(e)}")
            return render(request, "edit_sheet.html", {
                "sheet": sheet,
                "genre_choices": Sheet.GENRE_CHOICES,
                "difficulty_choices": Sheet.DIFFICULTY_CHOICES,
            })

    return render(request, "edit_sheet.html", {
        "sheet": sheet,
        "genre_choices": Sheet.GENRE_CHOICES,
        "difficulty_choices": Sheet.DIFFICULTY_CHOICES,
    })

@login_required(login_url='login')
def sheet_profile(request, pk):
    sheet = get_object_or_404(Sheet, pk=pk)
    return render(request, "sheet_profile.html", {"sheet": sheet})
