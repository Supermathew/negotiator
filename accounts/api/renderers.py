from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {}
        status_code = renderer_context['response'].status_code if renderer_context else 200
        print(status_code)
        if status_code >= 400:
            message = ''
            if 'non_field_errors' in data:
                message += ' '.join(data.pop('non_field_errors'))
            else:
                for key, value in data.items():
                    if isinstance(value, list):
                        # Check if the list contains dict items
                        if all(isinstance(item, dict) for item in value):
                            for item in value:
                                for sub_key, sub_value in item.items():
                                    message += f"{key} -> {sub_key}: {sub_value} "
                        else:
                            message += f"{key}: {', '.join(value)} "
                    elif isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            message += f"{key} -> {sub_key}: {sub_value} "
                    else:
                        message += f"{key}: {value} "
            response = {
                'status': 'failure',
                'message': message.strip()
            }
        else:
            if 'message' in data:
                response = {
                    'status': 'success',
                    'message': data['message'],
                }
                if 'refresh' in data:
                    response['refresh'] = data['refresh']
                if 'access' in data:
                    response['access'] = data['access']
            else:
                response = {
                    'status': 'success',
                    'message': data
                }

        return json.dumps(response)
