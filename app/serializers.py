from marshmallow import Schema, fields


class RegistrationModelSchema(Schema):
    id = fields.Int(dump_only=True)
    hash_password = fields.Str()
    username = fields.Str(required=True)
    telegram_user = fields.Int()


class UserModelSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime()


class TypesSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class CategoryModelSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    user_id = fields.Int(required=True)
    type_coin = fields.Int()


class SubCategoryModelSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    id_category = fields.Int(required=True)
    user_id = fields.Int(required=True)
    type_coin = fields.Int()


class CoinModelSchema(Schema):
    id = fields.Int(dump_only=True)
    id_subcategory = fields.Int(required=True)
    value = fields.Int(required=True)
    date = fields.Date()
    user_id = fields.Int(required=True)


class TagsModelSchema(Schema):
    id = fields.Int(dump_only=True)
    tag_name = fields.Str()
    coin_id = fields.Int(required=True)
