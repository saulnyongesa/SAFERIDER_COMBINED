from django.urls import path
from base2 import views
urlpatterns = [
    path('', views.dashboard, name='admin-dashboard-url'),
    path('search', views.search_item, name='admin-search-url'),

    path("stage/view/<pk>", views.stage_view, name="admin-stage-view-url"),
    path("stage/edit/<pk>", views.stage_edit, name="admin-stage-edit-url"),
    path("stage/add/", views.stage_add, name="admin-stage-add-url"),
    path("stage/admin/add/", views.stage_admin, name="admin-stage-admin-add-url"),

    path("stage/member/signup/<pk>", views.stage_member_add, name="admin-stage-member-add-url"),

    path("member/signup/", views.member_add, name="admin-member-add-url"),
    path("member/edit/<pk>", views.member_edit, name="admin-member-edit-url"),
    path("member/profile/view/<pk>", views.member_view, name="admin-member-url"),

    path("emerg/contact/rm/<pk>", views.emergency_contact_remove, name="admin-emergency-contact-rm-url"),
    path("emerg/contact/add/<pk>", views.emergency_contact_add, name="admin-emergency-contact-add-url"),
    path("sign_in/", views.sign_in, name="admin-sign-in-url"),
    path("sign-out/", views.sign_out, name="admin-sign-out-url"),
    path("edit/", views.user_edit, name="admin-user-edit-url"),
    path("profile/", views.my_profile, name="admin-profile-url"),
    # path("pwd/reset/", views.password_reset, name="pwd-reset-url"),
    # path("pwd/change/", views.password_change, name="pwd-change-url"),
]
