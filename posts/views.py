from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post


def api_response(status_code, message, data=None):
    return Response({
        "status": "success" if status_code < 400 else "error",
        "message": message,
        "data": data
    }, status=status_code)



@api_view(['POST'])
def signup_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return api_response(400, "Username aur password both compulsory")
    if User.objects.filter(username=username).exists():
        return api_response(400, "The username is already exist")
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return api_response(201, "User registered successfully", {"token": token.key, "username": user.username})

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return api_response(200, "Login successful", {"token": token.key, "username": user.username})
    return api_response(401, "Invalid credentials")


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def posts_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        data = [{
            "id": p.id, "title": p.title, "description": p.description,
            "amount": str(p.amount), "purpose": p.purpose, "user": p.user.username
        } for p in posts]
        return api_response(200, "Posts fetched successfully", data)

    elif request.method == 'POST':
        try:
            data = request.data
            post = Post.objects.create(
                user=request.user,
                title=data.get('title'),
                description=data.get('description'),
                amount=data.get('amount'),
                expiry_date=data.get('expiry_date'),
                purpose=data.get('purpose')
            )
            return api_response(201, "Post created successfully", {"post_id": post.id})
        except Exception as e:
            return api_response(400, f"Error: {str(e)}")


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return api_response(404, "not found post")


    if post.user != request.user:
        return api_response(403, "You can only take action on your own post.")

    if request.method == 'PUT':
        data = request.data
        post.title = data.get('title', post.title)
        post.description = data.get('description', post.description)
        post.amount = data.get('amount', post.amount)
        post.purpose = data.get('purpose', post.purpose)
        post.save()
        return api_response(200, "Post updated successfully")

    elif request.method == 'DELETE':
        post.delete()
        return api_response(200, "Post deleted successfully")