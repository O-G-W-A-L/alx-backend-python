from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return conversations where the authenticated user is a participant."""
        return Conversation.objects.filter(participants=self.request.user).distinct()

    @action(detail=False, methods=['post'])
    def start_conversation(self, request):
        """Start a new conversation with a single participant."""
        participant_id = request.data.get('participant_id')
        if not participant_id:
            return Response({'error': 'Participant ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(participant_id) == str(request.user.pk):
            return Response({'error': 'Cannot start a conversation with yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = User.objects.get(pk=participant_id)
        except User.DoesNotExist:
            return Response({'error': 'Participant not found.'}, status=status.HTTP_404_NOT_FOUND)

        conversations = Conversation.objects.filter(participants=request.user).filter(participants=participant).distinct()
        if conversations.exists():
            serializer = self.get_serializer(conversations.first())
            return Response(serializer.data, status=status.HTTP_200_OK)

        conversation = Conversation.objects.create()
        conversation.participants.set([request.user, participant])
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return messages from conversations the user is part of."""
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """Send a message in an existing conversation, ensuring the user is a participant."""
        conversation_id = self.request.data.get('conversation_id')
        if not conversation_id:
            raise serializers.ValidationError("Conversation ID is required.")

        try:
            conversation = Conversation.objects.get(pk=conversation_id, participants=self.request.user)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Invalid conversation or access denied.")

        serializer.save(sender=self.request.user, conversation=conversation)