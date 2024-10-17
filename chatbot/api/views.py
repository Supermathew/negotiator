# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot.models import UserSession,Car
from django.contrib.auth.models import User
import json
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from chatbot.api.serializers import CarSerializer

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
                "message": "Enter the Manufacturer of the car.",
                "next": "enter_model"
            },  ## validation done
            "enter_model": {
                "message": "Enter the Model of the car.",
                "next": "enter_year",
            },
            "enter_year": {
                "message": "Enter the Year of the car.",
                "next": "enter_trim"
            },
            "enter_trim": {
                "message": "Enter the Trim of the car.",
                "next": "enter_color"
            },
            "enter_color": {
                "message": "Enter the Color of the car.",
                "next": "tradeIn",
                "validation": True
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
        
        # chatbot_config = {
        #     "start": {
        #         "message": "Are you buying a new car or a used car?",
        #         "options": [
        #             {"label": "New", "value": "new", "next": "new_car"},
        #             {"label": "Used", "value": "used", "next": "enter_vin_used_Car"}
        #         ]
        #     },
        #     "new_car": {
        #         "message": "Enter the Manufacturer of the car.",
        #         "next": "enter_model"
        #     },  ## validation done
        #     "enter_model": {
        #         "message": "Enter the Model of the car.",
        #         "next": "enter_year",
        #     },
        #     "enter_year": {
        #         "message": "Enter the Year of the car.",
        #         "next": "enter_trim"
        #     },
        #     "enter_trim": {
        #         "message": "Enter the Trim of the car.",
        #         "next": "enter_color"
        #     },
        #     "enter_color": {
        #         "message": "Enter the Color of the car.",
        #         "next": "trade_in_check",
        #         "validation": True
        #     },
        #     "trade_in_check": {
        #         "message": "Do you have a car to trade-in?",
        #         "options": [
        #             {
        #             "label": "Yes",
        #             "value": "trade_in",
        #             "next":"enter_vin_new_Car"
        #             },
        #             {
        #             "label": "No",
        #             "value": "final_calculation"
        #             }
        #         ]
        #     },
        #     "enter_vin_used_Car": {
        #         "message": "Enter the VIN number of the vehicle.",
        #         "next": "damage_report"
        #     },
        #     # "enter_vin_new_Car": {
        #     #     "message": "Let's get some details about the used car you want to buy.",
        #     #     "next": "enter_vin"
        #     # },
        #     "enter_vin_new_Car": {
        #         "message": "Enter the VIN number of the vehicle.",
        #         "next": "damage_report"
        #     },
        #     "damage_report": {
        #         "message": "Please specify any damage to the vehicle.",
        #         "next": "enter_trade_in"
        #     },
        #     "enter_trade_in": {
        #         "message": "Do you have a car to trade-in?",
        #         "options": [
        #             {
        #             "label": "Yes",
        #             "value": "enter_trade_in_vin"
        #             },
        #             {
        #             "label": "No",
        #             "value": "final_calculation"
        #             }
        #         ]
        #     },
        #     "enter_trade_in_vin": {
        #         "message": "Enter the VIN number of the trade-in vehicle.",
        #         "next": "enter_zipcode"
        #     },
        #     "enter_zipcode": {
        #         "message": "Enter the zipcode of the trade-in vehicle.",
        #         "next": "enter_mileage"
        #     },
        #     "enter_mileage": {
        #         "message": "Enter the mileage of the trade-in vehicle.",
        #         "next": "condition_report"
        #     },
        #     "condition_report": {
        #         "message": "Please specify any damage to the trade-in vehicle.",
        #         "next": "final_calculation"
        #     },
        #     "final_calculation": {
        #        "message": "We are calculating the best price for your car.",
        #        "next": "payment"
        #     },
        #     "payment": {
        #        "message": "Proceeding to payment.",
        #        "next": "payment_confirmation"
        #     },
        #     "payment_confirmation": {
        #        "message": "Payment confirmation and quote will be sent to your email.",
        #        "next": "end"
        #     },
        #     "end": {
        #       "message": "Thank you for using Negotigator! If you need further assistance, please contact support."
        #     }
        # }
        
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
        if next_step != "":
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
    

def validate_vehicle_combination(make, year, model, trim, color):
    try:
        combination = Car.objects.get(make=make, year=year, model=model, trim=trim, color=color)
        return combination
    except Car.DoesNotExist:
        return None

    

from django.db.models import Q

def suggest_vehicle_combinations(make=None, year=None, model=None, trim=None, color=None, search_term=None):
    # Create a base query
    query = Car.objects.all()
    
    if make:
        query = query.filter(make__icontains=make)
    if model:
        query = query.filter(model__icontains=model)
    if trim:
        query = query.filter(trim__icontains=trim)
    if color:
        query = query.filter(color__icontains=color)

    return query.distinct()



def handle_user_input(make, year, model, trim, color):
    valid_combination = validate_vehicle_combination(make, year, model, trim, color)
    
    if valid_combination:
        response = {
            "status": "success",
            "message": "Your vehicle combination exists.",
            "data": CarSerializer(valid_combination).data
        }
    else:
        suggested_combinations = suggest_vehicle_combinations(make, year, model, trim, color)
        
        if suggested_combinations.exists():
            response = {
                "status": "success",
                "message": "The exact combination does not exist, but here are some similar options:",
                "data": CarSerializer(suggested_combinations, many=True).data  # Serialize the queryset
            }
        else:
            response = {
                "status": "failure",
                "message": "No similar vehicle combinations found."
            }
    
    return Response(response)



class CheckCarModelView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        make = request.data.get('make')
        year = request.data.get('year')
        model = request.data.get('model')
        trim = request.data.get('trim')
        color = request.data.get('color')
        
        return handle_user_input(make, year, model, trim, color)