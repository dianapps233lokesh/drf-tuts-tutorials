from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer,UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins,generics
from django.contrib.auth.models import User
from rest_framework import permissions,renderers
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import viewsets,renderers


# @csrf_exempt
# def snippet_list(request):
#     if request.method=='GET':
#         snippets=Snippet.objects.all()
#         serializer=SnippetSerializer(snippets,many=True)
#         return JsonResponse(serializer.data,safe=False)
#     elif request.method=='POST':
#         data=JSONParser().parse(request)
#         serializer=SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data,status=201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def snippet_detail(request,pk):
#     try:
#         snippet=Snippet.objects.get(pk=pk)
#     except Exception.DoesNotExist:
#         return HttpResponse(status=404)
    
#     if request.method=='GET':
#         serializer=SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#     elif request.method=='PUT':
#         data=JSONParser().parse(request)
#         serializer=SnippetSerializer(snippet,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors,status=400)
#     elif request.method=='DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)



# @api_view(['GET','POST'])
# def snippet_list(request,format=None):
#     if request.method=='GET':
#         snippets=Snippet.objects.all()
#         serializer=SnippetSerializer(snippets,many=True)
#         return Response(serializer.data)
    
#     elif request.method=='POST':
#         serializer=SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def snippet_detail(request,pk,format=None):
#     try:
#         snippet=Snippet.objects.get(pk = pk)
#     except Exception.DoesNotExist:
#         return HttpResponse(status=404)
    
#     if request.method=='GET':
#         serializer=SnippetSerializer(snippet)
#         return Response(serializer.data)
#     elif request.method=='PUT':
       
#         serializer=SnippetSerializer(snippet,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method=='DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#list view using class based views
# class SnippetList(APIView):
#     def get(self,request,format=None):
#         snippets=Snippet.objects.all()
#         serializer=SnippetSerializer(snippets,many=True)
#         return Response(serializer.data)

#     def post(self,request,format=None):
#         serializer=SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#detail view using class based views


# class SnippetDetail(APIView):
#     def get_object(self,pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
        
#     def get(self,request,pk,format=None):
#         snippets=self.get_object(pk)
#         serializer=SnippetSerializer(snippets)
#         return Response(serializer.data)

#     def put(self,request,pk,format=None):
#         snippet=self.get_object(pk)
#         serializer=SnippetSerializer(snippet,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=
#                         status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk,format=None):
#         snippet=self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#using mixins
# class SnippetList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Snippet.objects.all()
#     serializer_class=SnippetSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
# class SnippetDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset=Snippet.objects.all()
#     serializer_class=SnippetSerializer

#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request,*args,**kwargs)

#     def put(self,request, *args, **kwargs):
#         return self.update(request,*args,**kwargs)

#     def delete(self,request, *args, **kwargs):
#         return self.destroy(request,*args,**kwargs)


#using generic class based views

class SnippetList(generics.ListCreateAPIView):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

# @api_view(['GET'])
# def api_root(request,format=None):
#     return Response({
#         'users':reverse('user-list',request=request,format=format),
#         'snippets':reverse('snippet-list',request=request,format=format)
#     })

class SnippetHighlight(generics.GenericAPIView):
    queryset=Snippet.objects.all()
    renderer_classes=[renderers.StaticHTMLRenderer
                      ]
    def get(self,request,*args, **kwargs):
        snippet=self.get_object()
        return Response(snippet.highlighted)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset=Snippet.objects.all()
    serializer_class=SnippetSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self,request, *args, **kwargs):
        snippet=self.get_object()
        return Response(snippet.highlighted)
    
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)