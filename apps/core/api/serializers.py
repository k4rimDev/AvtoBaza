from rest_framework import serializers

from apps.core import models


class SliderSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = models.Slider
        fields = ('id', 'image', 'title', 'brand', 'group')

    def get_brand(self, obj):
        try:
            queryset = obj.brand.slug
        except:
            queryset = None
        return queryset
    
    def get_group(self, obj):
        try:
            queryset = obj.group.slug
        except:
            queryset = None
        return queryset

class CampaignTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CampaignText
        fields = ('id', 'text', )

class BrandNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BrandNumber
        fields = ('id', 'brand_logo', 'number', 'name')

class MainDataSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.MainData
        fields = ('id', 'logo', 'favicon', 'footer_logo', 
                  'phone_number', 'hero_section_bg')
        
class AboutUsSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.AboutUs
        fields = ('id', 'title', 'text')

class SuggestionComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SuggestionComplaints
        fields = ('text', )

    def validate(self, attrs):
        text = attrs.get('text')
        if not text:
            raise serializers.ValidationError({"message": 'Text is required'})
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context["request"].user
        instance = models.SuggestionComplaints.objects.create(
            user=user,
            **validated_data
        )

        return instance
