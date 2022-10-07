from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ProjectForm, TaskForm
from django.views.generic.detail import DetailView
  
from .models import Project, Task, TaskRequest, Skill
# Create your views here.
from django.http import HttpResponse
import plotly.graph_objects as go
import plotly.express as px
import datetime
def index(request) :
	return render(request,'home.html')

def register(request):
	skills = request.POST['skills']
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			#requests.post('localhost')
			messages.success(request, f'Your account has been created. You can log in now!')    
			return redirect('login')
	else:
		form = UserRegistrationForm()

	context = {'form': form, 'choices':Skill.choices}
	return render(request, 'register.html', context)

def main(request):
	if request.user.is_authenticated:
		own_set = request.user.own_project_set.all()
		ownExists = False
		for project in own_set:
			if not project.completed:
				ownExists = True
		total_set = request.user.project_set.all()
		totalExists = False
		for project in total_set:
			if not project.completed:
				totalExists = True
		return render(request, 'main.html', {'own_projects':own_set, 'projects':total_set, 'task_requests':request.user.taskrequest_set.all(), 'ownExists':ownExists, 'totalExists':totalExists})
	else:
		return redirect('login')


  
class ProjectDetailView(DetailView):
	# specify the model to use
	model = Project

	def get_context_data(self, *args, **kwargs):
		context = super(ProjectDetailView,
				self).get_context_data(*args, **kwargs)
		# add extra field 
		model_ = context['object']
		members = model_.members.all()
		members_freq_completed = {}
		weightwork = {}
		members_freq_incomplete = {}
		tasks = model_.task_set.all()
		user = self.request.user
		context['user'] = user
		ownExists = False
		totalExists = False
		usertasks = []
		for member in members:
			members_freq_completed[member.username] = 0
			members_freq_incomplete[member.username] = 0
			weightwork[member.username]=0
		history = {'x':[], 'y':[]}
		for task in tasks:
			if task.active:
				if task.Assigned.id == user.id:
					usertasks.append(task)
					if not task.completed:
						ownExists = True
				if task.completed:
					members_freq_completed[task.Assigned.username] += 1
					weightwork[task.Assigned.username] += task.weight
					history['x'].append(task.completionDate)
					history['y'].append(task.weight)
				else:
					totalExists = True
					members_freq_incomplete[task.Assigned.username] += 1
		x1 = []
		y1 = []

		for key in members_freq_completed:
			x1.append(key)
			y1.append(members_freq_completed[key])
		
		bar_completed = {'x':x1, 'y':y1}

		x1 = []
		y1 = []	
		for key in members_freq_incomplete:
			x1.append(key)
			y1.append(members_freq_incomplete[key])
		
		bar_incomplete = {'x':x1, 'y':y1}

		x1 = []
		y1 = []	
		for key in weightwork:
			x1.append(key)
			y1.append(weightwork[key])
		
		bar_weight = {'x':x1, 'y':y1}
		graphs = []
		if(history['x']):
			fig = px.histogram(x=history['x'], y=history['y'])

			graphs.append(fig.to_html())
		fig = px.bar(x=bar_weight['x'], y=bar_weight['y'],
					color=bar_weight['y'],
					labels={'x':'Username', 'y': 'Cumulative Weight Completed'}, height=400)
		graphs.append(fig.to_html())

		fig = px.bar(x=bar_completed['x'], y=bar_completed['y'],
					color=bar_completed['y'],
					labels={'x':'Username', 'y': 'Tasks Completed'}, height=400)
		graphs.append(fig.to_html())

		fig = px.bar(x=bar_incomplete['x'], y=bar_incomplete['y'],
					color=bar_incomplete['y'],
					labels={'x':'Username', 'y': 'Tasks Incomplete'}, height=400)
		graphs.append(fig.to_html())
		context['graphs'] = graphs
		context['tasks'] = tasks
		context['usertasks'] = usertasks
		context['ownExists'] = ownExists
		context['totalExists'] = totalExists

		return context

