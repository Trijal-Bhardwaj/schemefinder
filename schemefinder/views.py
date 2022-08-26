from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from authentication.models import BeneficiaryDetails, AgencyDetails, BenificiaryAgencyRelation
from datetime import datetime
from django.urls import reverse

def home(request):
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        context = {}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'schemes.html', context)
        else:
            context['error'] = "Incorrect username/password"
            return render(request, 'login.html', context)

    return render(request, 'login.html')


def registration(request):
    return render(request, 'get_beneficiary_registration.html')


def index(request):
    if request.method == 'POST':
        try:
            context = {}
            first_name = request.POST['str_fname']
            middle_name = request.POST['str_mname']
            last_name = request.POST['str_lname']
            father_name = request.POST['benef_father_name']
            mother_name = request.POST['benef_mother_name']
            salutation = request.POST['salutation']
            gender = request.POST['num_gender']
            occupation = request.POST['num_occupation_id']
            dob = request.POST['dt_dob']
            dob = datetime.strptime(dob, "%d/%m/%Y")
            age = datetime.today().year - dob.year
            category = request.POST['num_category_id']
            address = request.POST['str_houseNo'] + ', ' + request.POST['str_Street'] + ', ' + request.POST['Str_Area'] + ', ' + request.POST['str_tehsil']
            pin_code = request.POST['num_pincode']
            assistive_device = request.POST['aid_type']
            aadhaar = request.POST['benef_adhaar_no']
            udid = request.POST['str_udid_cardno']
            mobile = request.POST['str_mobile_no']
            imparement = request.POST['num_disability_type']
            imparement_per = request.POST['num_disability_persentage']
            imparement_certificate = request.FILES['disability_certificate']
            income_certificate = request.FILES['income_certificate']
            photo = request.FILES['files']
            

            context['name'] = request.POST['str_fname'] + ' ' +  request.POST['str_mname'] + ' ' + request.POST['str_lname']
            context['father_name'] = request.POST['benef_father_name']
            context['mother_name'] = request.POST['benef_mother_name']
            context['dob'] = request.POST['dt_dob']
            context['category'] = request.POST['num_category_id']
            context['address'] = request.POST['str_houseNo'] + ', ' + request.POST['str_Street'] + ', ' + request.POST['Str_Area'] + ', ' + request.POST['str_tehsil'] + ', ' + request.POST['num_pincode']
            context['aadhaar'] = request.POST['benef_adhaar_no']
            context['udid'] = request.POST['str_udid_cardno']
            context['mobile'] = request.POST['str_mobile_no']
            context['impairement'] = request.POST['num_disability_type']
            context['impairement_per'] = request.POST['num_disability_persentage']

            # print (context)
            beneficiary = BeneficiaryDetails.objects.create(
                udid=udid, aadhaar=aadhaar, mobile=mobile, first_name=first_name,
                middle_name=middle_name, last_name=last_name, father_name=father_name, mother_name=mother_name,
                imparement=imparement, imparement_per=imparement_per, dob=dob,
                salutation=salutation, gender=gender, age=age, category=category,
                address=address, pincode=pin_code, occupation=occupation,
                income=0, assistive_device='Cochlear Implants',
                imparement_certificate=imparement_certificate, 
                income_certificate=income_certificate, photo=photo
            )
            # print("********\n", beneficiary)
            beneficiary.save()

            return render(request, 'index.html', {'context':context})
        except:
            return render(request, 'index.html')

    return render(request, 'index.html')

def agency_index(request, username=None, password=None):
    if not username:
        username = request.POST.get('agency_username', None)
        password = request.POST.get('agency_password', None)

    # organisation_type = request.POST.get('orgType', None)
    # if organisation_type:
    #     redirect('agency_registration', request)
    # try:
    print("#########")
    print(username, password)
    AgencyDetails.objects.get(username=username, password=password)
    return render(request, 'index1.html', get_beneficiary_json(request, True, username))
    # except:
    #     return redirect('../')

def agency_registration(request):
    if request.method == 'POST':
        # print(request.POST)
        username = request.POST['agency_username']
        password = request.POST['password']
        type = request.POST['orgType']
        name = request.POST['orgName']
        address = request.POST['orgAddress']
        country = request.POST['orgCountryId']
        state = request.POST['orgStateId']
        district = request.POST['orgDistId']
        pin_code = request.POST['orgPincode']
        phone = request.POST['orgContactNumber']
        fax_number = request.POST['orgFaxNumber']
        pan_number = request.POST['orgPanNumber']
        website = request.POST['orgWebsite']
        cin_number = request.POST['cin']
        support_name = request.POST['contactPersonName']
        support_designation = request.POST['contactPerDesg']
        support_email = request.POST['contactPersonMobileNo']
        support_phone = request.POST['contactPersonEmail']
        address_proof = request.POST['addressProofDocument']

        agency = AgencyDetails.objects.create(
            username=username, password=password, type=type,
            name=name, address=address, country=country,
            state=state, district=district, pin_code=pin_code,
            phone=phone, fax_number=fax_number, pan_number=pan_number,
            website=website, cin_number=cin_number, support_name=support_name,
            support_designation=support_designation, support_email=support_email,
            support_phone=support_phone, address_proof=address_proof
        )
        agency.save()

        return render(request, 'index1.html', get_beneficiary_json(request, True))
    return render(request, 'agencyRegistration.html')

