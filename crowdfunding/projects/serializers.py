from rest_framework import serializers
from .models import Project, Pledge, Category


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    anonymous = serializers.BooleanField()
    supporter_id = serializers.IntegerField()
    project_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.anonymous = validated_data.get(
            'anonymous', instance.anonymous)
        instance.supporter = validated_data.get(
            'supporter', instance.supporter)
        instance.project = validated_data.get('project', instance.project)
        instance.save()
        return instance


class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    # owner = serializers.CharField(max_length=200)
    owner = serializers.ReadOnlyField(source='owner.id')
    categories = Category.Serializer(many=True)
    proj_cat = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        read_only=False,
        slug_field='name'
    )

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class Category(serializers.serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProjectDetailSerializer(ProjectSerializer):
    pledge = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get(
            'date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
