import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        profile_image_url = graphene.String(required=False)
        gender = graphene.String(required=True)
        country = graphene.String(required=True)
        state = graphene.String(required=True)
        city = graphene.String(required=True)
        contact_number = graphene.String(required=True)
        skill = graphene.String(required=True)
        date_of_birth = graphene.Date(required=True)

    def mutate(self, info, password, email, **kwargs):
        user = User(
            email=email,
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
