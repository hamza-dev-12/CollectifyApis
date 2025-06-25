from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    base_amount = models.IntegerField(default=1000)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")

    def __str__(self):
        return f"{self.group_name}"


class Member(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group")
    member_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        unique_together = ("group", "member_name")


class Payment(models.Model):
    status = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.IntegerField()
    group_members = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="group_members"
    )
