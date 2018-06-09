from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator
from .models import tasklist
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import json
import logging
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def index(request):
    '''
        Index page / 
    '''
    return render(request, "index.html")

@csrf_exempt
def user_login(request):
    '''
        login page
            GET:-
                No parameters required, provides form to login
            POST:-
                @param username: username given while registration
                @param password: password given while registration
                Response:- if request successful redirect to index page
                           else redirect to login page
    '''
    try:
        if request.method == "GET":
            if request.user.is_authenticated():
                return redirect("/")
            return render(request, "login.html")
        elif request.method == "POST":
            request_data = request.POST.dict()
            username = request_data.get("username","")
            password = request_data.get("password","")
            logger.info("User login request for user {}".format(username))
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                logger.info("User {} logged in successfully".format(username))
                return redirect("/todo")
            else:
                logger.error("Login request fail for user {}".format(username))
                return render(request, "login.html", {"message": "Incorrect Username/password"})
    except Exception as e:
        logger.error("Error in login request {}".format(e))
        return redirect("/error")

@csrf_exempt
def user_register(request):
    '''
        User registration view
        GET:-  Render the registration page
        POST:- 
            @param username: Username is email and should be uniques 
            @param password: Password to login  later
            @param first_name: First name of user
            @param last_name: last name of user
            
            Response:
                create new user if given username field is unique else it will return error message
    '''
    try:
        if not request.user.is_authenticated():
            if request.method == "GET":
                return render(request, "register.html")
            elif request.method == "POST":
                request_data = request.POST.dict()
                username = request_data.get("email","")
                logger.info("User registration request for user {}".format(username))
                email = request_data.get("email","")
                password = request_data.get("password","")
                first_name = request_data.get("fname", "")
                last_name = request_data.get("lname", "")
                if username  and password and first_name and last_name:
                    if User.objects.filter(username=username).exists():
                        logger.error("User registration request failed for user {} as user already exist".format(username))
                        return render(request, "register.html", {"message":"User already exist", "flag":"error"})
                    user_obj = User.objects.create_user(username, email, password)
                    user_obj.first_name = first_name
                    user_obj.last_name = last_name
                    user_obj.save()
                    logger.info("User {} created ".format(username))
                    return render(request, "register.html", {"message":"Successfully registered, you can login now","flag":"success"})
                else:
                    logger.error("User {} registration failed as all fields are not given".format(username))
                    return render(request, "register.html", {"message":"All fields are mandatory"})
        else:
            return redirect("/")
    except Exception as e:
        logger.error("Error in Registration request {}".format(e))
        return redirect("/error")

@csrf_exempt
@login_required(login_url='/login')
def todo_operation(request):
    '''
        To create new task and get all created task by all user.
        GET:
            No parameters required
            Response:- Returns list of task objects
        POST:-
            @param title: Title of the task
            @param description: Description of task
            @param deadline: Deadline of task which is (optional)
            
            Response:- If successful redirect to todo page else return to error page
    '''
    try:
        if request.method == "GET":
            if request.user.is_authenticated():
                task_list = tasklist.objects.filter().order_by('created_at')
                return render(request, "todo.html", {"tasklist":task_list})
            return HttpResponse("You are not logged in.")
        
        elif request.method == "POST":
            
            request_data = request.POST.dict()
            logger.info("Task creation request from user {} for task {}".format(request.user, request_data))
            #datetime.strptime(a,'%Y-%m-%d'), title, description, created_at
            title = request_data.get("title", "")
            description = request_data.get("description", "")
            deadline = request_data.get("deadline", "")
            task_list_obj = tasklist()
            if title and description:
                task_list_obj.user = request.user
                task_list_obj.title = title
                task_list_obj.description = description
                if deadline:
                    deadline = datetime.strptime(deadline,'%Y-%m-%d')
                    task_list_obj.deadline = deadline
                task_list_obj.save()
                logger.info("Task created successfully {}".format(request_data))
                return redirect("/todo")
            else:
                logger.info("Task created successfully {}".format(request_data))
                return redirect("/todo", {"message":"Insufficient data, title and description required"})
    except Exception as e:
        logger.error("Error in Task operation request {}".format(e))
        return redirect("/error")

