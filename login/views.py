from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from login.models import Login
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse

# for login validation

email_is_valid = False
email_address = ''
password_is_valid = False

def index(request):
    if request.session.get('logged_in'):
        return redirect('/calc/')
    else:
        return render(request=request, template_name="index.html", context=None)

@csrf_exempt
@require_POST
def check_login(request):
    form_email = request.POST.get("email")
    try:
        requested_user = Login.objects.get(email=form_email)
    except Login.DoesNotExist:
        messages.error(request, "ERROR: Email is not associated with an account. Click \"Register\" to sign up.")
        return redirect('/')
    else:
        form_pass = request.POST.get("password")
        if requested_user.password == form_pass:
            request.session['logged_in'] = True
            messages.success(request, f"SUCCESS: Logged in as {request.POST.get('email')}")
            return redirect('/calc/')
        else:
            messages.error(request, "ERROR: Password not valid for given email!")
            return redirect('/')

@csrf_exempt
def check_login_email(request):
    global email_is_valid, email_address
    curr_email = request.POST.get('email')
    if curr_email == '':
        print('CURR EMAIL VALUE IS: EMPTY')
        email_is_valid = False
        email_address = ''
        return HttpResponse('<div id="email-check">&larr;</div>')
    elif Login.objects.filter(email=curr_email).exists():
        email_is_valid = True
        email_address = curr_email
        print(f'EMAIL IS VALID: {email_is_valid}')
        return HttpResponse('<div id="email-check" style="color:green;">&#10003;')
    else:
        email_is_valid = False
        email_address = ''
        print(f'EMAIL IS VALID: {email_is_valid}')
        return HttpResponse('<div id="email-check" style="color:red;">&#10005;</div>')

@csrf_exempt
def check_login_password(request):
    global email_is_valid, email_address, password_is_valid
    # if valid email has been provided
    curr_password = request.POST.get('password')
    if curr_password == '':
        password_is_valid = False
        print('PASSWORD IS VALID: EMPTY')
        return HttpResponse('<div id="password-check">&larr;</div>')
    elif email_is_valid:
        curr_user = Login.objects.get(email=email_address)
        password_attempt = curr_password
        # if valid password is provided for valid email, enable login button
        if password_attempt == curr_user.password:
            password_is_valid = True
            return HttpResponse('<div id="password-check" style="color:green;">&#10003;')

        # if password is invalid, keep login button disabled
        else:
            password_is_valid = False
            print(f'EMAIL IS VALID: {email_is_valid}')
            print(f'PASS IS VALID: {password_is_valid}')
            return HttpResponse('<div id="password-check" style="color:red;">&#10005;</div>')
    # if no valid email has been provided, no password checking can be done
    else:
        password_is_valid = False
        return HttpResponse('<div id="password-check" style="color:red;">&#10005;</div>')

@csrf_exempt
def enable_login_button(request):
    global email_is_valid, password_is_valid
    if email_is_valid and password_is_valid:
        return HttpResponse('<input id="login-button" type="submit" title="Click to login" name="submit" value="Login &#10003;" style="display:block;padding:10px;font-size:24px;width:fit-content;background-color:rgb(0, 211, 0);border-radius:5px;border:none;cursor:pointer;transition:0.2s;">')
    else:
        return HttpResponse('<input id="login-button" type="submit" title="Valid email and password are required before logging in" name="submit" value="Login &#10005;" style="display:block;padding:10px;font-size:24px;width:fit-content;background-color:red;border-radius:5px;border:none;cursor:pointer;transition:0.2s;" disabled>')

def logout(request):
    request.session.flush()
    messages.success(request, "SUCCESS: Logged out of calculator")
    return redirect('/')