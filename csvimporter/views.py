from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail
from django.contrib import messages
from core.models import Customer, Product, Sale
from csvimporter.models import CSV
from csvimporter.forms import CSVForm, CSVAssociateForm

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


@login_required
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


@login_required
def associate(request, object_id, modelname="", **kwargs):
    if not kwargs.get("template_name"):
        kwargs["template_name"] = 'csv_detail.html'
    if not kwargs.get("form_class"):
        kwargs["form_class"] = CSVAssociateForm
    if not modelname:
        raise ValueError(
            "A model wasn't specified. This is our fault. Please let us know this happened so we can fix it, thanks.")
    else:
        kwargs["model"] = eval(modelname)

    kwargs = prepare_view(request, kwargs)
    instance = get_object_or_404(CSV, pk=object_id)
    if request.method == 'POST':
        form = kwargs["form_class"](instance, request.POST)
        if form.is_valid():
            form.save(request)
            request.user.message_set.create(message='CSV imported.')
            return HttpResponseRedirect("/core/%s" % (modelname.lower()))
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


@login_required
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
            modelname = kwargs["model"].__name__
            instance = form.save()
            return HttpResponseRedirect(
                reverse('associate-csv', args=[instance.id, modelname]))
    else:
        form = kwargs["form_class"](kwargs["model"])
    kwargs["extra_context"].update({"form": form})
    kwargs["extra_context"].update({"csv_import_type": request.get_full_path().split('/')[3]})
    return render_to_response(kwargs["template_name"],
        kwargs["extra_context"],
        context_instance=RequestContext(request)
    )
