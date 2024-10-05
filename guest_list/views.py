from decouple import config
import openpyxl
import os, secrets, string
import pandas as pd
import qrcode
from email.mime.image import MIMEImage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Guest

# Create your views here.

def generate_random_string(length=9):
    
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def send_qr_code_email(subject, body_text, body_html, from_email, to_email, image_path, logo_path):
    msg = EmailMultiAlternatives(subject, body_text, from_email, [to_email])
    msg.attach_alternative(body_html, "text/html")

     # Attach the image
    with open(image_path, 'rb') as img:
        qr_image = MIMEImage(img.read())
        qr_image.add_header('Content-ID', '<qr_code>')
        msg.attach(qr_image)

    # Attach the logo image
    with open(logo_path, 'rb') as img:
        logo_image = MIMEImage(img.read())
        logo_image.add_header('Content-ID', '<logo_image>')
        msg.attach(logo_image)

    # Send the email
    try:
        msg.send()
        print('Email was sent successfully!')
    except Exception as e:
        print(f'An error occurred while sending email: {str(e)}')

    # Attach the image
    # with open(image_path, 'rb') as f:
    #     image_data = f.read()
    #     msg.attach(f.name, image_data, 'image/png')

def dashboard(request):
    guests = Guest.objects
    all_guests = guests.all()
    guest_count = guests.count()
    notified_guest_count = guests.filter(status='sent').count()
    not_notified_guest_count = guests.filter(status='not-sent').count()
    context = {
        'all_guests': all_guests,
        'guest_count' : guest_count,
        'notified_guest_count': notified_guest_count,
        'not_notified_guest_count': not_notified_guest_count
    }
    return render(request, 'dashboard.html', context=context)

def all_guests(request):
    guests = Guest.objects
    all_guests = guests.all()
    guest_count = guests.count()
    notified_guest_count = guests.filter(status='sent').count()
    not_notified_guest_count = guests.filter(status='not-sent').count()
    context = {
        'all_guests': all_guests,
        'guest_count' : guest_count,
        'notified_guest_count': notified_guest_count,
        'not_notified_guest_count': not_notified_guest_count
    }
    return render(request, 'all_guests.html', context=context)

def notified_guests(request):
    guests = Guest.objects
    notified_guests = guests.filter(status='sent').all()
    guest_count = guests.count()
    notified_guest_count = guests.filter(status='sent').count()
    not_notified_guest_count = guests.filter(status='not-sent').count()
    context = {
        'notified_guests': notified_guests,
        'guest_count' : guest_count,
        'notified_guest_count': notified_guest_count,
        'not_notified_guest_count': not_notified_guest_count
    }
    return render(request, 'notified_guests.html', context=context)

def not_notified_guests(request):
    guests = Guest.objects
    not_notified_guests = guests.filter(status='not-sent').all()
    guest_count = guests.count()
    notified_guest_count = guests.filter(status='sent').count()
    not_notified_guest_count = guests.filter(status='not-sent').count()
    context = {
        'not_notified_guests': not_notified_guests,
        'guest_count' : guest_count,
        'notified_guest_count': notified_guest_count,
        'not_notified_guest_count': not_notified_guest_count
    }
    return render(request, 'not_notified_guests.html', context=context)

def send_qr_to_one(request):
    if request.method == 'POST':
        guest_id = request.POST.get('id')
        guest = Guest.objects.get(pk=guest_id)
        if guest.status == 'not-sent':
            if guest:
                splited_email = guest.email.split('@')[0]
                send_qr_code_email(
                    subject='Your Fintech Week Program Registration QR Code',
                    body_text='',
                    body_html=f'''
                        <html>
                            <body style="font-size: 14px">

                                <h4>Dear {guest.first_name},</h4>
                                <p>Thanks for registering to attend Nigeria Fintech Week 2024!
                                We are absolutely thrilled to host you from the 8th - 10th of October 2024 at <b>Landmark Event Centre, </b>
                                4, Water Corporation Road, Victoria Island, Lagos, Nigeria.</p>
                                <p>Kindly find below the QR Code that grants you access to the event venue.</p>
                               <div style="text-align: center">
                                    <div style="display: inline-block; text-align: center;">
                                        <img src="cid:qr_code" alt="QR" style="width: 100px;" />
                                        <p>{guest.registration_code}</p>
                                    </div>
                                    <img src="cid:logo_image" alt="Fintech-Logo" style="display: inline-block; width: 100px; margin-left: 20px; margin-bottom: 45px;"/>
                                </div>
                                <h5 style="text-align: center">Do keep this code handy to fast track your entry.</h5>
                            </body>
                        </html>
                    ''',
                    from_email=config('DEFAULT_FROM_EMAIL'),
                    to_email=guest.email,
                    image_path=os.path.join(settings.BASE_DIR, 'guest_list', 'static', 'qr_codes', f'{guest.first_name}_{splited_email}.png'),
                    logo_path=os.path.join(settings.BASE_DIR, 'guest_list', 'static', 'img', 'logo.png'),
                )

                guest.status = 'sent'
                guest.save()
                return JsonResponse({'status': 200})
            return JsonResponse({'status': 404})
    return JsonResponse({'status': 403}) 

