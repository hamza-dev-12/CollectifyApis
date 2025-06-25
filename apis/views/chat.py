import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from ..models import Group
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat(request, group_id):
    try:
        query = request.data.get("query")
        month = request.data.get("month")
        year = request.data.get("year")

        if not query or not month or not year:
            raise ValueError("Please provide query and month")

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

        prompt = f"""
        You will be given some context from database and basis on that respond to the user query. If the context is empty just respond with meaningful messsage.
        This database holds the information who have paid the mantainance and who has not in the group. So you are like Analytic agent for this admin.
        Context:
        f{str(result)}

        User Query: {query}

        Note: Please responsd with natural language with no special character and make it readable. And respond like you only know the query dont tell the user that you have any context
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return JsonResponse(status=200, data={"message": response.text})

    except Exception as e:
        return JsonResponse(status=400, data={"error": str(e)})