def get_beneficiary_json(request, flag=False, username=None):
    if not username:
        username = request.POST.get('agency_username', None)
    if not username:
        username = request.GET['agency_username']
    # agency = AgencyDetails.objects.get(username=username)
    beneficiary_list = BeneficiaryDetails.objects.all()
    # relation = BenificiaryAgencyRelation.objects.filter(agency__id=agency.id, beneficiary__in=beneficiary)
    context = []
    detail = {}

    index = 1
    for beneficiary in beneficiary_list:
        detail['S.No.'] = index
        detail['Beneficiary Name'] = beneficiary.get_name()
        detail['Father Name'] = beneficiary.father_name
        detail['Mother Name'] = beneficiary.mother_name
        detail['Date Of Birth'] = beneficiary.dob
        detail['Category'] = beneficiary.category
        detail['Address'] = beneficiary.address
        detail['Aadhar Card No.'] = beneficiary.aadhaar
        detail['udid'] = beneficiary.udid
        detail['Mobile No'] = beneficiary.mobile
        detail['Disability Type'] = beneficiary.imparement
        detail['Disability Percentage'] = beneficiary.imparement_per
        detail['Documents'] = [ '/media/'+str(beneficiary.imparement_certificate), 
                                '/media/'+str(beneficiary.income_certificate),
                                '/media/'+str(beneficiary.category_certificate),
                                '/media/'+str(beneficiary.photo)]
        detail['Status'] = beneficiary.verification_status
        context.append(dict(detail))

    if flag:
        return {'context':context, 'username': username}
    else:
        return JsonResponse(context, safe=False)


def beneficiary_index(request):
    if request.method == 'POST':
        try:
            context = {}
            first_name = request.POST['str_fname']
            middle_name = request.POST['str_mname']
            last_name = request.POST['str_lname']
            father_name = request.POST['benef_father_name']
            mother_name = request.POST['benef_mother_name']
            salutation = request.POST['salutation']
            gender = request.POST['num_gender']
            occupation = request.POST['num_occupation_id']
            dob = request.POST['dt_dob']
            dob = datetime.strptime(dob, "%d/%m/%Y")
            age = datetime.today().year - dob.year
            category = request.POST['num_category_id']
            address = request.POST['str_houseNo'] + ', ' + request.POST['str_Street'] + ', ' + request.POST['Str_Area'] + ', ' + request.POST['str_tehsil']
            pin_code = request.POST['num_pincode']
            assistive_device = request.POST['aid_type']
            aadhaar = request.POST['benef_adhaar_no']
            udid = request.POST['str_udid_cardno']
            mobile = request.POST['str_mobile_no']
            imparement = request.POST['num_disability_type']
            imparement_per = request.POST['num_disability_persentage']
            imparement_certificate = request.FILES['disability_certificate']
            income_certificate = request.FILES['income_certificate']
            photo = request.FILES['files']
            

            context['name'] = request.POST['str_fname'] + ' ' +  request.POST['str_mname'] + ' ' + request.POST['str_lname']
            context['father_name'] = request.POST['benef_father_name']
            context['mother_name'] = request.POST['benef_mother_name']
            context['dob'] = request.POST['dt_dob']
            context['category'] = request.POST['num_category_id']
            context['address'] = request.POST['str_houseNo'] + ', ' + request.POST['str_Street'] + ', ' + request.POST['Str_Area'] + ', ' + request.POST['str_tehsil'] + ', ' + request.POST['num_pincode']
            context['aadhaar'] = request.POST['benef_adhaar_no']
            context['udid'] = request.POST['str_udid_cardno']
            context['mobile'] = request.POST['str_mobile_no']
            context['impairement'] = request.POST['num_disability_type']
            context['impairement_per'] = request.POST['num_disability_persentage']

            # print (context)
            beneficiary = BeneficiaryDetails.objects.create(
                udid=udid, aadhaar=aadhaar, mobile=mobile, first_name=first_name,
                middle_name=middle_name, last_name=last_name, father_name=father_name, mother_name=mother_name,
                imparement=imparement, imparement_per=imparement_per, dob=dob,
                salutation=salutation, gender=gender, age=age, category=category,
                address=address, pincode=pin_code, occupation=occupation,
                income=0, assistive_device='Cochlear Implants',
                imparement_certificate=imparement_certificate, 
                income_certificate=income_certificate, photo=photo
            )
            # print("********\n", beneficiary)
            beneficiary.save()

            return render(request, 'index.html', {'context':context})
        except:
            return render(request, 'index.html')

    return render(request, 'index.html')

def change_status(request):
    accepted = request.POST.get('accepted', None)
    comments= request.POST.get('comment', None)
    udid = request.POST.get('udid', None)
    username = request.POST.get('username', None)
    print("^^^^^^^^^")
    print(accepted, comments, udid, username)

    if not comments:
        ben = BeneficiaryDetails.objects.filter(udid=udid).update(verification_status='2')
    else:
        BeneficiaryDetails.objects.filter(udid=udid).update(comments=comments, verification_status='3')

    agency = AgencyDetails.objects.filter(username=username)
    password = agency[0].password
    return agency_index(request, username=username, password=password)
    # return redirect(agency_index)
    # return redirect(reverse(agency_index, kwargs={'username':username, 'password':password}))

def schemes(request):
    return render(request, 'table.html')

def equipment(request):
    return render(request, 'getEquipmentInfo.html')

def feedback(request):
    return render(request, 'get_feedback_form.html')

def reg_status(request):
    return render(request, 'get_beneficiary_registration_status.html')

def dis_info(request):
    return render(request, 'getDisabilityInfo.html')

def national_institutes(request):
    return render(request, 'getnational_institutes.html')

def checklist(request):
    return render(request, 'checklist.html')

def downloads(request):
    return render(request, 'downloadPage1.html')