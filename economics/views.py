from django.shortcuts import render
from django.views.generic import TemplateView
from .fundamentals import FundamentalData
from .forms import FindTicker


class MacroView(TemplateView):
    template_name = 'economics/macro.html'




class FundamentalsView(TemplateView):
    template_name = 'economics/fundamentals.html'
    form_class = FindTicker

    def get(self, request, *args, **kwargs):
        pass


def fundamentals(request):
    context = {'search_form': FindTicker()}

    if request.method == 'GET' and 'ticker' in str(request.GET):
        print(request.GET)
        find_form = FindTicker(request.GET)
        if find_form.is_valid():
            form_data = find_form.cleaned_data
            print(form_data)
            ticker = form_data['ticker']
            context['ticker'] = ticker
            data = FundamentalData(ticker)
            context.update(data.get_fundamentals())
            print(context)
            context['price_history'] = data.get_price_history()
        else:
            print(find_form.errors)

        return render(request, 'economics/fundamentals.html', context)

    else:
        return render(request, 'economics/ticker_not_found.html', context)




