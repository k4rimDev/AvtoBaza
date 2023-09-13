from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                      verbose_name="Yaranma tarixi")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True,
                                      verbose_name="Güncəllənmə tarixi")

    class Meta:
        abstract = True

class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, editable=False, db_index=True)

    class Meta:
        abstract = True

class CustomPaginationMixin(object):

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination
        is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given
        output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
