from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView
from django.contrib.auth.decorators import login_required
from .models import Movie,Booking,Wallet,review
from django.contrib import messages
from .forms import BalanceUpdateForm
#from django.core.mail import send_mail
from .models import review

def home(request):
    context = {
        'posts': Movie.objects.all()
    }
    return render(request, 'movies/home.html', context)


class PostListView(ListView):
    model = Movie
    template_name = 'movies/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'movies'
    ordering = ['-launch_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        reviews = review.objects.filter(movie=movie).order_by('-date_posted')
        context['reviews'] = reviews
        return context
class PostCreateView(LoginRequiredMixin, CreateView):
    model = review
    fields = ['title', 'content', 'movie']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
def about(request):
    return render(request, 'movies/about.html', {'title': 'About'})




### booking


@login_required
def bookmovie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
#    wallet = get_object_or_404(Wallet, user=request.user)
    if not Booking.objects.filter(user=request.user, movie=movie).exists():
        Booking.objects.create(user=request.user, movie=movie)
#        Wallet.deduct_funds(request.user,movie.price)
#        send_mail(
#            "Congratulations",
#            "Your movie has been booked",
#            "Here is the ticket for the movie",
#            {User.email},
#            fail_silently=False,
#        )
        return render(request, 'movies/booking_success.html')
    else:
        return render(request,'movies/already_booked.html')
def booking_success(request):
    return render(request, 'movies/booking_success.html') 
def already_booked(request):
    return render(request, 'movies/already_booked.html') 

def bookinglist(request):
    Bookings = Booking.objects.filter(user=request.user)
    return render(request, 'movies/bookings.html', {'Bookings': Bookings})




@login_required
def updatebalance(request):
    if request.method == 'POST':
        b_form = BalanceUpdateForm(request.POST, instance=request.user)
        if b_form.is_valid():
            b_form.save()
            messages.success(request, f'Your balance has been updated!')
            return redirect('profile')

    else:
        b_form = BalanceUpdateForm(instance=request.user)

    context = {
        'b_form': b_form
    }

    return render(request, 'movies/balance.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = review
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)