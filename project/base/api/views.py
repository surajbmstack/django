from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from . serializer import RoomSerializer
@api_view(['GET'])
def routes(request):
    routes=[
        'GET /api/rooms',
        'GET /api/rooms/:id',

    ]

    return Response(routes)
@api_view(['GET'])
def getRomms(request):
    rooms=Room.objects.all()
    serializer=RoomSerializer(rooms,many=True)
    
    return Response(serializer.data)