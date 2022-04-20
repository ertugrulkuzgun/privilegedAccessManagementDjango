from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,label="Username",required=False)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput,label="Password",required=False)
    
    

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,label="Username ",required=True)
    password = forms.CharField(max_length=20, required=True,label="Password ",widget= forms.PasswordInput)
    confirm = forms.CharField(max_length=20, required=True,label="Confirm Password ",widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        if  password and confirm and password != confirm:
            raise forms.ValidationError("Passwords did not match.")

        values = {
            "username" : username,
            "password" : password
        }

        return values

class ExecuteCommand(forms.Form):
    command = forms.CharField(label="Enter Command")
