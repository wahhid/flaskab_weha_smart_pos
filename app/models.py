from flask import g
from sqlalchemy import func
from sqlalchemy.sql.elements import Label
from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.models.mixins import BaseMixin
from sqlalchemy import Table, Column, Date, ForeignKey, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app import db
from datetime import datetime, date


def get_user_id():
    try:
        return g.user.id
    except Exception:
        return None


class IrSequence(BaseMixin, Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    prefix = Column(String(200))
    suffix = Column(String(200))
    padding = Column(Integer, nullable=False)
    next_number = Column(Integer, nullable=False, default=1)
    step = Column(Integer,  nullable=False, default=1)

    def get_next_number_by_name(self):
        sequence = self.prefix + str(self.next_number).zfill(self.padding)
        self.next_number = self.next_number + 1
        db.session.commit()
        return sequence

    def get_next_number_by_id(self):
        pass 

class ContactGroup(BaseMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Gender(BaseMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class Contact(BaseMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey("gender.id"), nullable=False)
    gender = relationship("Gender")

    def __repr__(self):
        return self.name

class Company(BaseMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class WehaUser(User):
    __tablename__ = "ab_user"
    company_id = Column(Integer, ForeignKey("company.id"), nullable=True)
    company = relationship("Company")

class PosCategory(BaseMixin, Model):
    __tablename__ = 'pos_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return self.name

class ProductProduct(BaseMixin, Model):
    __tablename__ = 'product_product'

    id = Column(Integer, primary_key=True)
    display_name = Column(String(255))
    lst_price = Column(Float)
    standard_price = Column(Float)
    categ_id = Column(Integer)
    pos_categ_id = Column(Integer, ForeignKey("pos_category.id"), nullable=False)
    pos_category = relationship("PosCategory")
    taxes_id = Column(Integer)
    barcode = Column(String(20))
    default_code = Column(String(20))
    to_weight = Column(Boolean)
    uom_id = Column(Integer)
    description_sale = Column(String(255))
    description = Column(String(255))
    product_tmpl_id = Column(Integer)
    tracking = Column(String(20))
    image_1920 = Column(String())

    def __repr__(self):
        return self.display_name

assoc_pos_config_pos_payment_method = Table(
    "pos_config_pos_payment_method",
    Model.metadata,
    Column("id", Integer, primary_key=True),
    Column("pos_config_id", Integer, ForeignKey("pos_config.id")),
    Column("pos_payment_method_id", Integer, ForeignKey("pos_payment_method.id")),
)


class PosConfig(BaseMixin, Model):
    __tablename__ = 'pos_config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(5), unique=True)
    currency_id = Column(Integer)
    pricelist_id = Column(Integer)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=True)
    company = relationship("Company")
    pos_payment_methods = relationship(
        "PosPaymentMethod", secondary=assoc_pos_config_pos_payment_method, backref="pos_config"
    )

    def __repr__(self):
        return self.name


class PosSession(BaseMixin, Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    session_date = Column(Date, default=date.today())
    config_id = Column(Integer, ForeignKey("pos_config.id"), nullable=False)
    config = relationship("PosConfig")
    company_id = Column(Integer)
    currency_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("ab_user.id"), nullable=False)
    user = relationship("User")
    state = Column(String(20), default='active')
    creation_date = Column(DateTime, default=datetime.now())
    
    def __repr__(self):
        return self.name

    # def __init__(self, email):
    #     super(PosSession, self).__init__()
    #     sequence = db.session.query(IrSequence).filter_by(name="Session Sequence").first()
    #     self.name = sequence.get_next_number_by_name()

    # @classmethod
    # def create(cls, **kw):
    #     print("Create Pos Session")
    #     obj = cls(**kw)
    #     sequence = db.session.query(IrSequence).filter_by(name="Session Sequence").first()
    #     obj.name = sequence.get_next_number_by_name()
    #     db.session.add(obj)
    #     db.session.commit()

    def session_closed(self):
        pos_payment_methods = db.session.query(PosPaymentMethod).all()
        for pos_payment_method in pos_payment_methods:
            pos_session_payment = PosSessionPayment()
            pos_session_payment.pos_session_id = self.id
            pos_session_payment.pos_payment_method_id = pos_payment_method.id
            pos_session_payment.amount_total = self.total_by_pos_payment_method(pos_payment_method.id)
            db.session.add(pos_payment_method)
            db.session.commit()
        self.state = 'closed'
        db.session.commit()



    def total_by_pos_payment_method(self, pos_payment_method_id):
        result = db.session.query(Label('amount_total', func.sum(PosPayment.amount))).join(PosOrder).group_by(PosOrder.pos_session_id).first()
        if result:
            return result.amount_total
        else:
            return 0.0

    def total_amount(self):
        # Put your query here
        result = db.session.query(
            Label('amount_total', func.sum(PosOrder.amount_total))).group_by(PosSession.id).filter_by(pos_session_id=self.id).first()
        if result:
            return result.amount_total
        else:
            return 0.0
            
class PosSessionPayment(BaseMixin, Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pos_session_id = Column(Integer, ForeignKey("pos_session.id"), nullable=True)
    pos_session  = relationship("PosSession")
    pos_payment_method_id = Column(Integer, ForeignKey("pos_payment_method.id"), nullable=False)
    pos_payment_method =relationship("PosPaymentMethod")
    amount_total = Column(Float)


class PosOrder(BaseMixin, Model):
    __tablename__ = 'pos_order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    amount_paid = Column(Float)
    amount_total = Column(Float)
    amount_tax = Column(Float)
    amount_return = Column(Float)
    pos_session_id = Column(Integer, ForeignKey("pos_session.id"), nullable=True)
    pos_session  = relationship("PosSession")
    pricelist_id = Column(Integer)
    partner_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("ab_user.id"), nullable=True)
    user  = relationship("User")
    employee_id = Column(Integer)
    uid = Column(Integer)
    sequence_number = Column(Integer)
    creation_date = Column(DateTime)
    fiscal_position_id = Column(Integer)
    server_id = Column(Integer)
    to_invoice = Column(Boolean)
    state = Column(String(50), default='unpaid')

    def __repr__(self):
        return self.name

    def total_orderline(self):
        # Put your query here
        result = db.session.query(
          PosOrderLine.order_id,
          Label('amount_total', func.sum(PosOrderLine.price_subtotal))).group_by(PosOrderLine.order_id).filter_by(order_id=self.id).first()
        if result:
            return result.amount_total
        else:
            return 0.0

    def total_payment(self):
        # Put your query here
        result = db.session.query(
          PosPayment.pos_order_id,
          Label('amount_total', func.sum(PosPayment.amount))).group_by(PosPayment.pos_order_id).filter_by(pos_order_id=self.id).first()
        if result:
            return result.amount_total
        else:
            return 0.0

class PosOrderLine(BaseMixin, Model):
    __tablename__ = 'pos_order_line'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer)
    name = Column(String(255))
    notice = Column(String(255))
    product_id = Column(Integer, ForeignKey("product_product.id"), nullable=True)
    product  = relationship("ProductProduct")
    price_unit = Column(Float)
    qty = Column(Float)
    price_subtotal = Column(Float)
    price_subtotal_incl = Column(Float)
    discount = Column(Float)
    order_id = Column(Integer, ForeignKey("pos_order.id"), nullable=False)
    order = relationship("PosOrder")
    product_uom_id = Column(Integer)
    currency_id = Column(Integer)
    tax_id = Column(Integer)

class PosPayment(BaseMixin, Model):
    __tablename__ = 'pos_payment'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    amount = Column(Float)
    pos_order_id = Column(Integer, ForeignKey("pos_order.id"), nullable=False)
    order = relationship("PosOrder")
    payment_method_id = Column(Integer, ForeignKey("pos_payment_method.id"), nullable=False)
    pos_payment_method =relationship("PosPaymentMethod")
    session_id = Column(Integer)
    
class PosPaymentMethod(BaseMixin, Model):
    __tablename__ = 'pos_payment_method'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    
    def __repr__(self):
        return self.name