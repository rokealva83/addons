from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp.osv.orm import except_orm
from openerp.tools.translate import _

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _columns = {
        'position' : fields.char('Position', size=128),
        'need_answer' : fields.char('Need Answer', size=128),
        'interested_category' : fields.char('Interested Category', size=128),
    }
class ir_attachment(osv.osv):
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'

    def check(self, cr, uid, ids, mode, context=None, values=None):
        """Restricts the access to an ir.attachment, according to referred model
        In the 'document' module, it is overriden to relax this hard rule, since
        more complex ones apply there.
        """
        res_ids = {}
        require_employee = False
        if ids:
            if isinstance(ids, (int, long)):
                ids = [ids]
            cr.execute('SELECT DISTINCT res_model, res_id, create_uid FROM ir_attachment WHERE id = ANY (%s)', (ids,))
            for rmod, rid, create_uid in cr.fetchall():
                if not (rmod and rid):
                    if create_uid != uid:
                        require_employee = True
                    continue
                res_ids.setdefault(rmod,set()).add(rid)
        if values:
            if values.get('res_model') and values.get('res_id'):
                res_ids.setdefault(values['res_model'],set()).add(values['res_id'])

        ima = self.pool.get('ir.model.access')
        for model, mids in res_ids.items():
            # ignore attachments that are not attached to a resource anymore when checking access rights
            # (resource was deleted but attachment was not)
            if not self.pool.get(model):
                require_employee = True
                continue
            existing_ids = self.pool[model].exists(cr, uid, mids)
            if len(existing_ids) != len(mids):
                require_employee = True
            ima.check(cr, uid, model, mode)
            self.pool[model].check_access_rule(cr, uid, existing_ids, mode, context=context)

        # ----add from Surekha technology-----------
        # comment this code to give download permission to the users publicly......
        '''
        if require_employee:
            if not self.pool['res.users'].has_group(cr, uid, 'base.group_public'):
                raise except_orm(_('Access Denied'), _("Sorry, you are not allowed to access this document."))
                '''



