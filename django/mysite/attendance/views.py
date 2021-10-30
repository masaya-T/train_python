from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from .models import Person,Manager,Worker
# Create your views here.

class WorkerListView(generic.ListView):
    #  template_name を使って ListView に既存の "polls/index.html" テンプレートを使用するように伝えます。
    template_name = 'attendance/list.html'
    # context_object_name 属性を与え、 workers を代わりに使用すると指定します。
    context_object_name = 'workers'
    
    # get_querysetメソッドは主にListViewで使われますが、モデルインスタンスの一覧を返すメソッドです。
    def get_queryset(self):
        workers = Worker.objects.all()  # データベースからオブジェクトを取得して
        for i in workers:
            print(i.person,i.joined_at)
        return workers

    
class PersonView(generic.DetailView):
    model = Person
    template_name = 'attendance/person.html'



