from django.utils import timezone
import json
from django.shortcuts import render
from .models import todos
from django.contrib.auth.decorators import login_required
from .forms import TodoUpdateForm
from django.http import HttpResponse



def home(request):
    return render(request, 'todos/home.html', {'title': 'Todo-Home'})

def about(request):
    return render(request, 'todos/about.html', {'title': 'Todo-About'})

@login_required
def personalTodos(request):

    data = {
        'todos': todos.objects.filter(userID_id=request.user.id).order_by('-id'),
        'title': 'My Todo',
        'myText': request.POST.get('myText','default text'),
    }
    return render(request, 'todos/personalTodos.html', data)

@login_required
def updateTodos(request):
    # get all values of current todos in database and put to a list
    listCurrentData = todos.objects.filter(userID_id=request.user.id).order_by('-id').values()
    #values() to return list of dicts instead of queryset

    # get list of new data in UI
    lNewData = request.POST.getlist('allTodos[]','')
    listNewData = [json.loads(item) for item in lNewData]

    # compare 2 lists and delete/addNew records to database accordingly
    for currentData in listCurrentData: #iterator() to avoid caching queryset data in memory
        for newData in listNewData:
            if currentData['content'] == newData['content']:
                break
        #remove listCurrentData[i] from db
        else:
            todos.objects.filter(id=currentData['id']).delete()

    for newData in listNewData:
        for currentData in listCurrentData:
            if newData['content'] == currentData['content']:
                if currentData['isCompleted'] != newData['isCompleted']:
                    currentRec = todos.objects.get(id=currentData['id'])
                    # note get() method return object, filter() method return queryset
                    currentRec.isCompleted = not currentRec.isCompleted
                    currentRec.save()
                break
        else:
            # add listNewData[i] to db
            temp = todos(content=newData['content'], createdDate=timezone.now(), isCompleted=False, userID_id=request.user.id)
            temp.save()

    test = todos.objects.filter(userID_id=request.user.id).values()
    form = TodoUpdateForm()
    data = {
        'todos': todos.objects.filter(userID_id=request.user.id),
        'title': 'My Todo',
    }

    return render(request, 'todos/personalTodos.html', data)
    # return HttpResponse(200)

