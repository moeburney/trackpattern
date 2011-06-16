from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail
from django.contrib import messages
from core.models import Customer

from tracklist.csvimporter.models import CSV
from tracklist.csvimporter.forms import CSVForm, CSVAssociateForm

from django.http import HttpResponse

# TODO: Make this view class based
def prepare_view(request, kwargs):
    if not kwargs.get("model"):
        raise ValueError("You haven't specified the model")
    else:
        kwargs["app_label"] = kwargs["model"]._meta.app_label
        kwargs["model_name"] = kwargs["model"]._meta.module_name
        """
        kwargs["redirect_url"] = reverse(
                "admin:%s_%s_changelist" % (kwargs["app_label"],
                                            kwargs["model_name"])
                )
        """

        kwargs["extra_context"] = {
            "app_label": kwargs["app_label"],
            "model_name": kwargs["model_name"],
            #"redirect_url": kwargs["redirect_url"],
        }
    return kwargs


@staff_member_required
def csv_list(request, **kwargs):
    kwargs = prepare_view(request, kwargs)
    if not kwargs.get("template_name"):
        kwargs["template_name"] = 'csv_list.html'
    return object_list(request,
        queryset=CSV.objects.all(),
        template_name=kwargs["template_name"],
        template_object_name='csv',
        extra_context=kwargs["extra_context"],
    )


@staff_member_required
def associate(request, object_id, **kwargs):
    if not kwargs.get("template_name"):
        kwargs["template_name"] = 'csv_detail.html'
    if not kwargs.get("form_class"):
        kwargs["form_class"] = CSVAssociateForm
    if not kwargs.get("model"):
        kwargs["model"] = Customer

    #return HttpResponse(str(object_id))
    kwargs = prepare_view(request, kwargs)
    instance = get_object_or_404(CSV, pk=object_id)
    if request.method == 'POST':
        form = kwargs["form_class"](instance, request.POST)
        if form.is_valid():
            form.save(request)
            request.user.message_set.create(message='CSV imported.')
            return HttpResponseRedirect(kwargs["redirect_url"])
    else:
        messages.info(request, 'Uploaded CSV. Please associate fields below.')
        form = CSVAssociateForm(instance)
    kwargs["extra_context"].update({"form": form})
    return object_detail(request,
        queryset=CSV.objects.all(),
        object_id=object_id,
        template_name=kwargs["template_name"],
        template_object_name='csv',
        extra_context=kwargs["extra_context"],
    )


@staff_member_required
def new(request, **kwargs):
    if not kwargs.get("template_name"):
        kwargs["template_name"] = 'new.html'
    if not kwargs.get("form_class"):
        kwargs["form_class"] = CSVForm
    kwargs = prepare_view(request, kwargs)
    if request.method == 'POST':
        form = kwargs["form_class"](kwargs["model"],
                                    request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(str(instance.id))

            return HttpResponseRedirect(
                        reverse('associate-csv', kwargs={'object_id':instance.id} ))
    else:
        form = kwargs["form_class"](kwargs["model"])
    kwargs["extra_context"].update({"form": form})
    return render_to_response(kwargs["template_name"],
        kwargs["extra_context"],
        context_instance=RequestContext(request)
    )
