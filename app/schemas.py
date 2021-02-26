from marshmallow import Schema, fields


class ProductSchema(Schema):
    display_name = fields.Str()
    lst_price = fields.Float()

class PosConfigSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class PosOrderSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    amount_paid = fields.Float()
    amount_total = fields.Float()


class PosOrderLineSchema(Schema):
    id = fields.Int()

