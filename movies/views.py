from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Reply, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def create_reply(request, id, review_id, parent_reply_id=None):
    if request.method == 'POST' and request.POST['comment'] != '':
        review = get_object_or_404(Review, id=review_id)
        reply = Reply()
        reply.comment = request.POST['comment']
        reply.review = review
        reply.user = request.user
        
        # Handle nested replies
        if parent_reply_id:
            parent_reply = get_object_or_404(Reply, id=parent_reply_id, review=review)
            reply.parent_reply = parent_reply
        
        reply.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

def petitions(request):
    petitions_list = Petition.objects.all().order_by('-created_at')
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petitions'] = petitions_list
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        movie_title = request.POST.get('movie_title', '').strip()
        
        if title and description and movie_title:
            petition = Petition.objects.create(
                title=title,
                description=description,
                movie_title=movie_title,
                created_by=request.user
            )
            messages.success(request, 'Petition created successfully!')
            return redirect('movies.petitions')
        else:
            messages.error(request, 'All fields are required.')
    
    template_data = {}
    template_data['title'] = 'Create Petition'
    return render(request, 'movies/create_petition.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    
    # Check if user already voted
    existing_vote = PetitionVote.objects.filter(petition=petition, user=request.user).first()
    
    if existing_vote:
        messages.warning(request, 'You have already voted for this petition.')
    else:
        PetitionVote.objects.create(petition=petition, user=request.user)
        messages.success(request, f'You voted for "{petition.movie_title}"!')
    
    return redirect('movies.petitions')