from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Building, ElevatorReport
from .serializers import BuildingSerializer, ElevatorReportSerializer, ReportStatusSerializer
from .logic import ConsensusManager

class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing buildings and their verified status.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    lookup_field = 'bin'

    @action(detail=True, methods=['get'])
    def status(self, request, bin=None):
        """
        Returns the current verified status for a specific building.
        """
        building = self.get_object()
        manager = ConsensusManager()
        verified_status = manager.get_verified_status(building)
        return Response({
            'bin': building.bin,
            'verified_status': verified_status
        })

class ReportViewSet(viewsets.ViewSet):
    """
    API endpoint for reporting elevator status via address.
    """
    def create(self, request):
        serializer = ReportStatusSerializer(data=request.data)
        if serializer.is_valid():
            manager = ConsensusManager()
            building = manager.get_or_create_building(
                house_number=serializer.validated_data['house_number'],
                street=serializer.validated_data['street'],
                borough=serializer.validated_data['borough']
            )

            if not building:
                return Response(
                    {"error": "Building not found in NYC Geoclient."},
                    status=status.HTTP_404_NOT_FOUND
                )

            report = manager.report_status(
                building=building,
                user_id=serializer.validated_data['user_id'],
                status=serializer.validated_data['status']
            )

            return Response(
                ElevatorReportSerializer(report).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
