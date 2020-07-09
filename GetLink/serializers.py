from rest_framework import serializers
from .models import LinkExtract


class GetLinkSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LinkExtract
        fields =['fileName','fileId','url','directUrl']

