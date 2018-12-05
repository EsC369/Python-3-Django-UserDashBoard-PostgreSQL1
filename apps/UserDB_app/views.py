from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from time import gmtime, strftime
import bcrypt
import re
from .models import *
from django.db.models import Q
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    return render(request, "UserDB_app/index.html")
def logpage(request):
    return render(request, "UserDB_app/login.html")
def regpage(request):
    return render(request, "UserDB_app/register.html")

def showUser(request, id):
    user = User.objects.get(id = id)
    userMessage = Message.objects.filter(user=user)
    userMessages = userMessage.all().order_by("-created_at")
    msgCount = len(userMessages)

    context={
        "userMessages": userMessages,
        "id": user,
        "user": user,
        "msgCount": msgCount,
    }
    return render(request, "UserDB_app/showUser.html", context)

def showMsg(request, id):
    message = Message.objects.get(id = id)
    commentMsgs = Comment.objects.filter(message=message)
    msgUser = message.user
    comUser_id = request.session['id']
    comment_id = Comment.objects.filter(user=comUser_id)
    comments = Comment.objects.all().order_by("-created_at")
    comCount = len(commentMsgs)
    context={
        "user": msgUser,
        "msgUser": msgUser,
        "comUser": comUser_id,
        "comment": comment_id,
        "comments": comments,
        "message": message,
        "comCount": comCount,
        "commentMsgs": commentMsgs  # all comments for said msg
    }
    return render(request, "UserDB_app/showMsg.html", context)

def message(request):
    id = request.session['id']
    user = User.objects.get(id=id)
    if request.method == "POST":
        # Check errors
        errors = User.objects.MessageForm_Validator(request.POST)
        if len(errors):
            userMessages = Message.objects.all().order_by("-created_at")
            context = {"userMessages": userMessages}
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, "UserDB_app/success.html", context)
        else:
            # Process Post Data:
            content = request.POST["content"]
            # Create Message And Export:
            message = Message.objects.create(content=content, user=user)
            userMessages = Message.objects.all().order_by("-created_at")
            context = {"userMessages": userMessages, "message": message}
        return render(request, "UserDB_app/success.html", context)

def msgComment(request):
    id = request.session['id']
    user = User.objects.get(id=id)
    if request.method == "POST":
        # Check errors
        errors = User.objects.CommentForm_Validator(request.POST)
        if len(errors):
            comments = Comment.objects.all()
            message = Message.objects.get(id=int(request.POST["message_id"]))
            messageUser = message.user
            
            context = {"comments": comments, "message": message, "messageUser": messageUser, "user": messageUser}
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, "UserDB_app/showMsg.html", context)
        else:
            comUser_id = request.session['id']
            print("Post Comment User id:", comUser_id)       
            # Process Post Data:
            content = request.POST["com_content"]
            message = Message.objects.get(id=int(request.POST["message_id"]))
            messageUser = message.user
            # Create Message And Export:
            comment = Comment.objects.create(content=content, user=user, message=message)
            comment_id = comment.id
            print(" Post comment id:", comment_id)
            commentMsg = Comment.objects.filter(message=message)
            comments = commentMsg.all().order_by("-created_at")
            context = { "comUser": comUser_id, "comment": comment_id,"comments": comments, "messageUser": messageUser, "message": message, "user": messageUser }
        return render(request, "UserDB_app/showMsg.html", context)  

def register(request):
    if request.method == "POST":
        # Check errors
        errors = User.objects.RegForm_Validator(request.POST)
        if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/regpage')
        else:
            # Process:
            fName = request.POST['fName']
            lName = request.POST['lName']
            email = request.POST['email']
            password = request.POST['password']
            hashedPass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            # Create User And Export:
            user = User.objects.create(email=email, fName=fName, lName=lName, password=hashedPass.decode("utf-8"))
            request.session['id'] = User.objects.get(email=email).id
            userMessages = Message.objects.all().order_by("-created_at")
            comments = Comment.objects.all().order_by("-created_at")
            context = {"user": user, "userMessages": userMessages, "comments": comments }
        return render(request, "UserDB_app/success.html", context)

def login(request):
    if request.method == "POST":
        # Check errors
        errors = User.objects.LogForm_Validator(request.POST)
        if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/logpage')
        else:
            email = request.POST['logemail']
            user = User.objects.get(email=email)
            password = user.password
            request.session['id'] = user.id
            userMessages = Message.objects.all().order_by("-created_at")
            context = {
                "user": user,
                "userMessages": userMessages,
            }
        return render(request, "UserDB_app/success.html", context)

def success(request):
    # Check if user is logged in with session, if not boot back to root
    if 'id' in request.session:
        id = request.session['id']

        #Proccess Eveerything to show on success
        user = User.objects.get(id=id)

        # Query Message Search:
        query = request.GET.get("search")
        userMessages = Message.objects.all().order_by("-created_at")
        if query:
            #Query all messages and filter by is some content __icontains which searches for any simularities. NOTE THE FILTER CALL!
            # note utilizing db.models Q for multiple query searches! To also search for user name as well!
            # Searching for content OR User name
            userMessages = userMessages.filter(
                Q(content__icontains=query)|
                Q(user__fName__icontains=query)|
                Q(user__lName__icontains=query)
                )
            context = {"user": user, "userMessages":userMessages}
            return render(request, "UserDB_app/success.html", context)
        else: 
            userMessages = Message.objects.all().order_by("-created_at")
            context = {"user": user, "userMessages":userMessages}
            return render(request, "UserDB_app/success.html", context)
    else:
        return redirect("/login")

def logout(request):
    request.session.clear()
    return redirect("/logpage")

def delete(request, id):
    message = Message.objects.get(id=id).delete()
    return redirect("/success")

def deleteComment(request, id, msg_id):
    comment = Comment.objects.get(id=id).delete()
    return redirect("/showMsg/" + str(msg_id))




