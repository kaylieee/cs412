from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.functions import ExtractYear
from datetime import date
from .models import Voter

# Create your views here.
class ShowAllVotersView(ListView):
    '''
    Define a view class to show all voters
    '''

    model = Voter
    template_name = "voter_analytics/show_all_voters.html"
    context_object_name = "voters"
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()

        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                qs = qs.filter(party=party)
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            min_year_date = date(int(min_dob), 1, 1)
            if min_dob:
                qs = qs.filter(dob__gte=min_year_date)
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            max_year_date = date(int(max_dob), 12, 31)
            if max_dob:
                qs = qs.filter(dob__lte=max_year_date)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                qs = qs.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                qs = qs.filter(v20state='TRUE')
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                qs = qs.filter(v21town='TRUE')

        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                qs = qs.filter(v21primary='TRUE')

        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                qs = qs.filter(v22general='TRUE')

        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                qs = qs.filter(v23town='TRUE')

        return qs
    

class ShowVoterView(DetailView):
    '''
    Define a view class to show a voter
    '''

    model = Voter
    template_name = "voter_analytics/show_voter.html"
    context_object_name = "voter"