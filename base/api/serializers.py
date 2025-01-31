from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import Room,Topic,User,Message

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email','bio','avatar']
    def get_avatar(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url) 
        return None
    
    
class UserEmailSerializer(ModelSerializer):
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['name','email','bio','avatar']  
    def get_avatar(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url) 
        return None

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    user = UserEmailSerializer()  # Include user details in the message
    
    class Meta:
        model = Message
        fields = ['id', 'user', 'body', 'created', 'update']


class RoomSerializer(ModelSerializer):
    host = UserEmailSerializer()
    topic = TopicSerializer()
    messages = MessageSerializer(source='message_set', many=True)
    class Meta:
        model = Room
        fields = '__all__'
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email','username']
        
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        return user
        
             

class TopicWithCountSerializer(serializers.Serializer):
    topic = TopicSerializer()
    count = serializers.IntegerField()

