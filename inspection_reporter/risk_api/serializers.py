from inspection_reporter.records.models import Restaurant, Inspection, Violation, InspectionViolation
from inspection_reporter.utils.helpers import get_if_exists
from rest_framework import serializers


class RestaurantSerializer(serializers.Serializer):
    """
    custom validation for Restaurant uniqueness on inspection payloads."""

    restaurant_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    street_address = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=2)
    postal_code = serializers.CharField(max_length=5)

    def create(self, validated_data):
        return Restaurant(**validated_data)

    def update(self, instance, validated_data):
        restaurant_id = validated_data.get(
            'restaurant_id', instance.restaurant_id)
        name = validated_data.get('name', instance.name)
        street_address = validated_data.get(
            'street_address', instance.street_address)
        city = validated_data.get('city', instance.city)
        state = validated_data.get('state', instance.state)
        postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.save()
        return instance

    class Meta:
        model = Restaurant
        fields = ['restaurant_id', 'name', 'street_address',
                  'city', 'state', 'postal_code']


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
        violations_data = validated_data.pop('violations')
        restaurant_data = validated_data.pop('restaurant')
        # If new restaurant, create it
        r = get_if_exists(
            Restaurant, restaurant_id=restaurant_data['restaurant_id'])
        if r is None:
            r = Restaurant(**restaurant_data)
            r.save()
        inspection = Inspection.objects.create(
            restaurant_id=r.restaurant_id, **validated_data)
        # flip flag
        r.is_current = False
        r.save()

        for obj in violations_data:
            violation = Violation.objects.create(
                inspection_id=inspection.inspection_id, **obj)
            InspectionViolation.objects.create(
                inspection_id=inspection.inspection_id, violation=violation)

        return inspection
