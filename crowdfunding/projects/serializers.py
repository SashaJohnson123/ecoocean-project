from rest_framework import serializers
from .models import Project, Pledge, Category


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    anonymous = serializers.BooleanField()
    supporter_id = serializers.ReadOnlyField(source='supporter.username')
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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


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
    categories = CategorySerializer(many=True)

    def create(self, validated_data):
        # grab categories from your data, so it's not passed into your Project constructor
        categories = validated_data.pop('categories')
        # create your project (with no categories initially)
        project = Project.objects.create(**validated_data)
        # for each of the categories you've passed in
        for cat in categories:
            # create a new category, or use an existing one if it already exists
            # pass in the project so it creates a relationship between category <--> project
            category, created = Category.objects.get_or_create(**cat)
            category.projects.add(project)
            category.save()
        return project


class ProjectDetailSerializer(ProjectSerializer):
    pledge = PledgeSerializer(many=True, read_only=True, source='pledges')

    can_edit = serializers.SerializerMethodField()

    def get_can_edit(self, project):
        user = self.context['request'].user
        print(user)
        return user.is_superuser or user is project.owner

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
