from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (UserSerializer, PricingSerializer, ContactSerializer,
                          PasswordResetTokenSerializer,FootballTeamSerializer,
                          StaffUserSerializer, PlayerDetailSerializer, FAQSerializer)
from django.http import Http404
from .models import (CustomUser, Pricing, Contact, PasswordResetToken,FootballTeam,
                     PlayerDetail, FAQ)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid
from django.utils import timezone

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate both access and refresh tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)


class PricingListAPIView(APIView):
    def get(self, request):
        pricings = Pricing.objects.all()
        serializer = PricingSerializer(pricings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContactListCreateAPIView(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = self.get_object(pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListCreateAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




def generate_unique_token():
    return str(uuid.uuid4())

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                token = str(uuid.uuid4())  # Generate a unique token
                expiration_time = timezone.now() + timezone.timedelta(hours=1)  # Example: Token expires in 1 hour
                PasswordResetToken.objects.create(user=user, token=token, expires_at=expiration_time)
                # send_reset_password_email(email, token)
                return Response({'message': 'Password reset email sent.', 'email': email, 'token': token}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Email field is required.'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        if token and password:
            try:
                reset_token = PasswordResetToken.objects.get(token=token, expires_at__gt=timezone.now())
                user = reset_token.user
                user.set_password(password)
                user.save()
                reset_token.delete()
                return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
            except PasswordResetToken.DoesNotExist:
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Token and password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)


class FootballTeamCreateAPIView(APIView):
    def post(self, request):
        serializer = FootballTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        teams = FootballTeam.objects.all()
        serializer = FootballTeamSerializer(teams, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        team = FootballTeam.objects.get(pk=pk)
        serializer = FootballTeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        team = FootballTeam.objects.get(pk=pk)
        serializer = FootballTeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        team = FootballTeam.objects.get(pk=pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class StaffUserListAPIView(APIView):
    def get(self, request):
        staff_users = CustomUser.objects.filter(is_staff=True)
        serializer = StaffUserSerializer(staff_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        staff_user = CustomUser.objects.get(pk=pk)
        serializer = StaffUserSerializer(staff_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        staff_user = CustomUser.objects.get(pk=pk)
        serializer = StaffUserSerializer(staff_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        staff_user = CustomUser.objects.get(pk=pk)
        staff_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlayerDetailAPIView(APIView):
    def get(self, request):
        players = PlayerDetail.objects.all()
        serializer = PlayerDetailSerializer(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        player = PlayerDetail.objects.get(pk=pk)
        serializer = PlayerDetailSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        player = PlayerDetail.objects.get(pk=pk)
        serializer = PlayerDetailSerializer(player, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        player = PlayerDetail.objects.get(pk=pk)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FAQList(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FAQDetail(APIView):
    def get_object(self, pk):
        try:
            return FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        faq = self.get_object(pk)
        serializer = FAQSerializer(faq)
        return Response(serializer.data)

    def put(self, request, pk):
        faq = self.get_object(pk)
        serializer = FAQSerializer(faq, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        faq = self.get_object(pk)
        faq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)