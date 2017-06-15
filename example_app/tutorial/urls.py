import json

from django.conf.urls import url, include

from coreapi.compat import force_bytes

from openapi_codec.encode import generate_swagger_object

from rest_framework.routers import DefaultRouter

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from jsonhyperschema_codec import JSONHyperSchemaCodec

from snippets import views


router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)


class JSONHyperSchemaRenderer(renderers.BaseRenderer):

    media_type = 'application/schema+json'
    format = 'json'

    def render(self, data, media_type=None, renderer_context=None):
        codec = JSONHyperSchemaCodec()
        return codec.load(force_bytes(json.dumps(generate_swagger_object(data))))


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
        JSONHyperSchemaRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)


urlpatterns = [
    url('^$', SwaggerSchemaView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
