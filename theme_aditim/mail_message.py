from openerp.osv import fields, osv

class mail_message(osv.osv):
    _inherit = 'mail.message'
    _columns = {
        'comment_text' : fields.text('comment_text', help="Body of the comment"),
        'organization_name': fields.text('Organization', help="Name of the organization"),
        'city': fields.text('city', help="City of the person which put the comment"),
    }