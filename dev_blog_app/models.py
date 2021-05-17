from django.db import models
import bcrypt
import re

# Create your models here.

class userManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) == 0:
            errors['fname'] = "First name is required!"
        elif len(postData['fname']) < 2:
            errors['fname'] = 'First name should at leat be 2 characters.'
        
        if len(postData['lname']) == 0:
            errors['lname'] = "FLast name is required!"
        elif len(postData['lname']) < 2:
            errors['lname'] = 'Last name should at leat be 2 characters.'

        if len(postData['useremail']) == 0:
            errors['useremail'] = "Email is required!"    
        elif not EMAIL_REGEX.match(postData['useremail']):          
            errors['useremail'] = "Invalid email address!"
        
        if len(postData['pwd']) == 0:
            errors['pwd'] = 'Password is required'
        elif len(postData['pwd']) < 8:
            errors['pwd'] = 'Password must be 8 characters.'
        
        if  postData['pwd'] != postData['confirmpwd']:
            errors['confirmpwd'] = 'Password must match'

        return errors
    def loginValidator(self, postData):
        errors = {}
        emailMatch = User.objects.filter(email = postData['useremail'])
        if len(emailMatch) == 0:
            errors['useremail'] = 'Email not found'
        elif not bcrypt.checkpw(postData['pwd'].encode(), emailMatch[0].password.encode()):
            errors['loginpw'] = 'Incorrect password.'
        # elif emailMatch[0].password != postData['pwd']:
        #     errors['loginpw'] = 'Incorrect password.'
        # bcrypt.checkpw('test'.encode(), hash1.encode())
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length = 60)
    email = models.EmailField()
    password = models.CharField(max_length = 25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()
    #entries = entries is the associated link to the User
    #assets = assets is the associated link to the User
    #user_comments = usercomments is the associated link to the User

    def __repr__(self):
        return f"<Users object: {self.first_name} {self.last_name}({self.id})>"

class Entry(models.Model):
    progress = models.CharField(max_length=280)
    thought = models.TextField()
    music = models.TextField()
    link = models.TextField()
    user_entry = models.ForeignKey(User, related_name='entries', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __repr__(self):
    #     return f"<Users object: {self.first_name} {self.last_name}({self.id})>"

class Asset(models.Model):
    articles = models.CharField(max_length=255)
    platforms = models.CharField(max_length=255)
    resources = models.CharField(max_length=255)
    code_book = models.CharField(max_length=255)
    book = models.CharField(max_length=255)
    asset_entry = models.ForeignKey(User, related_name="assets", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

    # def __repr__(self):
    #     return f"<Users object: {self.first_name} {self.last_name}({self.id})>"

class Comment(models.Model):
    comment_post = models.CharField(max_length=999)
    users = models.ForeignKey(User, related_name="user_comments", on_delete = models.CASCADE)
    entries = models.ForeignKey(Entry, related_name="entry_comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __repr__(self):
    #     return f"<Users object: {self.first_name} {self.last_name}({self.id})>"
