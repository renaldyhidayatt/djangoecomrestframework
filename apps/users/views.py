from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterationSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializers_class = RegisterationSerializer

    def post(self, request):
        context = {"request": request}
        serialized = self.serializers_class(data=request.data, context=context)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        data = {"success": True}
        data.update(serialized.data)

        return Response(data=data, status=status.HTTP_201_CREATED)
