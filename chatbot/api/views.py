# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot.models import UserSession
from django.contrib.auth.models import User
import json
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import json

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def get_session(self, user):
        try:
            session = UserSession.objects.get(user=user)
        except UserSession.DoesNotExist:
            # Create a new session if one doesn't exist
            session = UserSession.objects.create(user=user, current_step='start', state=json.dumps({}))
        return session
    
    def get(self, request, *args, **kwargs):
        user = request.user
        session = self.get_session(user)
        
        # Define the chatbot configuration
        chatbot_config = {
            "start": {
                "message": "Do you wish to buy a new car or a used car?",
                "options": [
                    {"label": "New", "value": "new", "next": "new"},
                    {"label": "Used", "value": "used", "next": "used"}
                ]
            },
            "new": {
                "message": "Enter the Year, Make, Model and Trim",
                "next": "tradeIn"
            },
            "used": {
                "message": "Enter the VIN Number",
                "next": "verifyVIN"
            },
            "verifyVIN": {
                "message": "Is the VIN correct?",
                "options": [
                    {"label": "Yes", "value": "tradeIn", "next": "tradeIn"},
                    {"label": "No", "value": "used", "next": "used"}
                ]
            },
            "tradeIn": {
                "message": "Do you have a car to trade in?",
                "options": [
                    {"label": "Yes", "value": "tradeInDetails", "next": "tradeInDetails"},
                    {"label": "No", "value": "dealerOffer", "next": "dealerOffer"}
                ]
            },
            "tradeInDetails": {
                "message": "Enter the VIN of the car to be traded in",
                "next": "mileage"
            },
            "mileage": {
                "message": "Enter the Mileage of the car",
                "next": "zipCode"
            },
            "zipCode": {
                "message": "Enter your zip code",
                "next": "scratchesDents"
            },
            "scratchesDents": {
                "message": "Are there any scratches or dents in front of the car?",
                "options": [
                    {"label": "Yes", "value": "chooseArea", "next": "chooseArea"},
                    {"label": "No", "value": "driverSideDents", "next": "driverSideDents"}
                ]
            },
            "driverSideDents": {
                "message": "Are there any scratches or dents on the driver side of the car?",
                "options": [
                    {"label": "Yes", "value": "chooseArea", "next": "chooseArea"},
                    {"label": "No", "value": "rearDents", "next": "rearDents"}
                ]
            },
            "rearDents": {
                "message": "Are there any scratches or dents in the rear of the car?",
                "options": [
                    {"label": "Yes", "value": "chooseArea", "next": "chooseArea"},
                    {"label": "No", "value": "passengerSideDents", "next": "passengerSideDents"}
                ]
            },
            "passengerSideDents": {
                "message": "Are there any scratches or dents on the passenger side of the car?",
                "options": [
                    {"label": "Yes", "value": "chooseArea", "next": "chooseArea"},
                    {"label": "No", "value": "windowsDents", "next": "windowsDents"}
                ]
            },
            "windowsDents": {
                "message": "Are there any scratches or dents on windows or lights of the car?",
                "options": [
                    {"label": "Yes", "value": "chooseArea", "next": "chooseArea"},
                    {"label": "No", "value": "dealerOffer", "next": "dealerOffer"}
                ]
            },
            "chooseArea": {
                "message": "Choose areas of the car scratched, dinged or dented",
                "next": "dealerOffer"
            },
            "dealerOffer": {
                "message": "Enter the offer given by the dealer",
                "next": "calculatePrice"
            },
            "calculatePrice": {
                "message": "Using formula to calculate price",
                "next": "quoteTeaser"
            },
            "quoteTeaser": {
                "message": "Redirecting to quote teaser page",
                "next": "paymentGateway"
            },
            "paymentGateway": {
                "message": "Redirecting to payment gateway",
                "next": "paymentConfirmation"
            },
            "paymentConfirmation": {
                "message": "Providing report PDF on payment confirmation"
            },
            "end": {
                "message": "Thank you for using the chatbot",
                "options": [
                    {"label": "Start again", "value": "start", "next": "start"}
                ]
            }
        }
        
        # Prepare the response data
        response_data = {
            "chatbot_config": chatbot_config,
            "session": {
                "current_step": session.current_step,
                "state": session.state,
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)




# from .models import UserSession, Account

class UpdateChatbotSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get_session(self, user):
        try:
            session = UserSession.objects.get(user=user)
        except UserSession.DoesNotExist:
            session = UserSession.objects.create(user=user, current_step='start', state=json.dumps({}))
        return session

    def post(self, request, *args, **kwargs):
        user = request.user
        session = self.get_session(user)
        
        # Extract message and next from the request data
        message = request.data.get('message')
        next_step = request.data.get('next')
        previous_state = request.data.get('previous_state')
        response = request.data.get('response')
        data = request.data.get('data')

        current_step = session.current_step
        questions_and_answers = request.data.get('process_data')
        print(questions_and_answers)
        # questions_and_answers = session.questions_and_answers
        
        # # Save the question and answer
        # questions_and_answers[previous_state] = {
        #     'question': message,
        #     'answer': response
        # }
        session.current_step = next_step
        session.state = data
        session.questions_and_answers = questions_and_answers
        session.save()

        # # Update the session current step
        # session.current_step = next_step
        # session.state = json.dumps(state)
        # session.save()

        response_data = {
            'message': "data saved succesfully",
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
class ResetChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def get_session(self, user):
        try:
            session = UserSession.objects.get(user=user)
        except UserSession.DoesNotExist:
            session = UserSession.objects.create(user=user, current_step='start', state=json.dumps({}))
        return session

    def post(self, request, *args, **kwargs):
        user = request.user
        session = self.get_session(user)
        
        # Extract message and next from the request data
        session.current_step = "start"
        session.state = {}
        session.questions_and_answers = {}
        session.save()


        response_data = {
            'message': "Chatbot Reset Successfully",
        }

        return Response(response_data, status=status.HTTP_200_OK)



