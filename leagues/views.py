from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker

from django.db.models import Count

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		#"baseball_leagues": League.objects.filter(sport="Baseball"),
		"baseball_leagues": League.objects.filter(sport__contains="baseball"),
		"women_leagues": League.objects.filter(name__contains="women"),
		"all_hockey_leagues": League.objects.filter(sport__contains="hockey"),
		"not_football_leagues": League.objects.exclude(sport__contains="football"),
		"conferences_leagues": League.objects.filter(name__contains="conference"),
		"all_league_atlantic": League.objects.filter(name__contains="atlantic"),
		"teams_house_dallas": Team.objects.filter(location__contains="dallas"),
		"teams_with_raptors": Team.objects.filter(team_name__contains="raptors"),
		"teams_with_city": Team.objects.filter(location__contains="city"),
		"teams_startswith_t": Team.objects.filter(team_name__startswith="T"),
		"teams_orderby_location": Team.objects.all().order_by("location"),
		"teams_orderby_name": Team.objects.all().order_by("-team_name"),
		"player_lastname_cooper": Player.objects.filter(last_name__contains="cooper"),
		"player_name_joshua": Player.objects.filter(first_name__contains="joshua"),
		"player_cooper_less_joshua": Player.objects.filter(last_name__contains="cooper").exclude(first_name__contains="joshua"),
		"player_name_alexander_or_wyatt": Player.objects.filter(first_name__in=["Alexander","Wyatt"]),
	}
	return render(request, "leagues/index.html", context)

def index2(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"teams_atlantic_soccer_conference": Team.objects.filter(league__name__contains="atlantic soccer conference"),
		"players_boston_penguins": Player.objects.filter(curr_team__location="Boston", curr_team__team_name="Penguins"),
		"players_ICBC": Player.objects.filter(curr_team__league__name__contains="collegiate"),
		"players_ACAF": Player.objects.filter(curr_team__league__name="American Conference of Amateur Football").filter(last_name="Lopez"),
		"football_players":Player.objects.filter(curr_team__league__sport__contains="football"),
		"players_name_sophia":Player.objects.filter(first_name="Sophia"),
		"leagues_name_sophia":Player.objects.filter(first_name="Sophia"),
		"players_flores": Player.objects.filter(last_name = "Flores").exclude(curr_team__team_name="Roughriders", curr_team__location="Washington"),
		"teams_samuel_evans": Player.objects.get(last_name = "Evans", first_name = "Samuel").all_teams.all(),
		"players_tiger_cats": Team.objects.get(team_name = "Tiger-Cats", location="Manitoba").all_players.all(),
		"explayers_vikings": Team.objects.get(team_name = "Vikings", location="Wichita").all_players.all().exclude(curr_team__team_name="Vikings"),
		"exteams_jacob_gray": Player.objects.get(last_name = "Gray", first_name = "Jacob").all_teams.all().exclude(team_name="Colts", location="Oregon"),
		"all_joshua": Player.objects.filter(all_teams__league__name="Atlantic Federation of Amateur Baseball Players").filter(first_name="Joshua"),
		"12_players": Team.objects.annotate(num_players=Count("all_players")).filter(num_players__gt=12),
		"number_teams":Player.objects.all().values("first_name", "last_name").annotate(total_teams=Count("all_teams")).order_by("-total_teams"),
	}

	return render(request, "leagues/index2.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")
