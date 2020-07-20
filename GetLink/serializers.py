from rest_framework import serializers
from .models import FileObject


class GetLinkSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileObject
        fields =['fileName','fileId','url','directUrl']

