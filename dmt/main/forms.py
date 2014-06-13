from django.forms import ModelForm
from django import forms
from .models import StatusUpdate, Node, User, Project, Milestone, Item


class StatusUpdateForm(ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['body']


class NodeUpdateForm(ModelForm):
    class Meta:
        model = Node
        fields = ['subject', 'body']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["fullname", "email", "type", "title", "phone",
                  "bio", "photo_url", "photo_width", "photo_height",
                  "campus", "building", "room"]


class ProjectUpdateForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['pid', ]


class MilestoneUpdateForm(ModelForm):
    class Meta:
        model = Milestone
        exclude = ['mid', 'project', 'status']


class ItemUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemUpdateForm, self).__init__(*args, **kwargs)
        passed_item = kwargs.get('instance')
        milestone = Milestone.objects.get(item=passed_item)
        project = Project.objects.get(milestone=milestone)
        project_milestones = project.milestone_set.all()
        self.fields['milestone'].queryset = project_milestones

    class Meta:
        model = Item
        exclude = ['iid', 'owner',
                   'assigned_to', 'status', 'r_status', 'last_mod',
                   'tags', 'priority']

