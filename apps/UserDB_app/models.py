from __future__ import unicode_literals
import bcrypt
import re
import datetime
from django.contrib import messages
from django.db import models

EMAILREGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAMEREGEX = re.compile(r'^[a-zA-Z]+$')
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Custom Validations:
class UserManager(models.Manager):
    # Message Form:
    def MessageForm_Validator(self, postData):
        errors = {}
        if len(postData['content']) < 5:
            errors["message_err"] = "Message must be more than 5 characters!"
        return errors
    # Comment Form:

    def CommentForm_Validator(self, postData):
        errors = {}
        if len(postData['com_content']) < 5:
            errors["message_err"] = "Comment must be more than 5 characters!"
        return errors
    # Reg Form:

    def RegForm_Validator(self, postData):
        errors = {}
        if not NAMEREGEX.match(postData['fName']):
            errors["fName"] = "First name must be valid characters only!"
        if len(postData['fName']) < 3:
            errors["fName"] = "First name should be at least 3 characters!"
        if not NAMEREGEX.match(postData['lName']):
            errors["lName"] = "Last name must be valid characters only!"
        elif len(postData['lName']) < 3:
            errors["lName"] = "Last name should be at least 3 characters!"
        if not EMAILREGEX.match(postData['email']):
            errors["email"] = "Email must be valid characters only!"

        # Passwords:
        if len(postData['password']) < 6:
            errors['password'] = "Your password needs to be at least 6 characters"
        if postData["confirm"] != postData["password"]:
            errors['confirm_pw'] = "Your passwords need to match"
        email_check = User.objects.filter(email=postData['email'])
        if email_check:
            errors['user_exists'] = "An Account Already Exists With That Email!"
        return errors

    # Login Form:
    # Nested if else as it is to ensure proper order depending on dominent error response
    def LogForm_Validator(self, postData):
        errors = {}
        # Email Vlidations:
        if len(postData['logpassword']) < 1:
            errors["logpassword"] = "Password Cannot Be Left Blank!"
        if len(postData['logemail']) < 1:
            errors["logemail"] = "Email Cannot Be Left Blank!"
        else:  # added these 2 validations in an else, to keep it from flashing if left blank.
            if not EMAILREGEX.match(postData['logemail']):
                errors['email'] = "Your Email Must Be In A Valid Format!"
            else:
                # Check If User Exists, if not throw error, if so, check password function:
                email = postData['logemail']
                if len(postData['logpassword']) < 1:
                    errors["logpassword"] = "Password Cannot Be Left Blank!"
                elif len(User.objects.filter(email=email)) == 0:
                    errors['user_exists'] = 'Account Does Not Exist!'
                else:
                    user = User.objects.get(email=postData['logemail'])
                    # Bcrypt Check PW Function:
                    if bcrypt.checkpw(postData['logpassword'].encode(), user.password.encode()):
                        print("PASSWORD MATCH!")
                        print("User Id:", user.id )
                    else:
                        print("PASSWORD INCORRECT!")
                        errors['pw_match'] = 'Password Incorrect!'
        return errors


class User(models.Model):
    email = models.TextField(max_length=50, unique=True)
    fName = models.TextField(max_length=20)
    lName = models.TextField(max_length=20)
    password = models.TextField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    content = models.TextField(max_length=255)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField(max_length=255)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="message_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
