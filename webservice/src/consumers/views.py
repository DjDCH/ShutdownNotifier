from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from consumers.models import Consumer
from consumers.serializers import ConsumerSerializer, EmailSerializer, EmailValidationSerializer, PhoneSerializer, \
    PhoneValidationSerializer
from consumers.utils import Generator


class ConsumerDetail(APIView):
    """
    Retrieve a consumer instance.

    Require an authentication token.

    Throw a HTTP 404 if not found.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, user):
        try:
            return Consumer.objects.get(user=user)
        except Consumer.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        consumer = self.get_object(request.user)
        serializer = ConsumerSerializer(consumer)
        return Response(serializer.data)


class ConsumerEmail(APIView):
    """
    Create a new consumer (and matching user) or generate a new email validation code.

    Return the given email address.
    """
    def post(self, request, format=None):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: Ensure email domain is valid
            consumer, c_created = Consumer.objects.get_or_create(email=serializer.validated_data['email'])

            code = Generator.generate_code()
            consumer.email_validation_code = code
            consumer.save()

            if c_created:
                username = Generator.generate_username()
                user = User.objects.create_user(username)
                user.is_active = False
                user.save()
                consumer.user = user
                consumer.save()

            # TODO: Send validation code by email

            if c_created:
                return Response({'validate': request.build_absolute_uri('/consumer/email/validate/')},
                                status=status.HTTP_201_CREATED)

            return Response({'validate': request.build_absolute_uri('/consumer/email/validate/')})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumerEmailValidate(APIView):
    """
    Validate an email validation code.

    Return an authentication token if successful.
    """
    def get_object(self, email):
        try:
            return Consumer.objects.get(email=email)
        except Consumer.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = EmailValidationSerializer(data=request.data)
        if serializer.is_valid():
            consumer = self.get_object(serializer.validated_data['email'])

            if consumer.email_validation_code == serializer.validated_data['code']:
                consumer.email_validation_code = ''
                consumer.save()
                user = consumer.user
                user.is_active = True
                user.save()
                token, created = Token.objects.get_or_create(user=consumer.user)
                return Response({'token': token.key, 'phone': request.build_absolute_uri('/consumer/phone/')})

            return Response({'code': ['Code does not match.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumerPhone(APIView):
    """
    Update a consumer instance and generate a new phone validation code.

    Require an authentication token.

    Return the given phone number.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, user):
        try:
            return Consumer.objects.get(user=user)
        except Consumer.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: Ensure phone number is valid
            consumer = self.get_object(request.user)

            code = Generator.generate_code()
            consumer.phone_validation_code = code
            consumer.phone = serializer.validated_data['phone']
            consumer.save()

            # TODO: Send validation code by SMS

            return Response({'validate': request.build_absolute_uri('/consumer/phone/validate/')})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ConsumerPhoneValidate(APIView):
    """
    Validate an email validation code.

    Require an authentication token.

    Return an authentication token if successful.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, user):
        try:
            return Consumer.objects.get(user=user)
        except Consumer.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = PhoneValidationSerializer(data=request.data)
        if serializer.is_valid():
            consumer = self.get_object(request.user)

            if consumer.phone_validation_code == serializer.validated_data['code']:
                consumer.phone_validation_code = ''
                consumer.is_valid = True
                consumer.save()
                return Response({'notify': request.build_absolute_uri('/consumer/notify')})

            return Response({'code': ['Code does not match.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumerNotify(APIView):
    """
    Notify a consumer.

    Require an authentication token.

    Throw a HTTP 404 if not found.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, user):
        try:
            return Consumer.objects.get(user=user)
        except Consumer.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        consumer = self.get_object(request.user)

        if consumer.is_valid:
            # TODO: Send SMS notification
            serializer = ConsumerSerializer(consumer)
            return Response(serializer.data)

        return Response({'phone': ['Phone is missing or not validated.']}, status=status.HTTP_400_BAD_REQUEST)

