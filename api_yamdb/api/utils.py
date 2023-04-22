from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class GenreCategoryViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class ViewSetWithoutPut(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
