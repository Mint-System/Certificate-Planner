import graphene

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.graphql_base import OdooObjectType


class DocumentType(OdooObjectType):
    designation = graphene.String(required=True)
    identification = graphene.String(required=True)
    description = graphene.String(required=True)


class Part(OdooObjectType):
    name = graphene.String(required=True)


class Document(OdooObjectType):
    name = graphene.String(required=True)
    title = graphene.String(required=True)
    type = graphene.Field(DocumentType)
    parts = graphene.List(graphene.NonNull(lambda: Part), required=True)

    @staticmethod
    def resolve_type(root, info):
        return root.type_id or None

    @staticmethod
    def resolve_parts(root, info):
        return root.part_ids


class Query(graphene.ObjectType):
    all_documents = graphene.List(
        graphene.NonNull(Document),
        required=True,
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    @staticmethod
    def resolve_all_documents(root, info, limit=None, offset=None):
        domain = []
        return info.context["env"]["certificate_planer.document"].search(
            domain, limit=limit, offset=offset
        )


schema = graphene.Schema(query=Query)
