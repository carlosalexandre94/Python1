from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, QuestionFlow, UserResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'quiz/home.html')

@login_required
def quiz(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        answer = get_object_or_404(Answer, pk=answer_id)
        UserResponse.objects.create(user=request.user, question=question, answer=answer)
        next_question_flow = QuestionFlow.objects.filter(answer=answer).first()
        if next_question_flow:
            return redirect('quiz', question_id=next_question_flow.next_question.id)
        else:
            return render(request, 'quiz/end.html')
    return render(request, 'quiz/quiz.html', {'question': question})
