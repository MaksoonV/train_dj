from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import TaskForm
from .models import Task


def index(request):
    # GET — открыть страницу. POST — отправить заполненную форму.
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  # Django сам выполняет INSERT в SQLite.
            # После сохранения открываем страницу заново через GET.
            # Поэтому обновление страницы не добавляет задачу повторно.
            return redirect("tasks:index")
    else:
        form = TaskForm()

    tasks = Task.objects.order_by("-id")  # Новые задачи сверху.
    return render(request, "tasks/index.html", {"tasks": tasks, "form": form})


@require_POST  # Изменять данные можно только отправкой формы.
def toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=["done"])
    return redirect("tasks:index")


@require_POST
def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("tasks:index")
