from django.urls import path
from chatbot.api.views import ChatbotView,UpdateChatbotSessionView,ResetChatbotView,CheckCarModelView

urlpatterns = [
    # path('', ChatbotView.as_view(), name='chatbot'),
    path('questions-answers/', ChatbotView.as_view(), name='chatbot-questions-answers'),
    path('sessionup/', UpdateChatbotSessionView.as_view(), name='chatbot-questions-answers'),
    path('reset/', ResetChatbotView.as_view(), name='Reset-Chatbot'),
    path('check-car-model/', CheckCarModelView.as_view(), name='check_car_model'),
]
