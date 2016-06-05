from openerp.osv import fields, osv


class blog_post(osv.osv):
    _inherit = 'blog.post'
    _columns = {
        'displayAsCase': fields.boolean('Display As Case', help="Field for displaying blog as case"),
        'blogPostImage': fields.binary('Blog Post Image', help="Field for the blog image"),
        'description': fields.text('Description', help="Field for intial short description"),
    }