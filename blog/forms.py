from django import forms
from blog.models import Post, Comment
from django.contrib.auth.models import User
# STATUS = (
#     (0,"Draft"),
#     (1,"Publish")
# )

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter title.'}), required=True, max_length=500)
    poster = forms.ImageField(required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter content.'}), required=True,)
    
    
    class Meta():
        model=Post
        exclude =['author', 'slug']

class CommentForm(forms.ModelForm):
    
    #title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter title.'}), required=True, max_length=200)
    #content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter content.'}), required=True, max_length=200)
    #status = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter status.'}), required=True,)
    
    class Meta():
        model= Comment
        exclude=['post']

class Add_Profile(forms.ModelForm):

    # email_id=forms.CharField(widget=forms.EmailInput)
    dob=forms.DateField(
        widget=forms.DateInput(
        attrs={
        'type':'date',
        }
        )
    )
#     user = forms.CharField(
#     widget=forms.TextInput(attrs={'readonly':'readonly'})
# )
