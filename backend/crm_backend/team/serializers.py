from django.contrib.auth.models import User
from rest_framework import serializers
from userprofile.serializer import UserProfileSerializer
from .models import Team

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "is_superuser",
            "is_staff",
            "userprofile"
        )


    def update(self, instance, validated_data):
        full_name = None


        if instance.first_name and instance.last_name:
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            full_name = instance.first_name + " " + instance.last_name

        if instance.email:
            instance.email = validated_data.get('email',instance.email)

        instance.save()

        request_data = self.context['request'].data

        phone = None
        profile_picture = None



        #Front-end send JSON
        if 'userprofile' in request_data and isinstance(request_data['userprofile'],dict):
            phone = request_data['userprofile'].get('phone')
            profile_picture = request_data['userprofile'].get('profile_picture')
        #Front-end send FormData
        else:
            phone = request_data.get('userprofile.phone')
            profile_picture = request_data.get('userprofile.profile_picture')

        if phone is not None or profile_picture is not None or full_name is not None:
            profile = getattr(instance,'userprofile',None)

            if profile is not None:
                if phone is not None:
                    profile.phone = phone

                if profile_picture is not None:
                    if profile_picture not in ['', 'null', 'undefined'] and not isinstance(profile_picture, dict):
                        profile.profile_picture = profile_picture
                if full_name is not None:
                    profile.full_name = full_name


                profile.save()

        return instance







class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True,read_only=True) # MANY - MANY REALATIONSHIP , vream doar sa citim datele
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "members",
            "created_at",
            "created_by",
            "invite_code"
        )
