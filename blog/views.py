# Create your views here.
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from blog.forms import UserForm, SubmitForm, HighlightForm, TagForm
from blog.models import Share, Highlight, Link, Follow, Like, Image
import re
import heapq


def home(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    users = User.objects.all()
    stories = Share.objects.all()
    for u in users:
        if (Follow.objects.filter(user1 = request.user, user2 = u).count() != 1 and u != request.user):
            follow = Follow.objects.create(user1 = request.user, user2 = u, following = False)
            follow.save()
    for s in stories:
        if (Like.objects.filter(user = request.user, story = s).count() != 1):
            like = Like.objects.create(user = request.user, story = s, liking = False)
            like.save()
    return redirect("dashboard")


def faq(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("help.html", {"user": request.user})


def contact(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("contact.html", {"user": request.user})


def exchange(request):

    array = []
    array_large = []
    total = 0
    total_large = 0
    darray = []
    allarray = []

    story = Share.objects.filter(publish = True).order_by("?")[:1]
    tags = Link.objects.all()
    like = Like.objects.filter(user = request.user)

    for s in story:

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()
        trimmest = cooler.splitlines()

        darray = []
        sums = 0
        count = 0

        for x in trimmest:
            count = count + 1
            v = x.split()
            sums = sums + len(v)
            darray.append([sums, count, len(v), s.id])

        allarray.append(darray)

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        store = 0
        for w, p, c, q in darray:
            if (c != 0):
                chill = 0
                for word in trimmer:
                    flag = False
                    chill = chill + 1
                    if (chill > store and chill <= w):
                        for l in link:
                            if word == l.links:
                                heapq.heappush(array_large, (l, total, s.id, p))
                                flag = True
                        if (flag == False):
                            heapq.heappush(array_large, (word, total, s.id, p))
                    total = total + 1
                store = w

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("exchange.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags, "like": like, "template": allarray})


def tag(request, id, word):
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            story = Share.objects.get(id = id)
            links = Link.objects.get(story = story, id = word) 
            key = Image.objects.create(story = story, user = request.user, paths = image)
            key.save()
            links.path.add(key)
            links.save()
            return HttpResponseRedirect('/')
    else:
        form = TagForm()
    return render_to_response("dashboard.html", {"form": form})
    

# Changes made
def dashboard(request):

    array = []
    array_large = []
    total = 0
    total_large = 0
    darray = []
    allarray = []

    story = Share.objects.filter(publish = True).order_by("-id")
    tags = Link.objects.all()
    like = Like.objects.filter(user = request.user)

    for s in story:

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()
        trimmest = cooler.splitlines()

        darray = []
        sums = 0
        count = 0

        for x in trimmest:
            count = count + 1
            v = x.split()
            sums = sums + len(v)
            darray.append([sums, count, len(v), s.id])

        allarray.append(darray)

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        store = 0
        for w, p, c, q in darray:
            if (c != 0):
                chill = 0
                for word in trimmer:
                    flag = False
                    chill = chill + 1
                    if (chill > store and chill <= w):
                        for l in link:
                            if word == l.links:
                                heapq.heappush(array_large, (l, total, s.id, p))
                                flag = True
                        if (flag == False):
                            heapq.heappush(array_large, (word, total, s.id, p))
                    total = total + 1
                store = w

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("dashboard.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags, "like": like, "template": allarray})


def view(request):
    array = []
    array_large = []
    total = 0
    total_large = 0
    nostory = False
    footer = False
    darray = []
    allarray = []

    story = Share.objects.filter(user = request.user).order_by("-id")

    if (story.count() == 0):
        nostory = True

    if (story.count() >= 3):
        footer = True
    
    tags = Link.objects.all()

    for s in story:

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()
        trimmest = cooler.splitlines()

        darray = []
        sums = 0
        count = 0

        for x in trimmest:
            count = count + 1
            v = x.split()
            sums = sums + len(v)
            darray.append([sums, count, len(v), s.id])

        allarray.append(darray)

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        store = 0
        for w, p, c, q in darray:
            if (c != 0):
                chill = 0
                for word in trimmer:
                    flag = False
                    chill = chill + 1
                    if (chill > store and chill <= w):
                        for l in link:
                            if word == l.links:
                                heapq.heappush(array_large, (l, total, s.id, p))
                                flag = True
                        if (flag == False):
                            heapq.heappush(array_large, (word, total, s.id, p))
                    total = total + 1
                store = w

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("view.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags, "flag": nostory, "footer": footer, "template": allarray})


def create(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("create.html", {"user": request.user})
    

def delete(request, id):

    story = Share.objects.get(id=id)
    story.delete()
    return HttpResponseRedirect("/view/")


def follow(request, username):

    follow = Follow.objects.get(user1 = request.user, user2__username = username, following = False)
    follow.following = True
    follow.save()
    return HttpResponseRedirect("/profile/" + username + "/")


def unfollow(request, username):

    follow = Follow.objects.get(user1 = request.user, user2__username = username, following = True)
    follow.following = False
    follow.save()
    return HttpResponseRedirect("/profile/" + username + "/")


def like(request, id):

    story = Share.objects.get(id=id)
    like = Like.objects.get(user = request.user, story = story, liking = False)
    like.liking = True
    like.save()
    return HttpResponseRedirect("/")


def unlike(request, id):

    story = Share.objects.get(id=id)
    like = Like.objects.get(user = request.user, story = story, liking = True)
    like.liking = False
    like.save()
    return HttpResponseRedirect("/")


def profile(request, username):

    array = []
    array_large = []
    total = 0
    total_large = 0
    num = 0
    following = 0
    followers = 0
    nostory = False
    footer = False
    darray = []
    allarray = []

    follow = Follow.objects.filter(user1 = request.user, user2__username = username)

    if (follow.count() == 0 and username != request.user.username):
        return render_to_response("error.html")

    followyou = Follow.objects.filter(user1__username = username, following = True)
    followme = Follow.objects.filter(user2__username = username, following = True)

    for y in followyou:

        following = following + 1

    for m in followme:

        followers = followers + 1

    story = Share.objects.filter(user__username=username, publish = True).order_by("-id")
    tags = Link.objects.all()
    like = Like.objects.filter(user = request.user)

    if (story.count() == 0):
        nostory = True

    if (story.count() >= 2):
        footer = True

    for s in story:

        num = num + 1

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()
        trimmest = cooler.splitlines()

        darray = []
        sums = 0
        count = 0

        for x in trimmest:
            count = count + 1
            v = x.split()
            sums = sums + len(v)
            darray.append([sums, count, len(v), s.id])

        allarray.append(darray)

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        store = 0
        for w, p, c, q in darray:
            if (c != 0):
                chill = 0
                for word in trimmer:
                    flag = False
                    chill = chill + 1
                    if (chill > store and chill <= w):
                        for l in link:
                            if word == l.links:
                                heapq.heappush(array_large, (l, total, s.id, p))
                                flag = True
                        if (flag == False):
                            heapq.heappush(array_large, (word, total, s.id, p))
                    total = total + 1
                store = w

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("profile.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags, "posts": num, "username": username, "follow": follow, "following": following, "followers": followers, "flag": nostory, "footer": footer, "like": like, "template": allarray})







def highlight(request):
    if request.method == 'POST':
        form = HighlightForm(request.POST)
        if form.is_valid():
            high = form.cleaned_data['highlight']
            story = Share.objects.filter(user = request.user, publish = False).order_by('-pk')[0]
            story.publish = True
            light = Highlight.objects.create(user = request.user, highlights = high, story = story)
            light.save()
            story.save()

            cool = str(light.highlights)
            cooler = str(story.paragraph)
            coolest = str(story.title)
            trim = cool.split()
            trimmer = cooler.split()
            trimmest = coolest.split()

            for word in trimmer:
                for w in trim:
                    if (word == w):
                        if (Link.objects.filter(links = word, story = story).count() == 0):
                            link = Link.objects.create(links = word, story = story)

            for words in trimmest:
                for w in trim:
                    if (words == w):
                        if (Link.objects.filter(links = words, story = story).count() == 0):
                            link = Link.objects.create(links = words, story = story)

            return HttpResponseRedirect('/')
    else:
        form = HighlightForm()
    return render_to_response("error.html", {"form": form})


def highlightw(request, id):
    if request.method == 'POST':
        form = HighlightForm(request.POST)
        if form.is_valid():
            high = form.cleaned_data['highlight']
            story = Share.objects.filter(user = request.user, publish = False).order_by('-pk')[0]
            story.publish = True
            light = Highlight.objects.create(user = request.user, highlights = high, story = story)
            light.save()
            story.save()

            cool = str(light.highlights)
            cooler = str(story.paragraph)
            coolest = str(story.title)
            trim = cool.split()
            trimmer = cooler.split()
            trimmest = coolest.split()

            for word in trimmer:
                for w in trim:
                    if (word == w):
                        if (Link.objects.filter(links = word, story = story).count() == 0):
                            link = Link.objects.create(links = word, story = story, path = None)

            for words in trimmest:
                for w in trim:
                    if (words == w):
                        if (Link.objects.filter(links = words, story = story).count() == 0):
                            link = Link.objects.create(links = words, story = story, path = None)

            return HttpResponseRedirect('/')
    else:
        form = HighlightForm()
    return render_to_response("error.html", {"form": form})


def next(request):
    heap = []
    total = 0
    heap_large = []
    total_large = 0
    array = []

    if (Share.objects.filter(user = request.user, publish = False).count() > 0):
        story = Share.objects.filter(user = request.user, publish = False).order_by('-pk')[0]
        cool = str(story.title)
        cooler = str(story.paragraph)
        trim = cool.split()
        trimmer = cooler.split()
        trimmest = cooler.splitlines()

        array = []
        sums = 0
        count = 0

        for x in trimmest:
            count = count + 1
            v = x.split()
            sums = sums + len(v)
            array.append([sums, count, len(v)])

        for w in trim:
            total = total + 1
            heapq.heappush(heap, (w, total))

        store = 0
        for l, p, c in array:
            if (c != 0):
                total_large = 0
                for word in trimmer:
                    total_large = total_large + 1
                    if (total_large > store and total_large <= l):
                        heapq.heappush(heap_large, (word, total_large, p))
                store = l
    
        sortme = sorted(heap, key=lambda x: x[1])
        sortme_large = sorted(heap_large, key=lambda x: x[1])

        print sortme_large

        if not request.user.is_authenticated():
            return render_to_response("register.html")
    else:
        sortme = None
        sortme_large = None
    return render_to_response("step2.html", {"user": request.user, "title": sortme, "paragraph": sortme_large, "template": array})


def nextw(request, id):
    heap = []
    total = 0
    heap_large = []
    total_large = 0
    array = []

    if (Share.objects.filter(id = id, publish = False).count() > 0):
        story = Share.objects.get(id = id)
        cool = str(story.title)
        cooler = str(story.paragraph)
        trim = cool.split()
        trimmer = cooler.split()
        trimmest = cooler.splitlines()

        array = []
        sums = 0
        count = 0

        for x in trimmest:
            count = count + 1
            v = x.split()
            sums = sums + len(v)
            array.append([sums, count, len(v)])

        for w in trim:
            total = total + 1
            heapq.heappush(heap, (w, total))

        store = 0
        for l, p, c in array:
            if (c != 0):
                total_large = 0
                for word in trimmer:
                    total_large = total_large + 1
                    if (total_large > store and total_large <= l):
                        heapq.heappush(heap_large, (word, total_large, p))
                store = l
    
        sortme = sorted(heap, key=lambda x: x[1])
        sortme_large = sorted(heap_large, key=lambda x: x[1])

        if not request.user.is_authenticated():
            return render_to_response("register.html")
    else:
        sortme = None
        sortme_large = None
    return render_to_response("step2_re.html", {"user": request.user, "title": sortme, "paragraph": sortme_large, "id": id, "template": array})


def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            tit = form.cleaned_data['title']
            para = form.cleaned_data['paragraph']
            story = Share.objects.create(user = request.user, title = tit, paragraph = para, publish = False)
            story.save()
            return HttpResponseRedirect('/next/')
    else:
        form = SubmitForm()
    return render_to_response("error.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            newuser = User.objects.create_user(name, form.cleaned_data['email'], pw)
            newuser.save()
            users = User.objects.all()
            stories = Share.objects.all()
            user = authenticate(username = name, password = pw)
            auth_login(request, user)
            for u in users:
                if (u != request.user):
                    follow = Follow.objects.create(user1 = request.user, user2 = u, following = False)
                    follow.save()
            for s in stories:
                like = Like.objects.create(user = request.user, story = s, liking = False)
                like.save()
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render_to_response("register.html", {"form": form})


def login(request):
    username = password = ''
    error = False
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
  
        user = authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = True
    return render_to_response("login.html", {"error": error})
  

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
