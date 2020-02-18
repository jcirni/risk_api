from ..records.models import (
    Restaurant, Inspection, Violation, InspectionViolation
)
from ..utils import helpers
from ..utils import records_validators as validators

from rest_framework import serializers


class RestaurantSerializer(serializers.Serializer):
    """
    custom serializer for Restaurant to remove uniqueness check during
    serialization on inbound inspection payloads."""

    restaurant_id = serializers.IntegerField(validators=[validators.valid_id])
    name = serializers.CharField(max_length=50)
    street_address = serializers.CharField(
        max_length=50, validators=[validators.valid_address])
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=2, validators=[
        validators.valid_state_abbrev])
    postal_code = serializers.CharField(
        max_length=5, validators=[validators.valid_zip])
    sum_score = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True)
    sum_violations = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True)
    total_inspections = serializers.IntegerField(default=0, read_only=True)

    def create(self, validated_data):
        return Restaurant(**validated_data)

    def update(self, instance, validated_data):
        self.restaurant_id = validated_data.get(
            'restaurant_id', instance.restaurant_id)
        self.name = validated_data.get('name', instance.name)
        self.street_address = validated_data.get(
            'street_address', instance.street_address)
        self.city = validated_data.get('city', instance.city)
        self.state = validated_data.get('state', instance.state)
        self.postal_code = validated_data.get(
            'postal_code', instance.postal_code)
        instance.save()
        return instance


class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = ['violation_id', 'is_critical',
                  'code', 'description', 'comments']


class InspectionSerializer(serializers.ModelSerializer):
    violations = ViolationSerializer(many=True, required=False)
    restaurant = RestaurantSerializer()

    class Meta:
        model = Inspection
        fields = ['inspection_id', 'inspection_date',
                  'score', 'comments', 'violations', 'restaurant']

    def create(self, validated_data):
        """create override to support writable nested object handling"""
        violations_data = validated_data.pop('violations')
        restaurant_data = validated_data.pop('restaurant')
        # If new restaurant, create it
        r = helpers.get_if_exists(
            Restaurant, restaurant_id=restaurant_data['restaurant_id'])
        if r is None:
            r = Restaurant(**restaurant_data)
            r.save()
        inspection = Inspection.objects.create(
            restaurant_id=r.restaurant_id, **validated_data)
        # update restaurant state, in case of violation failure
        r.is_current = False
        r.save()

        for obj in violations_data:
            violation = Violation.objects.create(
                inspection_id=inspection.inspection_id, **obj)
            InspectionViolation.objects.create(
                inspection_id=inspection.inspection_id, violation=violation)

        r.update_aggregates(num_violations=len(
            violations_data), score=inspection.score)

        return inspection


class InspectionSubSetSierializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = ['inspection_id', 'inspection_date', ]


class HistorySerializer(serializers.ModelSerializer):
    inspections = InspectionSubSetSierializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'restaurant_id', 'name', 'street_address', 'city', 'state',
            'postal_code', 'average_score', 'average_violations',
            'total_inspections', 'inspections'
        ]
