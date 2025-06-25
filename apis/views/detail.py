from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from ..models import User, Group
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

"""
select_realted --> forward --> one-to-one
prefetch_related --> reverse --> many-to-many
"""


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_groups_data(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        month = request.GET.get("month")
        year = request.GET.get("year")

        if not month or not year:
            raise ValueError("Please provide month and year in query")

        filter_date = {"date__month": int(month), "date__year": int(year)}

        result = {
            "user_id": user_id,
            "username": user.username,
            "email": user.email,
            "groups": [],
        }

        groups = Group.objects.filter(admin=user).prefetch_related(
            "group", "group__group_members"
        )

        for group in groups:
            members = group.group.all()

            group_data = {
                "id": group.id,
                "group_name": group.group_name,
                "base_amount": group.base_amount,
                "members": [],
            }

            for member in members:
                payments = member.group_members.filter(**filter_date)

                member_data = {
                    "group_member_id": member.id,
                    "email": member.email,
                    "name": member.member_name,
                    "status": "paid" if len(payments) > 0 else "pending",
                    "payments": [
                        {
                            "payment_id": payment.id,
                            "date": payment.date,
                            "status": payment.status,
                            "amount": payment.amount,
                        }
                        for payment in payments
                    ],
                }

                group_data["members"].append(member_data)

            result["groups"].append(group_data)

        return JsonResponse(data=result, status=200)

    except Exception as e:
        return JsonResponse({"status": 500, "error": str(e)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_group_detail_by_id(request, group_id):
    try:
        group = Group.objects.prefetch_related("group", "group__group_members").get(
            pk=group_id
        )
        result = {
            "group_id": group_id,
            "group_name": group.group_name,
            "base_amount": group.base_amount,
            "members": [],
        }
        members = group.group.all()
        month = request.GET.get("month")
        year = request.GET.get("year")

        if not month:
            raise ValueError("Please provide month in the query")
        if not year:
            raise ValueError("Please provide year in the query")

        month_filter = {"date__month": int(month), "date__year": int(year)}

        for member in members:
            payment = member.group_members.filter(**month_filter).first()
            result["members"].append(
                {
                    "group_member_id": member.id,
                    "email": member.email,
                    "name": member.member_name,
                    "status": "paid" if payment else "pending",
                    "payment": {
                        "payment_id": payment.id,
                        "date": payment.date,
                        "status": payment.status,
                        "amount": payment.amount,
                    }
                    if payment
                    else None,
                }
            )

        return JsonResponse(status=200, data=result)

    except Exception as e:
        return JsonResponse(status=500, data={"message": str(e)})


"""
# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Group, Member, Payment

# Option 1: Using Django REST Framework (Recommended)
@api_view(['GET'])
def get_user_groups_data(request, user_id):

    Get all groups, members, and payments for a specific user

    try:
        user = get_object_or_404(User, id=user_id)
        
        # Get all groups where user is admin with related data
        groups = Group.objects.filter(admin=user).select_related('admin').prefetch_related(
            'group',              # Fetch all members for these groups
            'group__group_members'  # Fetch all payments for these members
        )
        
        result = {
            'user_id': user.id,
            'username': user.username,
            'groups': []
        }
        
        for group in groups:
            # Get all members for this group with their payments
            members = Member.objects.filter(group=group).prefetch_related('group_members')
            
            group_data = {
                'group_id': group.id,
                'group_name': group.group_name,
                'admin': {
                    'id': group.admin.id,
                    'username': group.admin.username
                },
                'members': []
            }
            
            for member in members:
                # Get all payments for this member
                payments = Payment.objects.filter(group_members=member).order_by('-date')
                
                member_data = {
                    'member_id': member.id,
                    'member_name': member.member_name,
                    'email': member.email,
                    'payments': [
                        {
                            'payment_id': payment.id,
                            'status': payment.status,
                            'date': payment.date,
                            'amount': payment.amount
                        }
                        for payment in payments
                    ]
                }
                group_data['members'].append(member_data)
            
            result['groups'].append(group_data)
        
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Option 2: Using Django's built-in JsonResponse (Alternative)
def get_user_groups_data_json(request, user_id):
    Alternative implementation using JsonResponse

    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        # More efficient query using select_related and prefetch_related
        groups = Group.objects.filter(admin=user).select_related('admin').prefetch_related(
            'group',  # This is the related_name for members
            'group__group_members'  # This prefetches payments for each member
        )
        
        result = []
        for group in groups:
            group_data = {
                'group_id': group.id,
                'group_name': group.group_name,
                'admin_username': group.admin.username,
                'members': []
            }
            
            for member in group.group.all():  # Using the related_name 'group'
                payments_data = [
                    {
                        'payment_id': payment.id,
                        'status': payment.status,
                        'date': payment.date.isoformat(),
                        'amount': payment.amount
                    }
                    for payment in member.group_members.all().order_by('-date')
                ]
                
                member_data = {
                    'member_id': member.id,
                    'member_name': member.member_name,
                    'email': member.email,
                    'total_payments': len(payments_data),
                    'payments': payments_data
                }
                group_data['members'].append(member_data)
            
            result.append(group_data)
        
        return JsonResponse({
            'user_id': user_id,
            'username': user.username,
            'total_groups': len(result),
            'groups': result
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Option 3: Optimized version with aggregation
from django.db.models import Count, Sum, Prefetch

@api_view(['GET'])
def get_user_groups_summary(request, user_id):
    Optimized version with summary statistics

    user = get_object_or_404(User, id=user_id)
    
    # Create a custom prefetch for payments ordered by date
    payments_prefetch = Prefetch(
        'group_members',
        queryset=Payment.objects.select_related().order_by('-date')
    )
    
    # Fetch groups with all related data in one go
    groups = Group.objects.filter(admin=user).prefetch_related(
        Prefetch('group', queryset=Member.objects.prefetch_related(payments_prefetch))
    ).annotate(
        member_count=Count('group'),
        total_payments=Count('group__group_members')
    )
    
    result = {
        'user_id': user.id,
        'username': user.username,
        'groups': []
    }
    
    for group in groups:
        group_data = {
            'group_id': group.id,
            'group_name': group.group_name,
            'member_count': group.member_count,
            'total_payments': group.total_payments,
            'members': []
        }
        
        for member in group.group.all():
            payments = member.group_members.all()
            total_amount = sum(p.amount for p in payments)
            
            member_data = {
                'member_id': member.id,
                'member_name': member.member_name,
                'email': member.email,
                'payment_count': len(payments),
                'total_amount': total_amount,
                'recent_payments': [
                    {
                        'payment_id': p.id,
                        'status': p.status,
                        'date': p.date,
                        'amount': p.amount
                    }
                    for p in payments[:5]  # Last 5 payments
                ]
            }
            group_data['members'].append(member_data)
        
        result['groups'].append(group_data)
    
    return Response(result)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/users/<int:user_id>/groups/', views.get_user_groups_data, name='user-groups-data'),
    path('api/users/<int:user_id>/groups-json/', views.get_user_groups_data_json, name='user-groups-json'),
    path('api/users/<int:user_id>/groups-summary/', views.get_user_groups_summary, name='user-groups-summary'),
]
"""
