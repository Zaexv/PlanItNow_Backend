import graphene
import graphql_jwt

import friendship.schema
import plans.schema
import userprofiles.schema
import users.schema


class Query(plans.schema.Query,
            users.schema.Query,
            userprofiles.schema.Query,
            friendship.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation,
               plans.schema.Mutation,
               friendship.schema.Mutation,
               userprofiles.schema.Mutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
