from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from .serializers import AuthenticationSerializer, SignupSerializer
from .models import User
from users.api_exception import GenericException, UserActiveException, UserFeatureException, success_response, standard_response
from rest_framework.response import Response

class Signup(ViewSet):
    def create(self, request):
        try:
            data = request.data.copy()
            signup_serializer = SignupSerializer(data=data, context={'request': request})
            signup_serializer.is_valid(raise_exception=True)
            signup_serializer.save()
            return success_response(message='Success')
        except GenericException as e:
            return Response(e.detail, status=e.status_code)
        except Exception as e:
            raise GenericException(error_message=str(e), status_code=500)


class Login(ViewSet):
    serializer_class = AuthenticationSerializer

    def create(self, request):
        try:
            data = request.data.copy()

            # Check if the user exists
            user_ins = User.objects.filter(email=data['email']).first()
            if not user_ins:
                raise GenericException(error_message='User Account is not available', status=400)

            # Validate user credentials
            login_serializer = AuthenticationSerializer(data=data, context={'request': request})
            login_serializer.is_valid(raise_exception=True)

            user = login_serializer.validated_data['user']

            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return standard_response(
                data={
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'email': user.email,
                    'name': user.name,
                },
                message="Valid user, new tokens generated",
                status_num=200
            )
        except GenericException as e:
            return Response(e.detail, status=e.status_code)
        except Exception as e:
            raise GenericException(error_message=str(e), status_code=500)


class Logout(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            access_token = request.auth

            if not refresh_token or not access_token:
                raise GenericException(error_message="Refresh token and access token are required", status=400)

            # Blacklist the refresh token
            refresh_token_instance = RefreshToken(refresh_token)
            refresh_token_instance.blacklist()

            # Optionally, remove all outstanding tokens for the user
            OutstandingToken.objects.filter(user=request.user).delete()

            return standard_response(message="OK, goodbye", status_num=200)
        except GenericException as e:
            return Response(e.detail, status=e.status_code)
        except Exception as e:
            raise GenericException(error_message=str(e), status_code=500)


class Profile(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        try:
            user_ins = User.objects.get(email=request.user.email)

            profile_data = {
                "user_basic_info": {
                    "name": user_ins.name,
                    "email": user_ins.email,
                }
            }

            return standard_response(
                data=profile_data,
                message="User profile fetched successfully",
                status_num=200
            )
        except User.DoesNotExist:
            raise GenericException(error_message="User does not exist", status=404)
        except Exception as e:
            raise GenericException(error_message=str(e), status_code=500)
