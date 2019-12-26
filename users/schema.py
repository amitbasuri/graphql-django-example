import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from .models import User, Country, City, State


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class StateType(DjangoObjectType):
    class Meta:
        model = State


class CityType(DjangoObjectType):
    class Meta:
        model = City


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        profile_image_url = graphene.String(required=False)
        gender = graphene.String(required=True)
        country_id = graphene.Int(required=True)
        state_id = graphene.Int(required=True)
        city_id = graphene.Int(required=True)
        contact_number = graphene.String(required=True)
        skill = graphene.String(required=True)
        date_of_birth = graphene.Date(required=True)

    def mutate(self, info, password, email, country_id, state_id, city_id, **kwargs):
        country = Country(id=country_id)
        state = State(id=state_id)
        city = City(id=city_id)
        user = User(
            email=email,
            country=country,
            state=state,
            city=city,
            **kwargs
        )

        user.set_password(password)
        user.full_clean()
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType,
                          search=graphene.String(),
                          first=graphene.Int(),
                          skip=graphene.Int(),
                          )

    countries = graphene.List(CountryType, search=graphene.String(),
                              first=graphene.Int(),
                              skip=graphene.Int(),
                              )
    states = graphene.List(StateType, search=graphene.String(),
                           country_id=graphene.Int(),
                           first=graphene.Int(),
                           skip=graphene.Int(),
                           )
    cities = graphene.List(CityType, search=graphene.String(),
                           country_id=graphene.Int(),
                           state_id=graphene.Int(),
                           first=graphene.Int(),
                           skip=graphene.Int(),
                           )

    def resolve_users(self, info, search=None, first=None, skip=None, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        qs = User.objects.all()
        if search:
            filter = (
                Q(email__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    def resolve_countries(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Country.objects.all()

        if search:
            filter = (
                Q(name__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_states(self, info, search=None, country_id=None, first=None, skip=None, **kwargs):
        qs = State.objects.all()
        if country_id:
            qs = qs.filter(country_id=country_id)

        if search:
            filter = (
                Q(name__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_cities(self, info, search=None, country_id=None, state_id=None, first=None, skip=None, **kwargs):
        qs = City.objects.all()
        if country_id:
            qs = qs.filter(country_id=country_id)

        if state_id:
            qs = qs.filter(state_id=state_id)

        if search:
            filter = (
                Q(name__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs
