from openerp.osv import fields, osv

class cases_category(osv.osv):
    _name = 'case.category'
    _description = 'Cases Category'
    _inherit = ['mail.thread', 'website.seo.metadata']
    _order = 'name'
    _columns = {
        'name': fields.char('Case Name', required=True),
        'description': fields.text('Description'),
    }

class cases_post(osv.osv):
    _name = "case.post"
    _description = "Case Post"
    _inherit = ['mail.thread', 'website.seo.metadata']
    _order = 'id DESC'
    _columns = {
        'name': fields.char('Title', required=True, translate=True),
        'company': fields.char('Company'),
        'description': fields.text('Description'),
        'important_case': fields.boolean('Important Case', help="Publish on the website"),
        'author_id': fields.many2one('res.partner', 'Author'),
        'case_cat_id': fields.many2one(
            'case.category', 'Category',
            required=True, ondelete='cascade',
        ),
        'tag_ids': fields.many2many(
            'product.category', string='Product',
        ),
        'content': fields.html('Case Content', translate=True, sanitize=False),
        'content_decision': fields.html('Decision Content', translate=True, sanitize=False),

        'website_published': fields.boolean(
            'Publish', help="Publish on the website", copy=False,
        ),
        'website_message_ids': fields.one2many(
            'mail.message', 'res_id',
            domain=lambda self: [
                '&', '&', ('model', '=', self._name), ('type', '=', 'comment'), ('path', '=', False)
            ],
            string='Website Messages',
            help="Website communication history",
        ),
        'history_ids': fields.one2many(
            'blog.post.history', 'post_id',
            'History', help='Last post modifications',
        ),
        # creation / update stuff
        'create_date': fields.datetime(
            'Created on',
            select=True, readonly=True,
        ),
        'create_uid': fields.many2one(
            'res.users', 'Author',
            select=True, readonly=True,
        ),
        'write_date': fields.datetime(
            'Last Modified on',
            select=True, readonly=True,
        ),
        'write_uid': fields.many2one(
            'res.users', 'Last Contributor',
            select=True, readonly=True,
        ),
        'visits': fields.integer('No of Views'),
        'decision_attachment_ids': fields.many2many('ir.attachment', 'decision_class_ir_attachments_rel', 'decision_class_id', 'attachment_id', 'Decision Attachments'),
        'cases_attachment_ids': fields.many2many('ir.attachment', 'cases_class_ir_attachments_rel', 'case_class_id', 'attachment_id', 'Cases Attachments'),
    }