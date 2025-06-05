from rest_framework import viewsets, status, serializers, filters
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter, ConversationFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

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
        """Return messages for a specific conversation."""
        return Message.objects.filter(
            conversation__conversation_id=self.kwargs['conversation_pk'],
            conversation__participants=self.request.user
        ).order_by('-sent_at')

    def perform_create(self, serializer):
        """Create a new message in the conversation."""
        try:
            # Get conversation by UUID
            conversation = Conversation.objects.get(
                conversation_id=self.kwargs['conversation_pk']
            )
            
            # Check if user is participant
            if not conversation.participants.filter(id=self.request.user.id).exists():
                raise ValidationError({'error': 'You are not a participant in this conversation'})
            
            # Create message
            serializer.save(
                sender=self.request.user,
                conversation=conversation
            )
        except Conversation.DoesNotExist:
            raise ValidationError({'error': 'Conversation not found'})