def send_qr_to_all(request):
    if request.method == 'POST':
        guests = Guest.objects.filter(status='not-sent').all()

        if guests:
            for guest in guests:
                splited_email = guest.email.split('@')[0]
                send_qr_code_email(
                    subject='Your Fintech Week Event Access QR Code',
                    body_text='',
                    body_html=f'''
                         <html>
                            <body style="font-size: 14px">
                                <h4>Dear {guest.first_name},</h4>
                                <p>Thanks for registering to attend Nigeria Fintech Week 2024!
                                We are absolutely thrilled to host you from the 8th - 10th of October 2024 at <b>Landmark Event Centre, </b>
                                4, Water Corporation Road, Victoria Island, Lagos, Nigeria.</p>
                                <p>Kindly find below the QR Code that grants you access to the event venue.</p>
                               <div style="text-align: center">
                                    <div style="display: inline-block; text-align: center;">
                                        <img src="cid:qr_code" alt="QR" style="width: 100px;" />
                                        <p>{guest.registration_code}</p>
                                    </div>
                                    <img src="cid:logo_image" alt="Fintech-Logo" style="display: inline-block; width: 100px; margin-left: 20px; margin-bottom: 45px;"/>
                                </div>
                                <h5 style="text-align: center">Do keep this code handy to fast track your entry.</h5>
                            </body>
                        </html>
                    ''',
                    from_email=config('DEFAULT_FROM_EMAIL'),
                    to_email=guest.email,
                    image_path=os.path.join(settings.BASE_DIR, 'guest_list', 'static', 'qr_codes', f'{guest.first_name}_{splited_email}.png'),
                    logo_path=os.path.join(settings.BASE_DIR, 'guest_list', 'static', 'img', 'logo.png'),
                )
                guest.status = 'sent'
                guest.save()

            return JsonResponse({'status': 200, 'message': 'QR Codes sent successfully to all guests'})
        return JsonResponse({'status': 404, 'message': "Your guest list is empty or you've already sent QR Code to all guests."})

def import_guest_list(request):
    if request.method == 'POST' and request.FILES['guest_list']:
        file = request.FILES['guest_list']

        try:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active
            
            for row in sheet.iter_rows(min_row=2, values_only=True):

                first_name, last_name, email = row
                
                if email:
                    # if not Guest.objects.filter(email=email).exists():
                    splited_email = email.split('@')[0]

                    # Generate a QR code
                    qr_data = f"Name: {first_name} {last_name}"
                    
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=6,
                        border=2,
                    )
                    qr.add_data(qr_data)
                    qr.make(fit=True)

                    # Generate the QR code image
                    qr_image = qr.make_image()
                    
                    # Save QR code to a directory
                    save_dir = os.path.join('guest_list/static/qr_codes')
                    qr_code_filename = f"{first_name}_{splited_email}.png"
                    qr_code_path = os.path.join(save_dir, qr_code_filename)
                    qr_image.save(qr_code_path)
                    
                        # Create a Guest instance and save to database
                    Guest.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        qr_code_path=qr_code_path,
                        registration_code=generate_random_string(9)
                    )

                    print(f"Inserted {email}")
                    # else:
                    #     print(f"<{email}> already exist. Skipping it.")
                else:
                    print("Email cannot be empty")
            return JsonResponse({'message': 'File imported and processed successfully.', 'status': 200}) 
        except Exception as e:
            return JsonResponse({'message': 'Something went wrong, try again.', 'status': 400})

def export_to_excel(request):
    guests = Guest.objects.all().values('first_name', 'last_name', 'email', 'status', 'registration_code')

    df = pd.DataFrame(list(guests))
    df.columns = ['First Name', 'Last Name', 'Email', 'Status', 'Registration Code']
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=guests_list.xlsx'
    
    df.to_excel(response, index=False)

    return response

def export_not_notified_to_excel(request):
    guests = Guest.objects.filter(status='not-sent').all().values('first_name', 'last_name', 'email', 'status', 'registration_code')

    df = pd.DataFrame(list(guests))
    df.columns = ['First Name', 'Last Name', 'Email', 'Status', 'Registration Code']
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=guests_list.xlsx'
    
    df.to_excel(response, index=False)

    return response

def export_notified_to_excel(request):
    guests = Guest.objects.filter(status='sent').all().values('first_name', 'last_name', 'email', 'status', 'registration_code')

    df = pd.DataFrame(list(guests))
    df.columns = ['First Name', 'Last Name', 'Email', 'Status', 'Registration Code']
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=guests_list.xlsx'
    
    df.to_excel(response, index=False)

    return response

