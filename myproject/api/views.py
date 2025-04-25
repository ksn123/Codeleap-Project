from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import User,Post
from .serializers import UserSerializer,PostSerializer


@api_view(['GET','POST'])
def usersGetListOrPost(request):
    match request.method:
        case 'GET':
            return getHandler(User,UserSerializer)        
        case 'POST':
            return postHandler(request,UserSerializer)
        
@api_view(['GET','DELETE','PATCH'])
def usersPatchOrDelete(request,user_id=None):
    match request.method:
        case 'GET':
            return getHandler(User,UserSerializer,user_id)
        case 'PATCH':
            return patchHandler(request,user_id,User, UserSerializer,[])
        case 'DELETE':
            return deleteHandler(user_id,User)
       
        
@api_view(['GET','POST'])
def postsGetListOrPost(request):
    match request.method:
        case 'GET':
            return getHandler(Post,PostSerializer)
        case 'POST':
            return postHandler(request,PostSerializer)
       
        
@api_view(['GET','DELETE','PATCH'])
def postsPatchOrDelete(request,post_id=None):
    match request.method:
        case 'GET':
            return getHandler(Post,PostSerializer,post_id)
        case 'PATCH':
            return patchHandler(request,post_id,Post, PostSerializer,['id', 'username', 'created_datetime'])
        case 'DELETE':
            return deleteHandler(post_id,Post)
        

def getHandler(model,serializer,id=None):
        
        name = model.__name__ 
        if id is None:
            items = model.objects.all()
            serializer = serializer(items, many=True)
            return Response(serializer.data)
        else:
            try:
                item = model.objects.get(pk=id)
                serializer = serializer(item)
                return Response(serializer.data)
            except model.DoesNotExist:
                msg = name + ' not found.'
                return Response({'error': msg }, status=status.HTTP_404_NOT_FOUND)

            

def postHandler(request,serializer):
        serializer = serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

def patchHandler(request,id, model, serializer,cantChangeValues):
    name = model.__name__ 

    if id is None:
        return Response({'error': 'Missing post ID in URL.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        instance = model.objects.get(pk=id)

        for field in cantChangeValues:
            if field in request.data:
                return Response({field: 'This field cannot be modified.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializer(instance, data=request.data, partial=True,context={'request': request} )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except model.DoesNotExist:
            msg = name + ' not found.'
            return Response({'error': msg }, status=status.HTTP_404_NOT_FOUND)

def deleteHandler(id,model):

    name = model.__name__ 

    if id is None:
        msg = 'Missing {name} ID in URL.'
        return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
    try:
        item = model.objects.get(pk=id)
        item.delete()
        msg = name + ' deleted successfully.'
        return Response({'message': msg}, status=status.HTTP_204_NO_CONTENT)
    except model.DoesNotExist:
        msg = name + ' not found.'
        return Response({'error': msg }, status=status.HTTP_404_NOT_FOUND)



