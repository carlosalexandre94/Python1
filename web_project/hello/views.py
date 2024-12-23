from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, QuestionFlow, UserResponse
from django.contrib.auth.decorators import login_required
import uuid

def home(request):
    return render(request, 'quiz/home.html')

@login_required
def quiz(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    session_id = request.session.get('session_id', str(uuid.uuid4()))
    request.session['session_id'] = session_id

    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        answer = get_object_or_404(Answer, pk=answer_id)
        user_response = UserResponse.objects.filter(user=request.user, session_id=session_id).first()
        if user_response:
            question_ids = user_response.question_ids.split(',')
            question_ids.append(str(question_id))
            user_response.question_ids = ','.join(question_ids)
            user_response.save()
        else:
            UserResponse.objects.create(user=request.user, session_id=session_id, question_ids=str(question_id))
        
        next_question_flow = QuestionFlow.objects.filter(answer=answer).first()
        if next_question_flow:
            return redirect('quiz', question_id=next_question_flow.next_question.id)
        else:
            return render(request, 'quiz/end.html')
    return render(request, 'quiz/quiz.html', {'question': question})
