from openerp.osv import fields, osv

class product_category(osv.osv):
    _inherit = 'product.category'
    _columns = {
        'isProductVisible': fields.boolean('Visible', help="Displayed on website"),
        'categoryImage': fields.text("Category Image",help="This field holds the image path for product category"),
        'isMainCategory': fields.boolean('isMainCategory', help="This field indicates main category"),
        'hasSubCategory': fields.boolean('hasSubCategory', help="This field indicates that category has subcategories"),
        'detailPage': fields.text("Detail Page",help="This field holds the detail page url"),
        'attachment_ids': fields.many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments'),
    }
    
class product_template(osv.osv):
    _inherit = 'product.template'
    _columns = {
        'article': fields.float('Article', help="Article of the product"),
    }