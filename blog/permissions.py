from django.shortcuts import redirect
from django.contrib import messages


class OwnershipRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()

        if obj.author != self.request.user:
            messages.error(
                request,
                "You do not have the permission required to perform the "
                "requested operation because you are not the author.",
            )
            previous_page = request.META.get("HTTP_REFERER", "/")
            return redirect(previous_page)

        return super(OwnershipRequiredMixin, self).dispatch(request, *args, **kwargs)
