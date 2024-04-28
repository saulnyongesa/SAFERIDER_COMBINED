from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import *
from base.models import *
from .mpesa import *
from .twilio_utils import send_message


# create a view set
@api_view(['GET'])
def get_user(request, pk):
    user = User.objects.get(username=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def user_login(request, pk):
    user = User.objects.get(username=pk)
    serializer = UserLoginSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def emergency_contact(request, pk, lon,lat):
    user = User.objects.get(username=pk)
    stage = Stage.objects.get(id=user.stage_id)
    emer_contact = EmergencyContact.objects.filter(name__stage_id=stage.id)
    subject = "Emergency Alert!"
    message = (user.first_name + " " + user.last_name + " Pressed an Emergency Button\n" +
               user.first_name + " " + user.last_name + " is a "
                                                        "Member of\nStage Name: " + stage.stage_name +
               "\nStage Number: " + stage.stage_number +
               "\nHE NEEDS YOUR IMMEDIATE HELP/ASSISTANCE")
    emergency = Emergency.objects.create(
        sender=user,
        lon=lon,
        lat=lat
    )
    emergency.save()
    receiver_email = []
    for email in emer_contact:
        receiver_email.append(email.name.email)
    send_mail(
        subject,
        message,
        user.email,
        receiver_email
    )
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def fare_payment(request, pk, phone, amount):
    user = User.objects.get(username=pk)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    call_back_url = 'https://upward-husky-marginally.ngrok-free.app/fare-pay/' + user.username
    headers = {"Authorization": "Bearer %s" % access_token}
    if access_token and api_url and headers:
        request_payload = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": call_back_url,
            "AccountReference": "FarePayment",
            "TransactionDesc": "Fare Payment",
        }
        response = requests.post(api_url, json=request_payload, headers=headers)
        if response.status_code == 200:
            serializer = UserLoginSerializer(user, many=False)
            return JsonResponse(serializer.data)
        else:
            return HttpResponse("Failed to initiate payment", status=response.status_code)
    else:
        return HttpResponse("Invalid access token, API URL, or headers", status=500)


@csrf_exempt
def mpesa_callback(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        data = data.get('Body', {})
        if data:
            amount = data['stkCallback']['CallbackMetadata']['Item'][0]['Value']
            mpesa_receipt_number = data['stkCallback']['CallbackMetadata']['Item'][1]['Value']
            transaction_date = data['stkCallback']['CallbackMetadata']['Item'][2]['Value']
            phone_number = data['stkCallback']['CallbackMetadata']['Item'][3]['Value']

            user = User.objects.get(username=pk)

            transaction = Customer.objects.create(
                boda_name=user,
                amount=amount,
                fare_transaction_id=mpesa_receipt_number,
                created=transaction_date,
                customer_phone_number=phone_number
            )
            transaction.save()
            return redirect('admin-dashboard-url')

        else:
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def send_message_view(request):
    if request.method == 'POST':
        to_number = request.POST.get('to_number')
        message_body = request.POST.get('message_body')

        try:
            send_message(to_number, message_body)
            return JsonResponse({'success': True, 'message': 'Message sent successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
