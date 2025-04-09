from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm,PasswordResetForm,PasswordChangeForm
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from .models import Task,SubTask
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox




class UserLoginform(AuthenticationForm):

    def __init__(self,*args,**kwargs):
        super(UserLoginform,self).__init__(*args,**kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter User or Email',
        'class':'form-control bg-light my-1'
        } ))


    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control bg-light my-1',
        'input':'data-mdb-input-init'

        }))
    
    captcha= ReCaptchaField(label="",widget=ReCaptchaV2Checkbox())
    
class RegisterForm(UserCreationForm):


    email = forms.CharField(widget=forms.EmailInput(attrs={

        'placeholder':'Enter email',
        'class':'form-control bg-light my-1'

    }))

    username = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter Username',
        'class':'form-control bg-light my-1'

    }))

    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={

        'placeholder':'Enter Password',
        'class':'form-control bg-light my-1'

    }))

    password2 = forms.CharField(label="Repeat password",widget=forms.PasswordInput(attrs={

        'placeholder':'Repeat password ',
        'class':'form-control bg-light my-1'

    }))


    captcha = ReCaptchaField(label="",widget=ReCaptchaV2Checkbox())

    usable_password = None

    class Meta:

        model = User

        fields=('username','email','password1','password2')


class UserForm(forms.ModelForm):

    class Meta:

        model = User
        fields=('username','email','first_name','last_name')

    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={

        'placeholder':'Enter Username',
        'class':'form-control bg-light my-1'
        }))
    
    email = forms.CharField(max_length=100,widget=forms.EmailInput(attrs={

        'placeholder':'Enter Email address',
        'class':'form-control bg-light my-1'

    }))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={

        'placeholder':'Enter First name',
        'class':'form-control bg-light my-1'

    }))

    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={

        'placeholder':'Enter Last name',
        'class':'form-control bg-light my-1'

    }))


class ResetPasswordForm(PasswordResetForm):

    def __init__(self,*args,**kwargs):
        super(ResetPasswordForm,self).__init__(*args,**kwargs)


    email = forms.CharField(label="",widget=forms.EmailInput(attrs={

        'placeholder':'Enter your email address',
        'class':'form-control my-3'

    }))

    #captcha= ReCaptchaField(label="",widget=ReCaptchaV2Checkbox())



class ChangePasswordForm(PasswordChangeForm):


    old_password = forms.CharField(widget = forms.PasswordInput(attrs={

        'placeholder':'Enter old password',
        'class':'form-control',

    })) 

    new_password1 = forms.CharField(label='New password ',widget = forms.PasswordInput(attrs={

        'placeholder':'Enter new password ',
        'class':'form-control',

    }))

    new_password2 = forms.CharField(label='Retype New Password',widget = forms.PasswordInput(attrs={

        'placeholder':'Repeat new password',
        'class':'form-control',

    }))



class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields=('title','start_date','start_time','due_date','due_time')

    
    title = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={

        "placeholder":"Enter task title",
        "class":"form-control form-control-sm"
    }))


    start_date = forms.DateField(required=True,widget=DatePickerInput(attrs={
        "placeholder":"Enter start date",
        'class':'form-control form-control-sm '
    }))

    start_time = forms.TimeField(widget=TimePickerInput(attrs={
        "placeholder":"Enter start time",
        'class':'form-control form-control-sm',
              
    }))

    due_date  = forms.DateField(required=True,widget=DatePickerInput(attrs={
        "placeholder":"Enter due date",
        'class':'form-control form-control-sm',
    }))

    due_time = forms.TimeField(widget=TimePickerInput(attrs={
        "placeholder":"Enter due time",
        'class':'form-control form-control-sm',
              
    }))

    
class UpdateTaskform(forms.ModelForm):

    class Meta:
        model = Task
        fields=('title','note','start_date','start_time','due_date','due_time','status')


    title = forms.CharField(label="",max_length="100",widget=forms.TextInput(attrs={
        "placeholder":"Enter task title",
        "class":"form-control form-control-sm"
    }))

    note = forms.CharField(max_length=500,required=False,widget=forms.Textarea(attrs={

        "placeholder":"Enter note",
        "class":"form-control form-control-sm" 
    }))


    start_date = forms.DateField(widget=DatePickerInput(attrs={
        "placeholder":"Enter start date",
        'class':'form-control form-control-sm '
    }))

    start_time = forms.TimeField(widget=TimePickerInput(attrs={
        "placeholder":"Enter start time",
        'class':'form-control form-control-sm',
              
    }))

    due_date  = forms.DateField(widget=DatePickerInput(attrs={
        "placeholder":"Enter due date",
        'class':'form-control form-control-sm',
    }))

    due_time = forms.TimeField(widget=TimePickerInput(attrs={
        "placeholder":"Enter due time",
        'class':'form-control form-control-sm',
              
    }))

    STATUS=[

        ('W', 'Waiting'),
        ('I', 'Inprogress'),
        ('S', 'Success'),
        ('F', 'Failed'),
        ('O', 'Overdue'),

    ]


    status = forms.ChoiceField(
        
        choices=STATUS,
        widget=forms.Select(attrs={
         
            'class':'form-select form-control fw-bolder my-1'
            
        })

    )



class CreateSubTaskForm(forms.ModelForm):

    class Meta:
        model = SubTask
        fields = ('title',)

    
    title = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={

        "placeholder":'Enter Subtitle',
        "class":"form-control",
    }))
        
 
class UpdateSubTaskForm(forms.ModelForm):

    class Meta:
        model = SubTask
        fields = ('title','subnote')

    
    title = forms.CharField(label="",max_length=100,widget=forms.TextInput(attrs={

        "placeholder":'Enter Subtitle',
        "class":"form-control",
    }))
        
    subnote = forms.CharField(max_length=500,required=False,widget=forms.Textarea(attrs={

        "placeholder":"Enter note",
        "class":"form-control form-control-sm" 
    }))

