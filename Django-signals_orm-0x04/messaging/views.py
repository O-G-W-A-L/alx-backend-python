from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Message

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home') 
    
    return render(request, 'confirm_delete.html', {
        'user': request.user
    })

def conversation_view(request, conversation_user_id):
    user = request.user
    # Fetch root messages for the conversation with the specified user
    root_messages = Message.objects.filter(
        parent_message__isnull=True,
        sender=user,
        receiver__id=conversation_user_id
    ).select_related('sender', 'receiver').prefetch_related('replies')

    def get_threaded_replies(message):
        """Recursively retrieve replies for a given message."""
        return [{
            'message': reply,
            'replies': get_threaded_replies(reply)
        } for reply in message.replies.all()]

    # Prepare threaded data for rendering
    threaded_data = [{
        'message': msg,
        'replies': get_threaded_replies(msg)
    } for msg in root_messages]

    return render(request, 'messaging/conversation.html', {'threaded_data': threaded_data})