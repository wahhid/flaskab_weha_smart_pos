import json
from sqlalchemy.sql import func
from flask import g
from flask import request
from flask_appbuilder.api import ModelRestApi, BaseApi, expose, rison, safe
from flask_appbuilder.security.decorators import protect
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder, db, models, schemas


greeting_schema = {"type": "object", "properties": {"name": {"type": "string"}}}


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good python tutorial',
        'done': False
    }
] 

def get_user_id():
    try:
        return g.user.id
    except Exception:
        return None

def get_user():
    try:
        return g.user
    except Exception:
        return None

class ExampleApi(BaseApi):

    resource_name = "example"
    apispec_parameter_schemas = {"greeting_schema": greeting_schema}

    @expose("/greeting")
    def greeting(self):
        """Send a greeting
        ---
        get:
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        return self.response(200, message="Hello")

    @expose("/greeting2", methods=["POST", "GET"])
    def greeting2(self):
        """Send a greeting
        ---
        get:
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        post:
          responses:
            201:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        if request.method == "GET":
            return self.response(200, message="Hello (GET)")
        return self.response(201, message="Hello (POST)")

    @expose("/greeting3")
    @rison()
    def greeting3(self, **kwargs):
        if "name" in kwargs["rison"]:
            return self.response(
                200, message="Hello {}".format(kwargs["rison"]["name"])
            )
        return self.response_400(message="Please send your name")

    @expose("/greeting4")
    @rison(greeting_schema)
    def greeting4(self, **kwargs):
        """Get item from Model
        ---
        get:
          parameters:
          - $ref: '#/components/parameters/greeting_schema'
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        return self.response(200, message="Hello {}".format(kwargs["rison"]["name"]))

    @expose("/risonjson")
    @rison()
    def rison_json(self, **kwargs):
        """Say it's risonjson
        ---
        get:
          responses:
            200:
              description: Say it's private
              content:
                application/json:
                  schema:
                    type: object
        """
        return self.response(200, result=kwargs["rison"])

    @expose("/private")
    @protect()
    def private(self):
        """Say it's private
        ---
        get:
          responses:
            200:
              description: Say it's private
              content:
                application/json:
                  schema:
                    type: object
            401:
              $ref: '#/components/responses/401'
        """
        return self.response(200, message="This is private")

    @expose("/error")
    @protect()
    @safe
    def error(self):
        """Error 500
        ---
        get:
          responses:
            500:
              $ref: '#/components/responses/500'
        """
        raise Exception

class PosApi(BaseApi):
    resource_name = "pos"
  
    @expose("/get_user_id")
    @protect()
    def get_user_id(self):
      user_id = get_user_id()
      return self.response(200, data=user_id)

    # @expose("/products")
    # def products(self):
    #     products_schema = schemas.ProductSchema(many=True)
    #     products = db.session.query(models.ProductProduct).all()
    #     if not products:
    #         return self.response(404)
    #     result = products_schema.dump(products)
    #     return self.response(200, data=result)

    # @expose("/product/<int:product_id>")
    # def product(self, product_id):
    #     product_schema = schemas.ProductSchema()
    #     product = db.session.query(models.ProductProduct).get(product_id)
    #     if not product:
    #         return self.response(404)
    #     result = product_schema.dump(product)
    #     return self.response(200, data=result)

    # @expose("/product/barcode/<barcode>")
    # def product_barcode(self, barcode):
    #     product_schema = schemas.ProductSchema()
    #     product = db.session.query(models.ProductProduct).filter_by(barcode=barcode).first()
    #     if not product:
    #         return self.response(404)
    #     result = product_schema.dump(product)
    #     return self.response(200, data=result)


    # @expose("/pos_config")
    # def pos_configs(self):
    #     configs = db.session.query(models.PosConfig).all()
    #     return self.response(200, data=configs)

    # @expose("/pos_config/<int:id>")
    # def pos_config(self,id):
    #     pos_config_schema = schemas.PosConfigSchema()
    #     pos_config = db.session.query(models.PosConfig).get(id)
    #     if not pos_config:
    #         return self.response(404)
    #     result = pos_config_schema.dump(pos_config)
    #     return self.response(200, data=result)

    # @expose("/pos_session")
    # def pos_sessions(self):
    #     pass 

    # @expose("/pos_session/<int:id>")
    # def pos_sessions(self):
    #     pass 

    # @expose("/pos_session/active")
    # def pos_sessions(self):
    #     pass 

    # @expose("/pos_session/<int:id>")
    # def pos_sessions(self):
    #     pass 

    # @expose("/pos_order", methods=['GET'])
    # def pos_orders(self):
    #     pos_order_schema = schemas.PosOrderSchema(many=True)
    #     pos_orders = db.session.query(models.PosOrder).all()
    #     if not pos_orders:
    #         return self.response(404)
    #     result = pos_order_schema.dump(pos_orders)
    #     return self.response(200, data=result)

    # @expose("/pos_order/<int:id>")
    # def pos_order(self, id):
    #     pos_order_schema = schemas.PosOrderSchema()
    #     pos_order = db.session.query(models.PosOrder).get(id)
    #     if not pos_order:
    #         return self.response(404)
    #     result = pos_order_schema.dump(pos_order)
    #     return self.response(200, data=result)

    # @expose("/pos_order", methods=['POST'])
    # def pos_order_create(self):
    #     pos_order_schema = schemas.PosOrderSchema()
    #     pos_order = models.PosOrder()
    #     if not pos_order:
    #         return self.response(404)
    #     result = pos_order_schema.dump(pos_order)
    #     return self.response(200, data=result)

class ProductModelApi(ModelRestApi):
    resource_name = "product"
    datamodel = SQLAInterface(models.ProductProduct)
    exclude_route_methods = ("put")

class PosConfigModelApi(ModelRestApi):
    resource_name = "pos_config"
    datamodel = SQLAInterface(models.PosConfig)

class PosSessionModelApi(ModelRestApi):
    resource_name = "pos_session"
    datamodel = SQLAInterface(models.PosSession)
    search_columns = ['company_id','config_id','user_id','state']

    @expose("/by-payment-method/<int:pos_session_id>/<int:pos_payment_method_id>", methods=['GET'])
    def by_payment_method(self, pos_session_id, pos_payment_method_id):
      pos_session = db.session.query(models.PosSession).get(pos_session_id)
      #print(pos_order.sum_amount_total())
      result = {
        "amount_total": pos_session.total_by_pos_payment_method(pos_payment_method_id)
      }
      return self.response(200, data=result)

    @expose("/closed/<int:pos_session_id>", methods=['GET'])
    def pos_session_closed(self, pos_session_id):
      pos_session = db.session.query(models.PosSession).get(pos_session_id)    
      if pos_session:
        pos_session.session_closed()  
        return self.response(200, data={})
      else:
        return self.response(404, data={})


class PosOrderModelApi(ModelRestApi):
    resource_name = "pos_order"
    datamodel = SQLAInterface(models.PosOrder)
    search_columns = ['pos_session_id', 'state']


    @expose("/summary/<int:pos_order_id>")
    def order_summary(self, pos_order_id):
      pos_order = db.session.query(models.PosOrder).get(pos_order_id)
      #print(pos_order.sum_amount_total())
      result = {
        "total_order_line": pos_order.total_orderline(),
        "total_payment": pos_order.total_payment()
      }
      return self.response(200, data=result)
    
class PosOrderLineModelApi(ModelRestApi):
    resource_name = 'pos_order_line'
    datamodel = SQLAInterface(models.PosOrderLine)
    add_columns = ['company_id', 'order_id', 'name', 'notice', 'product_id', 'price_unit', 'qty', 'price_subtotal', 'price_subtotal_incl','discount', 'product_uom_id','currency_id', 'tax_id']
    search_columns = ['order_id']


class PosPaymentModelApi(ModelRestApi):
    resource_name = 'pos_payment'
    datamodel = SQLAInterface(models.PosPayment)
    search_columns = ['pos_order_id']
  

appbuilder.add_api(ExampleApi)
#appbuilder.add_api(PosApi)
appbuilder.add_api(ProductModelApi)
appbuilder.add_api(PosConfigModelApi)
appbuilder.add_api(PosSessionModelApi)
appbuilder.add_api(PosOrderModelApi)
appbuilder.add_api(PosOrderLineModelApi)
appbuilder.add_api(PosPaymentModelApi)
