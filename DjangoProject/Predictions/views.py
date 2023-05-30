import os
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt
from prediction.Main.run import MainRunner

from .forms import FileUploadForm
from .models import File
from django.conf import settings


def upload_file(request):
    data = File.objects.all()
    if data:
        os.remove(settings.PATH_FOR_CLEAN_FILE + data[0].file.url)
        os.remove('out/report.png')
        data.delete()

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('results')
    else:
        form = FileUploadForm(initial={'title': ''})
    return render(request, 'upload.html', {'form': form})

def results(path):
    history, test_loss = MainRunner(path).run()
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(loss))
    plt.figure()
    plt.plot(epochs, loss, 'b', label='training loss')
    plt.plot(epochs, val_loss, 'r', label='validation loss')
    plt.title('learning history')
    plt.xlabel('epochs')
    plt.ylabel('loss')
    plt.legend()
    plt.savefig('out/report.png')

def show_reult(request):
    results(settings.PATH_IN)
    data = File.objects.all()
    context = {
        'data': data
    }
    return render(request, 'home_page.html', context)
