from django.urls import path
from base import views

urlpatterns = [
    path('', views.dashboard, name='dashboard-url'),
    path("stage/edit/", views.stage_edit, name="stage-edit-url"),
    path("member/signup/", views.member_add, name="member-add-url"),
    path("member/edit/<pk>", views.member_edit, name="member-edit-url"),
    path("member/profile/view/<pk>", views.member_view, name="member-url"),

    path("emerg/contacts", views.emergency_contacts, name="emergency-contacts-url"),
    path("emerg/contact/rm/<pk>", views.emergency_contact_remove, name="emergency-contact-rm-url"),
    path("emerg/contact/add", views.emergency_contact_add, name="emergency-contact-add-url"),
    path("emergencies/received/", views.emergencies, name="emergencies-url"),
    path("emergencies/read/<pk>", views.emergency_read, name="emergency-read-url"),
    path("emergencies/view/<pk>", views.emergency_view, name="emergency-view-url"),
    path("map/view/<pk>", views.map_view, name="map-view-url"),

    path("usr/signup/", views.sign_up, name="sign-up-url"),
    path("usr/sign_in/", views.sign_in, name="sign-in-url"),
    path("usr/sign-out/", views.sign_out, name="sign-out-url"),
    path("usr/edit/", views.user_edit, name="user-edit-url"),
    path("usr/profile/", views.my_profile, name="profile-url"),
    # path("pwd/reset/", views.password_reset, name="pwd-reset-url"),
    # path("pwd/change/", views.password_change, name="pwd-change-url"),
]
