from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
            
        # For Message objects, check the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
            
        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated