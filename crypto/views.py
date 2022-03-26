from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from .crypto_src import *
from utils.charts import Chart
from utils.formatting import *
from website.models import Account, Config
from .models import *
from .forms import *
from markets.models import Watchlist, Portfolio, PortfolioAmounts

class CryptoView(TemplateView):
    template_name = 'crypto/crypto.html'


def crypto(request):
    context = {}
    context['currencies'] = Currency.objects.all()
    refresh_rate = REFRESH_RATE
    coin_ids = []

    table = top_coins_by_mcap()
    table['Watchlist'] = table['Symbol'].apply(lambda
                                                   x: f"""<input type="checkbox" name="watch_{x}" id="watch_{x.split('</a>')[0].split('>')[1]}" class="star">""")
    table['Portfolio'] = table['Symbol'].apply(lambda
                                                   x: f""" <button type="submit" name="add_to_pf" value="{x.split('</a>')[0].split('>')[1]}"> Add </button>""")
    context['table'] = table.to_html(escape=False, justify='center')

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        watchlist = Watchlist.objects.filter(user=profile).first()
        coins = watchlist.coins.all()

        print(coins)
        context['watchlist_ids'] = [c.symbol.lower() for c in coins]
        print(context['watchlist_ids'])
        if profile.currency:
            context['currency'] = profile.currency.symbol
        else:
            context['currency'] = DEFAULT_CURRENCY

    if request.method == 'GET':
        return render(request, 'crypto/crypto.html', context)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'website/login_required.html', context)

        elif request.is_ajax and 'checked_symbols' in str(request.POST):
            print('ajax2')
            print(request.POST)
            symbols = request.POST['checked_symbols'].split(',')
            coin_ids = [symbol.split('_')[1].lower() for symbol in symbols if '_' in symbol]
            print(coin_ids)
            watchlist.coins.clear()
            for symbol in coin_ids:
                watchlist.coins.add(Cryptocurrency.objects.filter(symbol=symbol).first())
            context['watchlist_ids'] = coin_ids

        elif 'amount' in str(request.POST):
            print('add to portfolio')
            print(request.POST)
            coin_id = request.POST['coin']
            new_amount = request.POST['amount']
            portfolio = Portfolio.objects.get(user=profile)
            if Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id).exists():
                amount = Amounts.objects.filter(portfolio=portfolio).filter(coin=coin_id)
                amount.amount += new_amount
                print(f'added {amount} to {coin_id}')
            else:
                amount = Amounts.objects.create(portfolio=portfolio, coin=coin_id, amount=new_amount)
                print(f'created {amount} of {coin_id}')
            amount.save()

        return HttpResponseRedirect(reverse('crypto:crypto', args=()))


def add_exchange(request):
    exchange_id = request.POST['exchange_id']
    value = request.POST['value']
    print(value)
    user = request.user.profile
    exchange = Exchange.objects.get(id=exchange_id)
    if value:
        user.exchanges.add(exchange)
        msg = 'added'
    else:
        user.exchanges.remove(exchange)
        msg = 'removed'
    return HttpResponse(msg)


class ExchangesView(ListView):
    template_name = 'crypto/exchanges.html'
    model = CryptoExchange

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favourites'] = [exchange.id for exchange in self.request.user.account.exchanges.all()]
        print(context)
        return context




