import jwt
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, \
    HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from credentials import SECRET_KEY, ALGO
from authentications import AuthAPIView
from .constants import collections, LOGIN_TOKEN_EXPIRE_TIMEOUT
from authentications import AuthAPIView
from .controllers import get_user_by_mobile, create_user, get_user_by_mobile_and_password, \
    get_all_todo, create_new_todo, update_todo
from todob.settings import DB

todos_collection = DB[collections.get("todos")]


class Register(APIView):
    def post(self, request):
        requested_data = request.data
        full_name = requested_data.get("full_name")
        mobile = requested_data.get("mobile")
        password = requested_data.get("password")

        if not full_name or not mobile or not password:
            response = "Please fill in all of the fields."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        existing_user = get_user_by_mobile(mobile)

        # check if user already exit with give mobile number
        if existing_user:
            response = "The mobile number is already being used."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        # create a brand-new user
        user = create_user(full_name, mobile, password)
        return Response(data=user, status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request):
        requested_data = request.data
        mobile = requested_data.get("mobile")
        password = requested_data.get("password")
        user = get_user_by_mobile_and_password(mobile, password)

        if not user:
            response = "Your mobile and password combination does not match an account."
            return Response(data=response, status=HTTP_400_BAD_REQUEST)

        if user:
            payload = user
            token = jwt.encode(payload, SECRET_KEY, ALGO, {"expires_in": LOGIN_TOKEN_EXPIRE_TIMEOUT})
            data = {
                "user": user,
                "token": token
            }
            return Response(data=data, status=HTTP_200_OK)


class TodoList(AuthAPIView):
    """
    List all todos, or create a new todo.
    """
    def get(self, request, format=None):
        user_id = request.user.get("user_id")
        todos = get_all_todo(user_id)
        return Response(data=todos, status=HTTP_200_OK)

    def post(self, request, format=None):
        requested_data = request.data
        user_id = request.user.get("user_id")
        body = requested_data.get("body")
        todo = create_new_todo(user_id, body)
        return Response(data=todo, status=HTTP_201_CREATED)


class TodoDetail(AuthAPIView):
    """
    Retrieve, update or delete a todo instance.
    """

    def get(self, request, id, format=None):
        user_id = request.user.get("user_id")
        todo = todos_collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})
        if todo is not None:
            return Response(data=todo, status=HTTP_200_OK)
        else:
            response = "No TODO found"
            return Response(data=response, status=HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        user_id = request.user.get("user_id")
        todo = todos_collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})
        requested_data = request.data
        body = requested_data.get("body")
        if not todo:
            response = "No TODO found to update"
            return Response(data=response, status=HTTP_404_NOT_FOUND)
        todo = update_todo(id, user_id, body)
        return Response(data=todo, status=HTTP_201_CREATED)

    def delete(self, request, id, format=None):
        user_id = request.user.get("user_id")
        todo = todos_collection.find_one({"id": id, "user_id": user_id}, {"_id": 0})
        if todo is not None:
            todos_collection.delete_one({"id": id, "user_id": user_id})
            response = "TODO deleted successfully"
            return Response(data=response, status=HTTP_204_NO_CONTENT)
        else:
            response = "No TODO found"
            return Response(data=response, status=HTTP_404_NOT_FOUND)








