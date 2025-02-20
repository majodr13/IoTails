from django import forms

class RegistroUsuarioForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=100, widget=forms.TextInput(attrs={
        "placeholder": "Usuario",
        "class": "form-control"
    }))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={
        "placeholder": "Correo Electrónico",
        "class": "form-control"
    }))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        "placeholder": "Contraseña",
        "class": "form-control"
    }))
    confirm_password = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirmar Contraseña",
        "class": "form-control"
    }))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")

        return cleaned_data