class DominanceView(DetailView):
    template_name = 'crypto/dominance.html'

    top_n_choices = [10, 20, 50, 100]
    mcap_col = f'Market cap (USD)'


    def get_queryset(self):
        return Cryptocurrency.objects.filter(price > 0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_n_coins = int(request.GET['top_n_coins']) if 'top_n_coins' in str(request.GET) else 20
        top_n_choices.remove(top_n_coins)
        top_n_choices.insert(0, top_n_coins)
        PALETTE = [get_random_color() for i in range(top_n_coins)]
        df = pd.read_csv('crypto.csv', index_col=0).iloc[:top_n_coins][['Symbol', mcap_col]]
        df[mcap_col] = df[mcap_col].apply(lambda x: x.replace(',', ''))
        df['Dominance'] = df[mcap_col].apply(lambda x: 100 * float(x) / sum(df[mcap_col].astype('float64')))
        #df.loc[:, mcap_col] = list(map(lambda x: format(x, ','), df.loc[:, mcap_col]))
        chart = Chart('doughnut', chart_id='dominance_chart', palette=PALETTE)
        chart.from_df(df, values='Dominance', labels=list(df.loc[:, 'Symbol']))
        js_scripts = chart.get_js()
        context['charts'] = []
        context['charts'].append(chart.get_presentation())
        context['table'] = chart.get_html()
        context['js_scripts'] = js_scripts
        context['top_n_choices'] = top_n_choices
        return context



def dominance(request):
    context = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.currency:
            currency = profile.currency.symbol
    else:
        currency = DEFAULT_CURRENCY
    top_n_choices = [10, 20, 50, 100]
    mcap_col = f'Market cap (USD)'

    if request.method == 'GET':
        top_n_coins = int(request.GET['top_n_coins']) if 'top_n_coins' in str(request.GET) else 20
        top_n_choices.remove(top_n_coins)
        top_n_choices.insert(0, top_n_coins)
        PALETTE = [get_random_color() for i in range(top_n_coins)]
        df = pd.read_csv('crypto.csv', index_col=0).iloc[:top_n_coins][['Symbol', mcap_col]]
        df[mcap_col] = df[mcap_col].apply(lambda x: x.replace(',', ''))
        df['Dominance'] = df[mcap_col].apply(lambda x: 100 * float(x) / sum(df[mcap_col].astype('float64')))
        #df.loc[:, mcap_col] = list(map(lambda x: format(x, ','), df.loc[:, mcap_col]))
        chart = Chart('doughnut', chart_id='dominance_chart', palette=PALETTE)
        chart.from_df(df, values='Dominance', labels=list(df.loc[:, 'Symbol']))
        js_scripts = chart.get_js()
        context['charts'] = []
        context['charts'].append(chart.get_presentation())
        context['table'] = chart.get_html()
        context['js_scripts'] = js_scripts
        context['top_n_choices'] = top_n_choices

        return render(request, 'crypto/dominance.html', context)



class GlobalMetricsView(TemplateView):
    template_name = 'crypto/global_metrics.html'

    def get_context_data(self, **kwargs):
        return {}


class CryptoCalendarView(TemplateView):
    template_name = 'crypto/calendar.html'




class NFTView(TemplateView):
    template_name = 'crypto/nft.html'


class DeFiView(TemplateView):
    template_name = 'crypto/defi.html'




class TrendsView(TemplateView):
    template_name = 'crypto/trends.html'


    def get_context_data(self, **kwargs):
        filename = Config.objects.get(key='crypto_file') if Config.objects.get(
            key='crypto_file').exists() else 'crypto.csv'
        refresh_rate = Config.objects.get(key='refresh_rate') if Config.objects.get(
            key='refresh_rate').exists() else 600
        if filename in os.listdir() and datetime.datetime.now().timestamp() - os.path.getmtime(filename) < refresh_rate:
            coins = pd.read_csv(filename, index_col=0).iloc[:, :8]
        else:
            coins = top_coins_by_mcap().iloc[:, :8]
        coins.loc[:, 'Price'] = coins.loc[:, 'Price'].astype('float64').round(6)
        timeframe = request.GET['timeframe'] if 'timeframe' in str(request.GET) else '24h'
        timeframes = ['1h', '24h']
        timeframes.remove(timeframe)
        timeframes.insert(0, timeframe)
        sort_key = timeframe + ' Δ'
        gainers = coins.sort_values(by=sort_key, ascending=False)
        losers = coins.sort_values(by=sort_key, ascending=True)
        gainers = prepare_df_display(gainers)
        losers = prepare_df_display(losers)
        return {'timeframes': timeframes, 'gainers_table': gainers.to_html(justify='center', escape=False),
                'losers_table': losers.to_html(justify='center', escape=False)}




class WatchlistView(ListView):
    template_name = 'crypto/watchlist.html'
    model = Watchlist

    # def get(self, request, *args, **kwargs):
    #     # context = self.get_context_data(kwargs['pk'])
    #
    #     return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'add_coin' in str(request.POST):
            coin = Cryptocurrency.objects.get(symbol=request.POST['coin'])
            context['watchlist'].coins.add(coin)
            context['watchlist'].save()

        return HttpResponseRedirect(reverse('crypto:watchlist2', kwargs={'id': kwargs['id']}))

    def get_queryset(self):
        return self.model.objects.get(pk=self.kwargs['pk']).coins.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['watchlists'] = Watchlist.objects.filter(user=self.request.user.profile)
        print(data)
        data['add_form'] = AddCoin
        return data




@login_required
def watchlist(request):
    profile = Profile.objects.get(user=request.user)
    watchlists = Watchlist.objects.filter(user=profile)
    watchlist = watchlists.first()
    coins = Cryptocurrency.objects.all()
    watchlist_coins = watchlist.coins.all()


    context = {'watchlists': watchlists, 'coins': coins, 'watchlist_coins': watchlist_coins,
               'new_watchlist': NewWatchlist(), 'change_currency': ChangeCurrency(), 'set_source': SetSource(),
               'add_form': AddToPortfolio()}

    if request.method == 'GET':
        return render(request, 'crypto/watchlist.html', context)


    elif request.method == 'POST':
        if 'add_coin' in str(request.POST):
            print('addin')
            watchlist.coins.add(Cryptocurrency.objects.get(symbol=request.POST['selected_coin']))
            watchlist.save()

        elif 'delete' in str(request.POST):
            ids_to_delete = [x.split('_')[1] for x in request.POST['checked_symbols'].split(',')]
            for id in ids_to_delete:
                watchlist.coins.remove(Cryptocurrency.objects.get(id=id))

        elif 'change_currency' in str(request.POST):
            print(request.POST)
            chg_form = ChangeCurrency(request.POST)
            if chg_form.is_valid():
                data = chg_form.cleaned_data
                new_currency = Currency.objects.get(id=data['currency'])
                portfolio.currency = new_currency
                portfolio.save()
            else:
                print(f'errors: {chg_form.errors}')

        elif 'add_to_portfolio' in str(request.POST):
            print('addin')
            add_form = AddToPortfolio(request.POST)
            if add_form.is_valid():
                data = add_form.cleaned_data
                coin = data['coin']
                amount = data['amount']
                if Amounts.objects.filter(portfolio=portfolio).filter(coin=coin).exists():
                    amount_obj = Amounts.objects.filter(portfolio=portfolio).filter(coin=coin)
                    amount_obj.amount += amount
                    amount_obj.save()
                else:
                    new_amount = Amounts.objects.create(portfolio=portfolio, coin=coin, amount=amount)
                    new_amount.save()
            else:
                print(f'errors: {add_form.errors}')

        elif 'new_watchlist' in str(request.POST):
            print('new_watch')
            print(request.POST)

            watchlist_form = NewWatchlist(request.POST)
            if watchlist_form.is_valid():
                form_data = watchlist_form.cleaned_data
                currency = Currency.objects.get(symbol=form_data['currency'])
                if form_data['type'] == 'Watchlist':
                    Watchlist.objects.create(user=profile, currency=currency)
                elif form_data['type'] == 'Portfolio':
                    Portfolio.objects.create(user=profile, currency=currency)

        elif 'source' in str(request.POST):
            print('set source')
            print(request.POST)
            source_form = SetSource(request.POST)
            if source_form.is_valid():
                form_data = source_form.cleaned_data
                exchange = Exchange.objects.get(id=form_data['source'])
                watch_coin = watchlist.coins.objects.get(id=form_data['coin'])
                watch_coin.source = exchange
                watch_coin.save()
                print(f'source changed to {form_data["source"]}')
            else:
                print(f'errors: {source_form.errors}')

        return HttpResponseRedirect(reverse('crypto:watchlist', args=()))


class PortfolioView(ListView):
    template_name = 'crypto/portfolio.html'
    model = Portfolio


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return HttpResponseRedirect(reverse('crypto:portfolio', args=()))

    def get_context_data(self, **kwargs):
        return {}

    def get_queryset(self):
        return self.model.objects.get(pk=self.kwargs['pk']).coins.all()
