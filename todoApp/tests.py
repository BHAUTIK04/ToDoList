from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
import json

class RegisterUserTest(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.fake_user = {
            'username': 'fakeuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        
    def test_user_login_success(self):
        response = self.client.post('/login', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
    
    def test_user_login_fail(self):
        response = self.client.post('/login', self.fake_user, follow=True)
        self.assertFalse(response.context['user'].is_active)
 
 
class TodoOperationTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.user)
           
    def test_create_todo(self):
        esp = self.client.post('/login', self.user, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        response = self.client.post('/todo', data, follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url=="/todo")
        self.assertTrue(status_code==302)
    
    def test_get_todo(self):
        self.client.post('/login', self.user, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        self.client.post('/todo', data, follow=True)
        response = self.client.get('/todo', follow=True)
        self.assertTrue(response.context["tasklist"][0].title  == "test")
        self.assertTrue(response.context["tasklist"][0].description  == "this is testcase")


class ChangeStatus(TestCase):
    def setUp(self):
        self.user = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.user)
        
    def test_status_change_success(self):
        self.client.post('/login', self.user, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        self.client.post('/todo', data, follow=True)
        response = self.client.get('/todo', follow=True)
        tid = response.context["tasklist"][0].id
        previous_status = response.context["tasklist"][0].status
        self.client.post('/statuschange',{"tid": tid},follow=True)
        response = self.client.get('/todo', follow=True)
        self.assertFalse(response.context["tasklist"][0].status == previous_status)
        
    def test_status_tid_not_given(self):
        self.client.post('/login', self.user, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        self.client.post('/todo', data, follow=True)
        response = self.client.post('/statuschange',{"tid": ""},follow=True)
        self.assertTrue(response.json()["message"] == "task id not given")
        
class EditTaskTest(TestCase):
    
    def setUp(self):
        self.user = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.user)
        
    def test_edit_task_success(self):
        self.client.post('/login', self.user, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        # create task
        create_response = self.client.post('/todo', data, follow=True)
        # get task
        get_response = self.client.get('/todo', follow=True)
        tid = get_response.context['tasklist'][0].id
        edit_data = {"title":"Edited test", "description":"this is testcase", "tid": tid}
        # edit task request
        self.client.post('/yourtodo', edit_data, follow=True)
        response = self.client.get('/todo', follow=True)
        title = response.context["tasklist"][0].title
        self.assertTrue(title == edit_data['title'])
        self.assertFalse(title == data['title'])
        
    def test_edit_task_fail(self):
        self.client.post('/login', self.user, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        # create task
        create_response = self.client.post('/todo', data, follow=True)
        # get task
        get_response = self.client.get('/todo', follow=True)
        tid = get_response.context['tasklist'][0].id
        edit_data = {"title":"Edited test", "description":"this is testcase"}
        # edit task request
        edit_response = self.client.post('/yourtodo', edit_data, follow=True)
        response = json.loads(edit_response.content.decode("utf-8"))
        self.assertTrue(response['response'] == "Insufficient_data")
        self.assertTrue(edit_response.status_code == 400)
        
class DeleteTaskTest(TestCase):
    def setUp(self):
        self.user1 = {
            'username': 'testuser1',
            'password': 'secret'}
        self.user2 = {
            'username': 'testuser2',
            'password': 'secret'}
        User.objects.create_user(**self.user1)
        User.objects.create_user(**self.user2)
        
    def test_delete_task_success(self):
        self.client.post('/login', self.user1, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        # create task
        create_response = self.client.post('/todo', data, follow=True)
        # get task
        get_response = self.client.get('/todo', follow=True)
        tid = get_response.context['tasklist'][0].id
        edit_data = {"title":"Edited test", "description":"this is testcase"}
        # edit task request
        delete_response = self.client.delete('/task/'+str(tid), follow=True)
        response = json.loads(delete_response.content.decode("utf-8"))
        self.assertTrue(response['response'] == "Deleted")
        self.assertTrue(delete_response.status_code == 200)
    
    def test_delete_task_wrong_task_id_failed(self):
        self.client.post('/login', self.user1, follow=True)
        tid = 100
        edit_data = {"title":"Edited test", "description":"this is testcase"}
        # edit task request
        delete_response = self.client.delete('/task/'+str(tid), follow=True)
        
        response = json.loads(delete_response.content.decode("utf-8"))
        self.assertTrue(response['response'] == "Task not available")
        self.assertTrue(delete_response.status_code == 400)
        
    def test_delete_task_different_user_failed(self):
        self.client.post('/login', self.user1, follow=True)
        data = {"title":"test", "description":"this is testcase"}
        # create task
        create_response = self.client.post('/todo', data, follow=True)
        get_response = self.client.get('/todo', follow=True)
        tid = get_response.context['tasklist'][0].id
        self.client.get('/logout', follow=True)
        
        self.client.post('/login', self.user2, follow=True)
        delete_response = self.client.delete('/task/'+str(tid), follow=True)
        response = json.loads(delete_response.content.decode("utf-8"))
        self.assertTrue(response['response'] == "You can not delete this task")
        self.assertTrue(delete_response.status_code == 401)