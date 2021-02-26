from flask import render_template, redirect, make_response, send_file
from flask_appbuilder.actions import action
from flask_appbuilder import BaseView, expose, ModelView, IndexView, CompactCRUDMixin
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import MasterDetailView
from flask_appbuilder.widgets import (
    ListWidget, ListBlock, ListItem, ListLinkWidget, ListThumbnail, ShowBlockWidget, ShowWidget
)


from flask_babel import lazy_gettext as _

from reportlab.pdfgen import canvas

from fpdf import FPDF, Template
import sys

from . import appbuilder, db
from .models import (
    Contact, ContactGroup, Gender, PosConfig, PosSession, PosOrder, PosOrderLine,
    PosPayment, PosCategory, ProductProduct, Company, PosPaymentMethod, PosSessionPayment,
    IrSequence
)

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )

def fill_gender():
    try:
        db.session.add(Gender(name="Male"))
        db.session.add(Gender(name="Female"))
        db.session.commit()
    except Exception:
        db.session.rollback()




class ReportView(BaseView):
    route_base = "/report"

    @expose("/report01")
    def report01(self):
        # try:
        #     from StringIO import StringIO ## for Python 2
        # except ImportError:
        #     from io import StringIO ## for Python 3
        # output = StringIO()

        # p = canvas.Canvas(output)
        # p.drawString(100, 100, 'Hello')
        # p.showPage()
        # p.save()
        
        # pdf_out = output.getvalue()
        # output.close()

        # response = make_response(pdf_out)
        # response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
        # response.mimetype = 'application/pdf'
        # return response

        pdf = FPDF()
        # compression is not yet supported in py3k version
        pdf.compress = False
        pdf.add_page()
        # Unicode is not yet supported in the py3k version; use windows-1252 standard font
        pdf.set_font('Arial', '', 14)  
        pdf.ln(10)
        pdf.write(5, 'hello world %s áéíóúüñ' % sys.version)
        #pdf.image("pyfpdf/tutorial/logo.png", 50, 50)
        pdf.output('/tmp/py3k.pdf', 'F')
        return send_file('/tmp/py3k.pdf', mimetype='application/pdf')

    @expose("/report02")
    def report02(self):
        #this will define the ELEMENTS that will compose the template. 
        elements = [
            { 'name': 'company_name', 'type': 'T', 'x1': 17.0, 'y1': 32.5, 'x2': 115.0, 'y2': 37.5, 'font': 'Arial', 'size': 12.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
            { 'name': 'box', 'type': 'B', 'x1': 15.0, 'y1': 15.0, 'x2': 185.0, 'y2': 260.0, 'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 0, },
            { 'name': 'box_x', 'type': 'B', 'x1': 95.0, 'y1': 15.0, 'x2': 105.0, 'y2': 25.0, 'font': 'Arial', 'size': 0.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 2, },
            { 'name': 'line1', 'type': 'L', 'x1': 100.0, 'y1': 25.0, 'x2': 100.0, 'y2': 57.0, 'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
            { 'name': 'barcode', 'type': 'BC', 'x1': 20.0, 'y1': 246.5, 'x2': 140.0, 'y2': 254.0, 'font': 'Interleaved 2of5 NT', 'size': 0.75, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '200000000001000159053338016581200810081', 'priority': 3, },
        ]

        #here we instantiate the template and define the HEADER
        f = Template(format="A4", elements=elements,
                    title="Sample Invoice")
        f.add_page()

        #we FILL some of the fields of the template with the information we want
        #note we access the elements treating the template instance as a "dict"
        f["company_name"] = "Sample Company"
        #f["company_logo"] = "pyfpdf/tutorial/logo.png"

        #and now we render the page
        #f.render("/tmp/template.pdf")
        f.render('/tmp/template.pdf')
        return send_file('/tmp/template.pdf', mimetype='application/pdf')
    
    @expose("/report03")
    def report03(self):
        # Create instance of FPDF class
        # Letter size paper, use inches as unit of measure
        pdf=FPDF(format='letter', unit='in')
        
        # Add new page. Without this you cannot create the document.
        pdf.add_page()
        
        # Remember to always put one of these at least once.
        pdf.set_font('Times','',10.0) 
        
        # Effective page width, or just epw
        epw = pdf.w - 2*pdf.l_margin
        
        # Set column width to 1/4 of effective page width to distribute content 
        # evenly across table and page
        col_width = epw/4
        
        # Since we do not need to draw lines anymore, there is no need to separate
        # headers from data matrix.
        
        data = [['First name','Last name','Age','City'],
        ['Jules','Smith',34,'San Juan'],
        ['Mary','Ramos',45,'Orlando'],[
        'Carlson','Banks',19,'Los Angeles']
        ]
        
        # Document title centered, 'B'old, 14 pt
        pdf.set_font('Times','B',14.0) 
        pdf.cell(epw, 0.0, 'Demographic data', align='C')
        pdf.set_font('Times','',10.0) 
        pdf.ln(0.5)
        
        # Text height is the same as current font size
        th = pdf.font_size
        
        for row in data:
            for datum in row:
                # Enter data in colums
                # Notice the use of the function str to coerce any input to the 
                # string type. This is needed
                # since pyFPDF expects a string, not a number.
                pdf.cell(col_width, th, str(datum), border=1)
        
            pdf.ln(th)
        
        # Line break equivalent to 4 lines
        pdf.ln(4*th)
        
        pdf.set_font('Times','B',14.0) 
        pdf.cell(epw, 0.0, 'With more padding', align='C')
        pdf.set_font('Times','',10.0) 
        pdf.ln(0.5)
        
        # Here we add more padding by passing 2*th as height
        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
        
        pdf.output('/tmp/table-using-cell-borders.pdf','F')
        return send_file('/tmp/table-using-cell-borders.pdf', mimetype='application/pdf')
        
class WehaWidgetList(ListWidget):

    template = '/general/widgets/list.html'

class WehaWidgetShow(ShowWidget):

    template = '/general/widgets/show.html'

class AdminLteModelView(ModelView):
    list_template = 'list.html'
    list_widget = WehaWidgetList
    can_delete = True

class ContactGeneralView(AdminLteModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {"contact_group": "Contacts Group"}
    list_columns = ["name", "personal_phone", "contact_group"]

    base_order = ("name", "asc")

    show_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": False,
            },
        ),
    ]

class GroupMasterView(MasterDetailView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactGeneralView]

class GroupGeneralView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactGeneralView]

