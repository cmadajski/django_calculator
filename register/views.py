from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from login.models import Login
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import logging

# keep track of password input
email_valid = False
first_password_input = ''
password_valid = False
password_repeat_valid = False

def register(request):
    return render(request=request, template_name="register.html", context=None)

@csrf_exempt
def check_register(request):
    # check if email field is empty
    if not request.POST.get('email'):
        messages.error(request, "ERROR: No email was given!")
        return redirect('/register/')
    elif not request.POST.get('password'):
        messages.error(request, 'ERROR: No password was given!')
        return redirect('/register/')
    else:
        # check if email is already in use
        try:
            check_email = Login.objects.get(email=request.POST.get('email'))
            messages.error(request, "ERROR: Cannot create new account. Email already exists in database!")
        except Login.DoesNotExist:
            new_user = Login(email=request.POST.get('email'), password=request.POST.get('password'))
            new_user.save()
            messages.success(request, f"SUCCESS: New user with email {request.POST.get('email')} has been created.")
            return redirect('/')
        else:
            return redirect('/register/')

@csrf_exempt
@require_POST
def check_registration_email(request):
    """
    Use HTMX to dynamically check user input for the email field during registration.
    """
    global email_valid
    valid_domains = ['.com', '.net', '.org', '.gov']
    curr_email = request.POST.get('email')
    email_already_exists = Login.objects.filter(email=curr_email).exists()
    if curr_email == '':
        email_valid = False
        logging.error(f'email valid: {email_valid}, pass valid: {password_valid}, repeat valid: {password_repeat_valid}')
        return HttpResponse('<div id="email-checker">&larr;</div>')
    elif '@' in curr_email and not email_already_exists and curr_email[-4:] in valid_domains:
        email_valid = True
        logging.error(f'email valid: {email_valid}, pass valid: {password_valid}, repeat valid: {password_repeat_valid}')
        return HttpResponse('<div id="email-checker" style="color:green;">&#10003;</div>')
    else:
        email_valid = False
        logging.error(f'email valid: {email_valid}, pass valid: {password_valid}, repeat valid: {password_repeat_valid}')
        return HttpResponse('<div id="email-checker" style="color:red;">&#10005;</div>')

@csrf_exempt
@require_POST
def check_registration_password(request):
    """
    Use HTMX to dynamically check user input for the password field during registration.
    """
    curr_password = request.POST.get('password')
    global first_password_input, password_valid
    first_password_input = curr_password
    if curr_password == "":
        password_valid = False
        return HttpResponse('<div id="password-checker">&larr;</div>')
    elif len(curr_password) > 8:
        password_valid = True
        return HttpResponse('<div id="password-checker" style="color:green;">&#10003;</div>')
    else:
        password_valid = False
        return HttpResponse('<div id="password-checker" style="color:red;">&#10005;</div>')

@csrf_exempt
@require_POST
def check_registration_password_repeat(request):
    """
    Use HTMX to dynamically check user input for the password repeat field during registration.
    """
    global password_repeat_valid
    curr_password_repeat = request.POST.get('password-repeat')
    if curr_password_repeat == '':
        password_repeat_valid = False
        return HttpResponse('<div id="password-repeat-checker">&larr;</div>')
    elif curr_password_repeat == first_password_input:
        password_repeat_valid = True
        return HttpResponse('<div id="password-repeat-checker" style="color:green;">&#10003;</div>')
    else:
        password_repeat_valid = False
        return HttpResponse('<div id="password-repeat-checker" style="color:red;">&#10005;</div>')

@csrf_exempt
@require_POST
def enable_register_button(request):
    """
    Use HTMX to enable or disable the submit button for the registration form.
    Enable/disable is based on validity of email, password, and password-repeat fields.
    """
    if email_valid and password_valid and password_repeat_valid:
        logging.error(f'email valid: {email_valid}, pass valid: {password_valid}, repeat valid: {password_repeat_valid}')
        return HttpResponse('<input id="register-button" type="submit" title="Click to register" name="register-button" value="Register &#10003;" style="font-size:24px;padding:10px;background-color:green;border-radius:5px;border:none;cursor:pointer;">')
    else:
        logging.error(f'email valid: {email_valid}, pass valid: {password_valid}, repeat valid: {password_repeat_valid}')
        return HttpResponse('<input id="register-button" type="submit" title="Valid email and password are required for registration" name="register-button" value="Register &#10005;" style="font-size:24px;padding:10px;background-color:red;border-radius:5px;border:none;" disabled>')