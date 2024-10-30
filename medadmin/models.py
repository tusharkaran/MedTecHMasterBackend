from django.db import models
from django.contrib.auth.hashers import make_password

class Admin(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hash the password before saving if it's a new admin
        if not self.id:
            self.password = make_password(self.password)
        super(Admin, self).save(*args, **kwargs)

    @classmethod
    def create_admin(cls, user_name, password):
        hashed_password = make_password(password)
        admin = cls(
            user_name=user_name,
            password=hashed_password
        )
        admin.save()
        return admin

    @classmethod
    def get_admin_by_username(cls, username):
        try:
            return cls.objects.get(user_name=username)
        except cls.DoesNotExist:
            return None
