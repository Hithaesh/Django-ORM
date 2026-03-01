from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):

  def create(self):
    raise NotImplementedError("Create method for this is overriden with create_user(). Please use create_user method to create an user")
  
  def create_user(self, email, password, **extra_fields):

    if email is None and password is None:
      raise ValidationError("Email must not be none!!")
    
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
