from django.db import models
import bcrypt
import re
# Create your models here.

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        usersWithEmail = User.objects.filter(email = postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['fname']) <2:
            errors['fnamerequired'] = "First Name must be at least 2 Characters!"
        if len(postData['lname']) <2:
            errors['lnamerequired'] = "Last Name must be at least 2 Characters!"
        elif len(usersWithEmail) >0:
            errors['emailtaken'] = "Email is taken, get creative"
        if len(postData['email']) < 5:
            errors['emailsmall'] = "Email must be at least 5 characters"
        if len(postData['pw']) <8:
            errors['pwrequired'] = "Password must be at least 8 characters"
        print(errors)
        return errors


    def loginValidator(self, postData):
        errors = {}
        usersWithEmail = User.objects.filter(email = postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        print(usersWithEmail)
        if len(usersWithEmail) ==0:
            errors['email'] = "Email doesnt exist. Please register first to login."
        else:
            user = usersWithEmail[0]
            if bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                print("password match")
            else:
                errors['pw'] = "invalid password"
        return errors

    def orgValidator(self, postData):
        errors = {}
        if len(postData['org']) <5:
                errors['orgtooshort'] = "Org name must be at least 5 characters"
        if len(postData['desc']) <10:
                errors['desctooshort'] = "Description should be 10 or more characters"
        return errors

    










class User(models.Model):
    firstName = models.CharField(max_length= 255)
    lastName = models.CharField(max_length= 255)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    


class Org(models.Model):
    orgname = models.CharField(max_length= 255)
    description = models.CharField(max_length= 255)
    joiner = models.ForeignKey(User, related_name = "joiners", on_delete = models.CASCADE)
    group = models.ManyToManyField(User, related_name = 'groups')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)