@csrf_exempt
@login_required(login_url='/login')
def change_status(request, tid):
    '''
        To change task status if its Done than change to Undone and if its Undone than change to Done
    '''
    try:
        if request.method == "PUT":
            if tid:
                task_list = tasklist.objects.get(id=tid)
                if task_list.status:
                    logger.info("status changed for task {} form Done to Undone".format(task_list.id))
                    task_list.status = False
                else:
                    logger.info("status changed for task {} form Undone to Done".format(task_list.id))
                    task_list.status = True
                task_list.status_change_by_id = request.user.id
                task_list.status_change_at = now()
                task_list.save()
                return HttpResponse(json.dumps({"message":"Status changed successfully"}), status=200, content_type="application/json")
            else:
                return HttpResponse(json.dumps({"message":"task id not given"}), status=400, content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message":"Method not allowed"}), status=503, content_type="application/json")
    except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"response":"Task not available"}), status=400)
    except Exception as e:
        logger.error("Error in change status request {}".format(e))
        print(str(e))
        return HttpResponse(json.dumps({"message":"data format error"}), status=400, content_type="application/json")

@csrf_exempt
@login_required(login_url='/login')
def your_todo_operation(request):
    
    '''
        Operations for tasks belongs to user
        GET:
            Will return all the tasks belongs to requested user. No parameters required
            
        POST:
            @param tid: task id
            @param title: New title/ changed title
            @param description: changed description
            
            Response:
                will return response as Done if success
                Else return error with message
         
    '''
    if request.method == "GET":
        try:
            task_list = tasklist.objects.filter(user=request.user)
            return render(request, "personaltodo.html", {"tasklist": task_list})
        except Exception as e:
            logger.error("Error in get all task {}".format(e))
            return redirect("/error")
                                                      
    elif request.method == "POST":
        try:
            request_data = request.POST.dict()
            tid = request_data.get("tid", "")
            title = request_data.get("title", "")
            description = request_data.get("description", "")
            logger.info("Edit task request for task id {} ".format(tid))
            if tid and title and description:
                tid = int(tid)
                task_list = tasklist.objects.get(id=tid)
                task_list.title = title
                task_list.description = description
                task_list.edited_at = now()
                if task_list.user.id  == request.user.id:
                    task_list.save()
                    logger.info("task edited with task id {} ".format(tid))
                    return HttpResponse(json.dumps({"response":"done"}), status=200)
                else:
                    logger.error("Unauthorized request to edit task {} ".format(tid))
                    response_data = {"response":"Unauthorized request."}
                    return HttpResponse(json.dumps(response_data),status=401)
            else:
                response_data = {"response":"Insufficient_data"}
                logger.info("Request with insufficient data to edit task {} ".format(request_data))
                return HttpResponse(json.dumps(response_data), status=400)
        except Exception as e:
            logger.error("Error in edit task request {}".format(e))
#             return HttpResponse(json.dumps({"data":str(e)}), status=400)
            return redirect("/error")


@csrf_exempt    
@login_required(login_url="/login")
def single_task_operation(request, tid):
    '''
        operation on single task.
        GET:
            @param tid: Task id
            Response:
            it will return single task details for passed tid. 
            
        DELETE:
            @param tid: Task id
            Response:
                It will delete task of taskid which is valid and request user is authorized too.
    '''
    if request.method == "GET":
        try:
            task = tasklist.objects.get(id=tid)
            if task:
                response_data = {}
                response_data["tid"] = task.id
                response_data["title"] = task.title
                response_data["description"] = task.description
                logger.info("task request for task id {} ".format(tid))
                return HttpResponse(json.dumps(response_data),status=200)
            else:
                response_data = {"response": "Data not available"}
                logger.error("Task not found for task id {}".format(tid))
                return HttpResponse(json.dumps(response_data),status=400)
        except Exception as e:
            logger.error("Error in single task {}".format(e))
            return redirect("/error")    
        
    
    elif request.method == "DELETE":
        try:
            tl = tasklist.objects.get(id=tid)
            logger.info("Delete request for task id {} ".format(tid))
            if tl and tl.user == request.user:
                tl.delete()
                logger.info("task deleted with task id {} ".format(tid))
                return HttpResponse(json.dumps({"response":"Deleted"}),status=200)
            else:
                logger.info("Unauthorized request to delete task {} ".format(tid))
                return HttpResponse(json.dumps({"response":"You can not delete this task"}),status=401)
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"response":"Task not available"}), status=400)
        except Exception as e:
            logger.error("Error in delete request {}".format(e))
            return redirect("/error")

def user_logout(request):
    '''
        logout for logged in user
    '''
    logout(request)
    return redirect("/")

def error(request):
    '''
        Error page
    '''
    return render(request, "error.html")