class CompanyModelView(AdminLteModelView):
    datamodel = SQLAInterface(Company)

class IrSequenceView(AdminLteModelView):
    datamodel = SQLAInterface(IrSequence)
    list_columns = ["name", "prefix", "suffix", "padding", "next_number", "step"]

class PosCategoryView(AdminLteModelView):
    datamodel = SQLAInterface(PosCategory)
    list_columns = ["name"]
    
class ProductProductView(AdminLteModelView):
    datamodel = SQLAInterface(ProductProduct)
    list_columns = ["display_name","lst_price","standard_price", "pos_category"]

class PosConfigView(ModelView):
    datamodel = SQLAInterface(PosConfig)
    list_columns = ["name", "company"]

    def pre_add(self, item):
        item.currency_id = 1

    @action("printaction","Print","Do you really want to?","fa-rocket")
    def printaction(self, item):
        """
            do something with the item record
        """
        return redirect(self.get_redirect())

    @action("emailaction","Email","Do you really want to?","fa-rocket")
    def emailaction(self, item):
        """
            do something with the item record
        """
        return redirect(self.get_redirect())

class PosPaymentMethodView(AdminLteModelView):
    datamodel = SQLAInterface(PosPaymentMethod)
    list_columns = ["name"]

class PosSessionPaymentView(AdminLteModelView):
    datamodel = SQLAInterface(PosSessionPayment)
    list_columns = ['pos_payment_method_id', 'amount']