def createProject(request):
	if(request.user.is_authenticated):
		if request.method == "POST":
			project_form = ProjectForm(request.POST)
			if project_form.is_valid():
				obj = project_form.save(commit = False)
				obj.manager = request.user
				obj.save()
				obj.members.add(request.user)

				messages.success(request, ('Your Project was succesfully created'))
			else:
				messages.error(request, 'Error saving form')
				return redirect("createProject")
			
			
			return redirect("main")
		project_form = ProjectForm()
		return render(request=request, template_name="createProject.html", context={'form':project_form})
	else:
		return HttpResponse('Unauthorized', status = 401)

def acceptTask(request, pk):
	try:
		task_request = TaskRequest.objects.get(pk=pk)
	except Project.DoesNotExist:
		return HttpResponse('Error', status = 404)
	
	if request.user.is_authenticated and request.user.id == task_request.toUser.id:
		project = task_request.project
		task = task_request.task

		task.active = True
		task.save()
		if not request.user in project.members.all():
			project.members.add(request.user)
		task_request.delete()
		return redirect("projectview", pk = project.id)
	
	return HttpResponse('Unauthorized', status = 401)

def rejectTask(request, pk):
	try:
		task_request = TaskRequest.objects.get(pk=pk)
	except Project.DoesNotExist:
		return HttpResponse('Error', status = 404)
	
	if request.user.is_authenticated and request.user.id == task_request.toUser.id:
		task = task_request.task
		task_request.delete()
		task.delete()
		return redirect("main")
	
	return HttpResponse('Unauthorized', status = 401)


def createTask(request, pk):
	try:
		project = Project.objects.get(pk=pk)
	except Project.DoesNotExist:
		return HttpResponse('Error', status = 404)
	if(request.user.is_authenticated and request.user.id == project.manager.id):
		if request.method == "POST":
			
			task_form = TaskForm(request.POST)
			if task_form.is_valid():
				obj = task_form.save(commit = False)
				print(task_form.cleaned_data.get('Assigned'))
				try:
					assigned = User.objects.get(username = task_form.cleaned_data.get('Assigned'))
				except User.DoesNotExist:
					messages.error(request, 'Error user does not exist')
					return render(request=request, template_name="createTask.html", context={'form':task_form, 'project' : project})

				obj.project = project
				obj.Assigned = assigned
				obj.save()
				if(assigned.id != request.user.id):
					messages.success(request, ('Request has been succesfully sent, Task will be created once accepted'))
					task_request = TaskRequest(project = project, toUser = assigned, task = obj)
					task_request.save()
					return redirect("projectview", pk = project.id)
				
				obj.active = True
				if not assigned in obj.project.members.all():
					obj.project.members.add(assigned)
				obj.save()

				messages.success(request, ('Your Task was succesfully created'))
			else:
				messages.error(request, 'Error saving form')
				return render(request=request, template_name="createTask.html", context={'form':task_form, 'project' : project})
			
			
			return redirect("projectview", pk = project.id)
		task_form = TaskForm()
		return render(request=request, template_name="createTask.html", context={'form':task_form, 'project' : project})
	else:
		return HttpResponse('Unauthorized', status = 401)

def taskcompleted(request, pk, p_id):
	try:
		task = Task.objects.get(pk=pk)
	except Task.DoesNotExist:
		return HttpResponse('Error', status = 404)

	if(request.user.is_authenticated and (request.user.id == task.Assigned.id)):
		task.completed = True
		task.completionDate = datetime.date.today()
		task.save()

	return redirect("projectview", pk = p_id)

def projectcompleted(request, pk):
	try:
		project = Project.objects.get(pk=pk)
	except Task.DoesNotExist:
		return HttpResponse('Error', status = 404)

	if(request.user.is_authenticated and (request.user.id == project.manager.id)):
		project.completed = True
		project.save()

	return redirect("main")


