from django.test import TestCase
from django.test import Client
import pytest

# Create your tests here.
from django.urls import reverse

from accounts.forms import CreateUserForm
from doctor_app.forms import CreatePatientForm, CreateAddressForm, AddAppointmentForm, CreateSpecialistForm, \
    CreateClinicForm
from doctor_app.models import Patient, Specialization, Specialist, Schedule, Appointment, Address, WEEK_DAY, Clinic, \
    Type


# Create your tests here.

@pytest.mark.django_db
def test_index():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_registration_get():
    client = Client()
    url = reverse('p_registration')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'],CreateUserForm)
    assert isinstance(response.context['model_form'], CreatePatientForm)
    assert isinstance(response.context['address_form'], CreateAddressForm)

@pytest.mark.django_db
def test_add_appointment_not_login():
    client = Client()
    url = reverse('add_appointment')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_add_appointment_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_appointment')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddAppointmentForm)

# @pytest.mark.django_db
# def test_add_appointment_post(user2, patient, clinic, specialist, type):
#     client = Client()
#     client.force_login(user2)
#     url = reverse('add_appointment')
#     date = {
#         'clinic': clinic.id,
#         'specialist': '1',
#         'a_date':'2022-3-28',
#         'a_time': '12:30',
#         'type': type.id,
#         'patient': user2.patient.id,
#     }
#     response = client.post(url, date)
#     assert response.status_code == 302
#     new_url = reverse('index')
#     assert response.url.startswith(new_url)
#     Appointment.objects.get(**date)

@pytest.mark.django_db
def test_CreateClinicView_not_login():
    client = Client()
    url = reverse('create_clinic')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_CreateClinicView_get_login(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_clinic')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['model_form'], CreateClinicForm)
    assert isinstance(response.context['address_form'], CreateAddressForm)



@pytest.mark.django_db
def test_CreateClinicView_post(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_clinic')
    data = {
        'name': 'Luxmed',
        'email': 'lm@p.pl',
        'phone_number':'55',
        'city': 'Poznań',
        'postcode':'60-476',
        'street':'Kaliska',
        'building_number':'55',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('list_clinics')
    assert response.url.startswith(new_url)
    Clinic.objects.get(name='Luxmed')


@pytest.mark.django_db
def test_CreateSpecialistView_not_login():
    client = Client()
    url = reverse('create_specialist')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_CreateSpecialistView_get_login(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_specialist')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], CreateUserForm)
    assert isinstance(response.context['model_form'], CreateSpecialistForm)
    assert isinstance(response.context['address_form'], CreateAddressForm)


@pytest.mark.django_db
def test_CreateSpecialistView_post(superuser, specialization):
    client = Client()
    client.force_login(superuser)
    url = reverse('create_specialist')
    data = {
        'username': 'gos',
        'password':'goog',
        'first_name':'gos',
        'last_name':'mic',
        'email':'gm@p.pl',
        'city': 'Poznań',
        'postcode':'60-476',
        'street':'Kaliska',
        'building_number':'55',
        'specialization': specialization.id,
        'phone_number':'55',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    # new_url = reverse('list_specialists')
    # assert response.url.startswith(new_url)
    # Specialist.objects.get(first_name='gos')


@pytest.mark.django_db
def test_CreateViewSchedule_not_login():
    client = Client()
    url = reverse('create_schedule')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_CreateViewSchedule_post(superuser,clinic, specialist):
    # bez superusera nie działa, list_schedules wymaga superusra
    client = Client()
    client.force_login(superuser)
    url = reverse('create_schedule')
    data = {
        'day_of_week': '1',
        'sch_from': '10:00',
        'sch_to': '15:00',
        'clinic': clinic.id,
        'specialist': specialist.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('list_schedules')
    assert response.url.startswith(new_url)
    Schedule.objects.get(**data)


@pytest.mark.django_db
def test_CreateViewType_get_not_login():
    client = Client()
    url = reverse('create_type')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_CreateViewType_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('create_type')
    date = {
        'name': 'Evrything',
    }
    response = client.post(url, date)
    assert response.status_code == 302
    new_url = reverse('list_types')
    assert response.url.startswith(new_url)
    Type.objects.get(**date)


@pytest.mark.django_db
def test_CreateViewSpecialization_not_login():
    client = Client()
    url = reverse('create_specialization')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_CreateViewSpecialization_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('create_specialization')
    date = {
        'name': 'Opto',
    }
    response = client.post(url, date)
    assert response.status_code == 302
    new_url = reverse('list_specializations')
    assert response.url.startswith(new_url)
    Specialization.objects.get(**date)

@pytest.mark.django_db
def test_ListViewSchedule_not_login():
    client = Client()
    url = reverse('list_schedules')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_ListViewSchedule_login(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('list_schedules')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0


@pytest.mark.django_db
def test_ListViewSchedule_login(superuser, schedules):
    client = Client()
    client.force_login(superuser)
    url = reverse('list_schedules')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(schedules)
    for sch in schedules:
        assert sch in response.context['object_list']


@pytest.mark.django_db
def test_ListViewPatient_not_login():
    client = Client()
    url = reverse('list_patients')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_ListViewPatient_login(superuser):
    client = Client()
    client.force_login(superuser)
    url = reverse('list_patients')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0

@pytest.mark.django_db
def test_ListViewPatient_login(superuser, patients):
    client = Client()
    client.force_login(superuser)
    url = reverse('list_patients')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(patients)
    for pat in patients:
        assert pat in response.context['object_list']


@pytest.mark.django_db
def test_ListViewClinic(clinics):
    client = Client()
    url = reverse('list_clinics')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(clinics)
    for clinic in clinics:
        assert clinic in response.context['object_list']


@pytest.mark.django_db
def test_ListViewspecialists(specialists):
    client = Client()
    url = reverse('list_specialists')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(specialists)
    for spec in specialists:
        assert spec in response.context['object_list']

@pytest.mark.django_db
def test_ListViewSpecialization_not_login():
    client = Client()
    url = reverse('list_specializations')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_ListViewSpecialization_login_without_perm(user2):
    client = Client()
    client.force_login(user2)
    url = reverse('list_specializations')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_ListViewSpecialization_login_with_perm(user):
    client = Client()
    client.force_login(user)
    url = reverse('list_specializations')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0


@pytest.mark.django_db
def test_ListViewType_not_login():
    client = Client()
    url = reverse('list_types')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_ListViewType_login_without_perm(user2):
    client = Client()
    client.force_login(user2)
    url = reverse('list_types')
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_ListViewType_login_with_perm(user):
    client = Client()
    client.force_login(user)
    url = reverse('list_types')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 0
#
# @pytest.mark.parametrize("index",list(range(10)))
# @pytest.mark.django_db
# def test_szczegoly_osoby( index, client, osoby, user):
#     client.force_login(user)
#     result = client.get(reverse("osoba", args=(osoby[index].id,)))
#     assert result.status_code == 200
#     assert result.context['object'].imie == osoby[index].imie
#     assert result.context['object'].nazwisko == osoby[index].nazwisko












