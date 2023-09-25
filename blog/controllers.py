from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Question, Answer, Category, Notification, Image


def create_image_if_exists(request):
    print(request.FILES)
    image = request.FILES.get('photo')
    if image:
        image = Image.objects.create(title=image.name, image=image)
        return image

def get_all_questions():
    return Question.objects.all().order_by('-up_votes')


def get_all_answers():
    return Answer.objects.all()


def get_all_questions_with_answers_for_category(category_id):
    return get_all_questions().filter(category=int(category_id)).prefetch_related('answer_set')


def get_question_by_id(question_id):
    return get_object_or_404(Question, pk=question_id)


def get_answers_for_question(question_id):
    return Answer.objects.all().filter(question=question_id)


def get_all_questions_with_answers():
    return get_all_questions().prefetch_related('answer_set')


def get_all_categories():
    return Category.objects.all()


def create_question_with_success_message(form, request, image=None):
    question = form.save(commit=False)
    question.author = request.user
    question.image = image

    words_to_replace = ['word1', 'word2', 'word3', "Лох"]
    replacement_char = '*'

    for word in words_to_replace:
        question.title = question.title.replace(word, replacement_char * len(word))
        question.text = question.text.replace(word, replacement_char * len(word))

    question.publish()
    messages.success(request, message='Запитання додано!')


def create_answer_with_success_message(form, request, image=None):
    if not request.user.is_authenticated:
        return redirect('/login.html')

    answer = form.save(commit=False)
    answer.author = request.user
    answer.image = image

    words_to_replace = ['word1', 'word2', 'word3', "Лох"]
    replacement_char = '*'

    for word in words_to_replace:
        answer.text = answer.text.replace(word, replacement_char * len(word))

    answer.author = request.user
    question_pk = request.POST.get('pk')
    question = Question.objects.get(pk=question_pk)
    answer.question = question

    answer.publish()
    messages.success(request, message='Відповідь додана!')


def edit_record(request, model_class, form_class, record_id, image=None):
    record = get_object_or_404(model_class, pk=record_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=record)

        if form.is_valid():
            image = create_image_if_exists(request)
            record.image = image

            record.save()
            form.save()
            return redirect('/')
    else:
        form = form_class(instance=record)

    return render(request, 'edit_record.html', {'form': form, 'model': record.__class__.__name__})


def delete_record(request, model_class, record_id):
    record = get_object_or_404(model_class, pk=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('/my_questions')
    else:
        return render(request, 'delete_record.html', {'record': record, 'model': record.__class__.__name__})


def get_all_questions_for_user(user):
    return Question.objects.all().filter(author=user)


def get_all_answers_for_user(user):
    return Answer.objects.all().filter(author=user)


def get_all_notifications_for_user(user):
    return Notification.objects.all().filter(Q(to_user=user) and ~Q(from_user=user))


def get_questions_by_search_query(query):
    return Question.objects.filter(Q(title__icontains=query) or Q(text__icontains=query))


def get_user_by_id(user_id):
    return User.objects.get(pk=user_id)


def create_notification(request, record, action):
    n = Notification()

    n.from_user = get_user_by_id(request.user.id)
    n.to_user = record.author
    n.post_id = record.id
    n.post_type = type(record).__name__
    n.action = action

    n.save()
