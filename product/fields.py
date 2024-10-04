from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    description = 'Ordering product field'

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_unique_for_field(**kwargs)
        ]

    def _check_unique_for_field(self, **kwargs):

        field_object = self.model._meta.get_fields()
        filds_list = []

        for obj in field_object:
            filds_list.append(obj.name)

        if self.unique_for_field is None:
            return [
                checks.ERROR(
                    'unique_for_field must be set',
                    obj=self,
                    id='products.E001',
                )
            ]

        elif self.unique_for_field not in filds_list:
            return [
                checks.ERROR(
                    'unique_for_field not found',
                    obj=self,
                    id='products.E002',
                )
            ]

        else:
            return []

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                all_objects = self.model.objects.all()
                filter_query = {
                    self.unique_for_field: getattr(model_instance, self.unique_for_field)
                }
                filter_objects = all_objects.filter(**filter_query)
                last_item = filter_objects.latest(self.attname) #خروجی last_item ، یک productline می‌باشد.
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 1

            return value

        else:
            return super().pre_save(model_instance, add)