class PosSessionView(AdminLteModelView):
    datamodel = SQLAInterface(PosSession)
    related_views = [PosSessionPaymentView]
    show_template = 'general/model/show_cascade.html'
    list_columns = ["name", "session_date", "config", "user", "state"]
    order_columns = ["name","config"]
    order_rel_fields = {'config': ('name', 'asc')}
    show_fieldsets = [
        (
            "General", 
                {
                    "fields": [
                        "name",
                        "session_date",
                        "config",
                        "user",
                        "state",
                        "creation_date"
                    ]
                }
        )
    ]

class PosOrderLineView(AdminLteModelView):
    datamodel = SQLAInterface(PosOrderLine)
    list_columns = ["name", "qty", "price_unit", "amount_paid"]

class PosOrderInlineView(CompactCRUDMixin, AdminLteModelView):
    datamodel = SQLAInterface(PosOrderLine)
    list_columns = ["name", "qty", "price_unit", "amount_paid"]

class PosPaymentView(AdminLteModelView):
    datamodel = SQLAInterface(PosPayment)
    list_columns = ["name", "amount"]
    can_create = False
    can_delete = False
    can_edit = False

class PosOrderView(AdminLteModelView):
    datamodel = SQLAInterface(PosOrder)
    related_views = [PosOrderLineView, PosPaymentView]
    
    list_columns = ['name','pos_session','sum_amount_total','state']
    order_columns = ['name','sum_maount_total','state']
    
    #show_template = 'appbuilder/general/model/show_cascade.html'
    show_template = 'general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'

    show_fieldsets = [
        (
            "General", 
                {
                    "fields": [
                        "name",
                        "pos_session",
                        "user",
                        "state"
                    ]
                }
        ),
        (
            "Amount",
            {
                "fields": [
                    "amount_paid",
                    "amount_total",
                    "amount_tax",
                    "amount_return",
                ],
                "expanded": False,
            },
        ),
    ]

fixed_translations_import = [
    _("List Groups"),
    _("Manage Groups"),
    _("List Contacts"),
    _("Contacts Chart"),
    _("Contacts Birth Chart"),
]

db.create_all()
fill_gender()

appbuilder.add_view(
    GroupMasterView, "List Groups", icon="fa-folder-open-o", category="Contacts"
)
appbuilder.add_separator("Contacts")
appbuilder.add_view(
    GroupGeneralView, "Manage Groups", icon="fa-folder-open-o", category="Contacts"
)
appbuilder.add_view(
    ContactGeneralView, "List Contacts", icon="fa-envelope", category="Contacts"
)

appbuilder.add_view(
    PosCategoryView, "Categories", icon="fa-envelope", category="Master"
)

appbuilder.add_view(
    ProductProductView, "Products", icon="fa-envelope", category="Master"
)

appbuilder.add_view(
    PosConfigView, "Configs", icon="fa-desktop", category="Point of Sale"
)
appbuilder.add_view(
    PosPaymentMethodView, "Payment Method", icon="fa-desktop", category="Point of Sale"
)
appbuilder.add_view(
    PosSessionView, "Sessions", icon="fa-gears", category="Point of Sale"
)

appbuilder.add_view(
    PosOrderView, "Orders", icon="fa-cart-plus", category="Point of Sale"
)
appbuilder.add_view(
    PosOrderLineView, "Order Lines", icon="fa-envelope", category="Point of Sale"
)
appbuilder.add_view(
    PosPaymentView, "Payments", icon="fa-envelope", category="Point of Sale"
)
appbuilder.add_view(CompanyModelView, "Companys", icon="fa-folder-open-o", category="Settings")
appbuilder.add_view(IrSequenceView, "Sequence", icon="fa-folder-open-o", category="Settings")


appbuilder.add_view_no_menu(ReportView())