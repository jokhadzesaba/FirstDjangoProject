from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import Room,Topic,User,Message

class UserSerializer(ModelSerializer):
    id = User.id
    class Meta:
        model = User
        fields = ['name','email','bio','avatar','id']
    def get_avatar(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url) 
        return None
    

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    user = UserSerializer()  # Include user details in the message
    
    class Meta:
        model = Message
        fields = ['id', 'user', 'body', 'created', 'update']


class RoomSerializer(ModelSerializer):
    host = UserSerializer()
    topic = TopicSerializer()
    messages = MessageSerializer(source='message_set', many=True)
    class Meta:
        model = Room
        fields = '__all__'
class RoomSerializer2(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','name']
        
class ActivitySerializer(ModelSerializer):
    user = UserSerializer()
    room = RoomSerializer2()
    
    class Meta:
        model = Message
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

