from django.conf import settings
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator, AutoSchema
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class APISchema(AutoSchema):
    def __init__(self, manual_fields=None, extra_fields=None):
        self.extra_fields = extra_fields or {}
        if not manual_fields:
            manual_fields = []
        super().__init__(manual_fields)

    def get_manual_fields(self, path, method):
        extra_fields = self.extra_fields.get(method) or []
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class SwaggerUIRenderer(renderers.SwaggerUIRenderer):
    def set_context(self, data, renderer_context):
        with open(settings.BASE_DIR + '/vpo_admin/table.py', 'r') as f:
            table = f.read()
        renderer_context['table'] = table
        super(SwaggerUIRenderer, self).set_context(data, renderer_context)


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """

    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        schema = None
        permission_classes = [IsAuthenticated]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            SwaggerUIRenderer
        ]

        def get(self, request):
            generator = SchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf
            )
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()
