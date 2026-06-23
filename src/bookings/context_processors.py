from bookings.forms import CallbackLeadForm


def callback_modal(request):
    return {'callback_form': CallbackLeadForm()}
