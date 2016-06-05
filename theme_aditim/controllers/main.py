##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (c) 2012 OpenERP S.A. <http://openerp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.http import Controller, route, request
from werkzeug.utils import redirect
from openerp.addons.website.models.website import slug
from openerp import SUPERUSER_ID
import random
import json
import openerp
from openerp.addons.web.controllers.main import WebClient
from openerp.addons.web import http
from openerp.http import request, STATIC_CACHE
from openerp.tools import image_save_for_web
import cStringIO
from PIL import Image

class aditimControllers(Controller):
    _blog_post_per_page = 5
    _case_post_per_page = 4
    _super_user = 1
    
    @route("/page/product_page", auth="public", website=True)
    def getProductCategoryData(self):
        
        product_env = request.env['product.category']
        product_cat_ids = product_env.search([('isProductVisible', '=', True)])
        product_with_subcategory = product_env.search([('hasSubCategory', '=', True)])
        product_subcategory_ids = product_env.search([('parent_id', '=', product_with_subcategory[0].id)])
        values = {
                  'productCategories': product_cat_ids,
                  'product_subcategory_ids': product_subcategory_ids
                }
        
        return request.website.render('theme_aditim.product_page', values)
    
    @route("/page/product_interior_page", auth="public", website=True)
    def getProductDetailData(self):
        return request.website.render('theme_aditim.product_interior_page', {})
    
    @route("/page/product_interior_page/<model('product.category'):product_category>", auth="public", website=True)
    def getProductDetailDataByCategory(self, product_category):
        cr, uid, context = request.cr, self._super_user, request.context
        linkToPage = product_category[0].detailPage
        product_category_id = product_category[0].id
        product_related_cases = [];
        case_post_env = request.registry['case.post']
        case_post_ids = case_post_env.search(cr, uid, [('website_published','=',True)], context=context)
        published_case_posts = case_post_env.browse(cr, uid, case_post_ids, context=context)

        for cases in published_case_posts:
            for product_tag in cases.tag_ids:
                if product_category_id == product_tag.id:
                    product_related_cases.append(cases);
        
        if len(product_related_cases) > 3 :
            three_cases_ids = random.sample(product_related_cases, 3)
        else:
            three_cases_ids = product_related_cases

        product_template_env = request.env['product.template']
        product_prod_env = request.env['product.product']
        products_by_category = product_template_env.search([('categ_id', '=', product_category_id)])
        
        product_attributes = [];
        for prod_tmpl_ids in products_by_category:
            products_product_ids = product_prod_env.search([('product_tmpl_id', '=', prod_tmpl_ids.id)])
            for prod_prod_ids in products_product_ids:
                for attribute_value in prod_prod_ids.attribute_value_ids:
                    if attribute_value not in product_attributes:
                        product_attributes.append(attribute_value);
        
        values = {
                  'productsBycategory': products_by_category,
                  'product_attributes': product_attributes,
                  'three_cases': three_cases_ids,
                  'product_category': product_category,
                }
        return request.website.render(linkToPage, values)
    
    @route("/page/main_home_page", auth="public", website=True)
    def getMainPageData(self):
        cr, uid, context = request.cr, self._super_user, request.context
        
        product_env = request.env['product.category']
        product_main_categories = product_env.search([('isMainCategory', '=', True)])

        blog_env = request.registry['blog.post']
        latest_blog_ids = blog_env.search(cr, uid,[('displayAsCase', '=', False),('website_published','=',True)], offset=0, limit=2, context=context)
        latest_blog = blog_env.browse(cr, uid, latest_blog_ids, context=context)
        
        case_env = request.registry['case.post']
        case_posts_ids = case_env.search(cr, uid,[('website_published','=',True)], offset=0, limit=1, context=context)
        case_posts = case_env.browse(cr, uid, case_posts_ids, context=context)
        
        values = {
                  'productMainCategories': product_main_categories,
                  'case_post': case_posts,
                  'latest_blog': latest_blog,
                }
        return request.website.render('theme_aditim.main_home_page', values)
    
    @route(['/page/theme_aditim.product_profiles_polyethylene',
            '/page/theme_aditim.product_accessories_for_spacer',
            '/page/theme_aditim.product_polyamide_profile_timberal',
            '/page/theme_aditim.product_insulation_profile_timberal',
            '/page/theme_aditim.product_TPV_foam_sealants'] ,type='http', auth="public", website=True)
    def getProductByCategory(self):
        currentPath = request.httprequest.path
        pageToRedirect = currentPath.replace('/page/','')
        cr, uid, context = request.cr, self._super_user, request.context

        product_env = request.env['product.category']
        product_cat_ids = product_env.search([('detailPage', '=', pageToRedirect)])

        product_template_env = request.env['product.template']
        product_prod_env = request.env['product.product']
        
        product_related_cases = [];
        case_post_env = request.registry['case.post']
        case_post_ids = case_post_env.search(cr, uid, [('website_published','=',True)], context=context)
        published_case_posts = case_post_env.browse(cr, uid, case_post_ids, context=context)

        for cases in published_case_posts:
            for product_tag in cases.tag_ids:
                if product_cat_ids.id == product_tag.id:
                    product_related_cases.append(cases);
        
        if len(product_related_cases) > 3 :
            three_cases_ids = random.sample(product_related_cases, 3)
        else:
            three_cases_ids = product_related_cases

        products_by_category = product_template_env.search([('categ_id', '=', product_cat_ids[0].id)])
        product_attributes = [];
            
        for prod_tmpl_ids in products_by_category:
            products_product_ids = product_prod_env.search([('product_tmpl_id', '=', prod_tmpl_ids.id)])
            for prod_prod_ids in products_product_ids:
                for attribute_value in prod_prod_ids.attribute_value_ids:
                    if attribute_value not in product_attributes:
                        product_attributes.append(attribute_value);
        
        values = {
                  'productsBycategory': products_by_category,
                  'product_attributes': product_attributes,
                  'three_cases': three_cases_ids,
                  'product_category': product_cat_ids,
                }
        return request.website.render(pageToRedirect,values)
    
    @route("/page/product/<model('product.category'):product_category>/<model('product.attribute.value'):pro_att_value>" ,type='http', auth="public", website=True)
    def getProductByAttributeValue(self, pro_att_value,product_category):
        cr, uid, context = request.cr, self._super_user, request.context
        product_template_env = request.env['product.template']
        
        products_by_attribute = [];        
        products = pro_att_value.product_ids
        for prod in products:
            products_to_display = product_template_env.search([('id', '=', prod.product_tmpl_id.id)])
            for p in products_to_display:
                if p.categ_id.id == product_category.id:
                    products_by_attribute.append(p);
                
        pageToRedirect = product_category.detailPage
        
        product_related_cases = [];
        case_post_env = request.registry['case.post']
        case_post_ids = case_post_env.search(cr, uid, [('website_published','=',True)], context=context)
        published_case_posts = case_post_env.browse(cr, uid, case_post_ids, context=context)
        
        for cases in published_case_posts:
            for product_tag in cases.tag_ids:
                if product_category.id == product_tag.id:
                    product_related_cases.append(cases);
                    
        if len(product_related_cases) > 3 :
            three_cases_ids = random.sample(product_related_cases, 3)
        else:
            three_cases_ids = product_related_cases
        
        product_prod_env = request.env['product.product']
        products_by_category = product_template_env.search([('categ_id', '=', product_category.id)])
        
        product_attributes = [];
        for prod_tmpl_ids in products_by_category:
            products_product_ids = product_prod_env.search([('product_tmpl_id', '=', prod_tmpl_ids.id)])
            for prod_prod_ids in products_product_ids:
                for attribute_value in prod_prod_ids.attribute_value_ids:
                    if attribute_value not in product_attributes:
                        product_attributes.append(attribute_value);
        
        values = {
                  'productsBycategory': products_by_attribute,
                  'product_attributes': product_attributes,
                  'three_cases': three_cases_ids,
                  'product_category': product_category,
                  'product_attr' : pro_att_value,
                }
        return request.website.render(pageToRedirect,values)
    
    @route(['/page/theme_aditim.blog_aggregator_page',
            '/page/theme_aditim.blog_aggregator_page/page/<int:page>'], type='http', auth="public", website=True)
    def getBlogPostData(self, page=1):
        cr, uid, context = request.cr, self._super_user, request.context
        
        blog_post_env = request.registry['blog.post']
        blog_tags_env = request.registry['blog.tag']

        if request.session.uid:
            total = len(blog_post_env.search(cr, uid, [], context=context))
            blog_post_ids = blog_post_env.search(cr, uid, [], offset=(page-1)*self._blog_post_per_page, limit=self._blog_post_per_page, context=context)
        else:
            total = len(blog_post_env.search(cr, uid, [('website_published','=',True)], context=context))
            blog_post_ids = blog_post_env.search(cr, uid, [('website_published','=',True)], offset=(page-1)*self._blog_post_per_page, limit=self._blog_post_per_page, context=context)

        blog_posts = blog_post_env.browse(cr, uid, blog_post_ids, context=context)

        blog_tag_ids = blog_tags_env.search(cr, uid, [], context=context)
        blog_tags = blog_tags_env.browse(cr, uid, blog_tag_ids, context=context)
        
        p_blogs_ids = blog_post_env.search(cr, uid, [('displayAsCase', '=', False), ('website_published','=',True)], order='visits', context=context)
        p_blogs = blog_post_env.browse(cr, uid, p_blogs_ids, context=context)
        popular_blogs = tuple(reversed(p_blogs))
        
        pager = request.website.pager(
            url='/page/theme_aditim.blog_aggregator_page',
            total=total,
            page=page,
            step=self._blog_post_per_page,
        )
        values = {
                  'pager': pager,
                  'blog_tags': blog_tags,
                  'all_blog_posts': blog_posts,
                  'popular_blogs' : popular_blogs[0:3],
                }
        return request.website.render('theme_aditim.blog_aggregator_page', values)
    
    @route(['/page/tag/<model("blog.tag"):blog_tag>',
            '/page/tag/<model("blog.tag"):blog_tag>/page/<int:page>'], type='http', auth="public", website=True)
    def getBlogDataByTag(self, blog_tag, page=1):
        cr, uid, context = request.cr, self._super_user, request.context
        
        blog_post_env = request.registry['blog.post']
        blog_tags_env = request.registry['blog.tag']
        
        blogs_related_to_tags = blog_tag.post_ids
        total = len(blogs_related_to_tags) 
        blog_ids = [];
        for p_id in blogs_related_to_tags:
                blog_ids.append(p_id.id);
        
        blog_posts = blog_post_env.browse(cr, uid, blog_ids[(0+((page-1)*5)):(((page-1)*5)+5)], context=context)

        blog_tag_ids = blog_tags_env.search(cr, uid, [], context=context)
        blog_tags = blog_tags_env.browse(cr, uid, blog_tag_ids, context=context)
        
        p_blogs_ids = blog_post_env.search(cr, uid, [('displayAsCase', '=', False), ('website_published','=',True)], order='visits', context=context)
        p_blogs = blog_post_env.browse(cr, uid, p_blogs_ids, context=context)
        popular_blogs = tuple(reversed(p_blogs))
        
        pager_url = "/page/tag/%s" % blog_tag.id
        pager = request.website.pager(
            url=pager_url,
            total=total,
            page=page,
            step=self._blog_post_per_page,
        )
        values = {
                  'pager': pager,
                  'blog_tags': blog_tags,
                  'all_blog_posts': blog_posts,
                  'popular_blogs' : popular_blogs[0:3],
                }
        return request.website.render('theme_aditim.blog_aggregator_page', values)

    @route(['''/page/<model("blog.blog"):blog>/post/<model("blog.post", "[('blog_id','=',blog[0])]"):blog_post>''',
            ], type='http', auth="public", website=True)
    def postTheBlog(self, blog, blog_post):
        cr, uid, context = request.cr, self._super_user, request.context
        
        blog_post_obj = request.registry['blog.post']
        blog_tags_env = request.registry['blog.tag']
        tags = blog_post.tag_ids
        
        mail_msg_obj = request.registry['mail.message']
        blog_comments_ids = mail_msg_obj.search(cr, uid, [('model', '=', 'blog.post'),('res_id', '=', blog_post.id), ('website_published','=',True)], context=context)
        blog_comments = mail_msg_obj.browse(cr, uid, blog_comments_ids, context=context)

        blog_tag_ids = blog_tags_env.search(cr, uid, [], context=context)
        blog_tags = blog_tags_env.browse(cr, uid, blog_tag_ids, context=context)

        p_blogs_ids = blog_post_obj.search(cr, uid, [('displayAsCase', '=', False), ('website_published','=',True)], order='visits', context=context)
        p_blogs = blog_post_obj.browse(cr, uid, p_blogs_ids, context=context)
        popular_blogs = tuple(reversed(p_blogs))
        
        request.session[request.session_id] = request.session.get(request.session_id, [])
        if not (blog_post.id in request.session[request.session_id]):
            request.session[request.session_id].append(blog_post.id)
            # Increase counter
            blog_post.write({ 'visits': blog_post.visits+1 })
        
        values = {
                  'blog_post_detail': blog_post,
                  'blog_post_tags' : tags,
                  'blog_comments' : blog_comments,
                  'three_popular' : popular_blogs[0:3],
                  'four_popular' : popular_blogs[0:4],
                  'blog_tags_cloud':blog_tags,
                }
            
        return request.website.render('theme_aditim.blog_inner_page', values)
    
    @route(['/page/theme_aditim.projects_page',
            '/page/theme_aditim.projects_page/page/<int:page>',
            '/projects/all',
            '/projects/all/page/<int:page>'], type='http', auth="public", website=True)
    def getCasesData(self, page=1):
        cr, uid, context = request.cr, self._super_user, request.context
        currentPath = request.httprequest.path
        all_project_url = currentPath.find('/projects/all') 
        
        if (all_project_url != -1):
            pageUrl = '/projects/all' 
        else:
            pageUrl = '/page/theme_aditim.projects_page'
        
        case_post_env = request.registry['case.post']
        case_category_env = request.registry['case.category']

        case_categories_ids = case_category_env.search(cr, uid, [], context=context)
        case_categories = case_category_env.browse(cr, uid, case_categories_ids, context=context)

        if request.session.uid:
            total = len(case_post_env.search(cr, uid, [], context=context))
            case_post_ids = case_post_env.search(cr, uid, [], offset=(page-1)*self._case_post_per_page, limit=self._case_post_per_page, context=context)
        else:
            total = len(case_post_env.search(cr, uid, [('website_published','=',True)], context=context))
            case_post_ids = case_post_env.search(cr, uid, [('website_published','=',True)], offset=(page-1)*self._case_post_per_page, limit=self._case_post_per_page, context=context)
            
        important_cases_ids = case_post_env.search(cr, uid, [('website_published','=',True),('important_case','=',True)], offset=0, limit=3, context=context)
        case_posts = case_post_env.browse(cr, uid, case_post_ids, context=context)
        important_cases = case_post_env.browse(cr, uid, important_cases_ids, context=context)
        
        pager = request.website.pager(
            url=pageUrl,
            total=total,
            page=page,
            step=self._case_post_per_page,
        )
        values = {
                  'case_categories': case_categories,
                  'pager': pager,
                  'case_posts': case_posts,
                  'important_cases': important_cases,
                  'all_cases':True,
                }
        return request.website.render('theme_aditim.projects_page', values)
    
    @route(['''/page/<model("case.category"):case>/case/<model("case.post"):case_post>''',
            ], type='http', auth="public", website=True)
    def postTheCase(self, case, case_post):
        cr, uid, context = request.cr, self._super_user, request.context
        
        mail_msg_obj = request.registry['mail.message']
        case_comments_ids = mail_msg_obj.search(cr, uid, [('type', '=','comment'),('model', '=', 'case.post'),('res_id', '=', case_post.id), ('website_published','=',True)], context=context)
        case_comments = mail_msg_obj.browse(cr, uid, case_comments_ids, context=context)
        case_tags = case_post.tag_ids
        case_post_env = request.registry['case.post']
        case_post_ids = case_post_env.search(cr, uid, [('website_published','=',True)], context=context)
        if len(case_post_ids) > 3 :
            three_random_cases_ids = random.sample(case_post_ids, 3)
        else:
            three_random_cases_ids = case_post_ids

        three_random_cases = case_post_env.browse(cr, uid, three_random_cases_ids, context=context)
        
        values = {
                  'case_posts': case_post,
                  'case_tags': case_tags,
                  'case_comments': case_comments,
                  'three_random_cases':three_random_cases,
                }
        return request.website.render('theme_aditim.projects_interior_page', values)
    
    @route(['/casepost/comment/<model("case.post"):case_post>',
            ], type='http', auth="public", website=True)
    def setCaseCommentData(self, case_post, **form_data):
        cr, uid, context = request.cr, self._super_user, request.context

        case_comment = form_data.get('case_comment')
        your_name = form_data.get('your_name')
        email = form_data.get('pemail')
        res_id = case_post.id
        
        case_comment_env = request.registry['mail.message']
        values = {
                  'comment_text': case_comment, 
                  'organization_name': your_name,
                  'reply_to': email,
                  'res_id': res_id, 
                  'type': 'comment', 
                  'model':'case.post'
        }
        case_comment_env.create(cr, uid, values, context=context)
        
        return redirect("/page/%s/case/%s" % (slug(case_post.case_cat_id), slug(case_post)))
    
    @route(['/projects/<model("case.category"):case_category>',
            '/projects/<model("case.category"):case_category>/page/<int:page>',
            ], type='http', auth="public", website=True)
    def getCasesDataByCategory(self, case_category, page=1):
        cr, uid, context = request.cr, self._super_user, request.context
        case_category_env = request.registry['case.category']

        case_categories_ids = case_category_env.search(cr, uid, [], context=context)
        case_categories = case_category_env.browse(cr, uid, case_categories_ids, context=context)
        
        case_post_env = request.registry['case.post']
        if request.session.uid:
            total = len(case_post_env.search(cr, uid, [('case_cat_id','=',case_category.id)], context=context))
            case_post_ids = case_post_env.search(cr, uid, [('case_cat_id','=',case_category.id)], offset=(page-1)*self._case_post_per_page, limit=self._case_post_per_page, context=context)
        else:
            total = len(case_post_env.search(cr, uid, [('website_published','=',True),('case_cat_id','=',case_category.id)], context=context))
            case_post_ids = case_post_env.search(cr, uid, [('website_published','=',True),('case_cat_id','=',case_category.id)], offset=(page-1)*self._case_post_per_page, limit=self._case_post_per_page, context=context)
            
        case_posts = case_post_env.browse(cr, uid, case_post_ids, context=context)
        
        important_cases_ids = case_post_env.search(cr, uid, [('website_published','=',True),('important_case','=',True),('case_cat_id','=',case_category.id)], offset=0, limit=3, context=context)
        important_cases = case_post_env.browse(cr, uid, important_cases_ids, context=context)

        pager_url = "/projects/%s" % case_category.id
        pager = request.website.pager(
            url= pager_url,
            total=total,
            page=page,
            step=self._case_post_per_page,
        )
        values = {
                  'case_categories': case_categories,
                  'pager': pager,
                  'case_posts': case_posts,
                  'selected_case_categories':case_category,
                  'important_cases': important_cases,
                }
        return request.website.render('theme_aditim.projects_page', values)
    
    @route(['/blogpost/comment/<model("blog.post"):blog_post>',
            ], type='http', auth="public", website=True)
    def setBlogCommentData(self, blog_post, **form_data):
        cr, uid, context = request.cr, self._super_user, request.context

        blog_comment = form_data.get('blog_comment')
        org_name = form_data.get('org_name')
        city = form_data.get('city')
        res_id = blog_post.id
        
        blog_comment_env = request.registry['mail.message']
        values = {
                  'comment_text': blog_comment, 
                  'organization_name': org_name, 
                  'city': city, 'res_id': res_id, 
                  'type': 'comment', 
                  'model':'blog.post'
        }
        blog_comment_env.create(cr, uid, values, context=context)
        
        return redirect("/page/%s/post/%s" % (slug(blog_post.blog_id), slug(blog_post)))
    
    @route("/page/product_interior_page/p/<model('product.template'):product_template>", type='http', auth="public", website=True)
    def getProductDetailDataByProduct(self, product_template):
        product_env = request.env['product.category']
        cat_id = product_template.categ_id;
        product_prod_env = request.env['product.product']
        product_category = product_env.search([('id', '=', cat_id.id)])
        linkToPage = product_category[0].detailPage
        
        product_attributes = [];
        products_product_ids = product_prod_env.search([('product_tmpl_id', '=', product_template.id)])
        for prod_prod_ids in products_product_ids:
            for attribute_value in prod_prod_ids.attribute_value_ids:
                product_attributes.append(attribute_value);
        
        values = {
                  'productsBycategory': product_template,
                  'product_attributes': product_attributes,
                }
        return request.website.render(linkToPage, values)
    
    @route(['/contact/secondform'], type='http', auth="public", website=True)
    def cart_update_custom_profile_length(self, **form_data):
        cr, uid, context = request.cr, self._super_user, request.context
        
        medium_id = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'crm.crm_medium_website')
        section_id = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'website.salesteam_website_sales')

        your_name = form_data.get('your_name')
        email = form_data.get('email')
        org_name = form_data.get('org_name')
        your_city = form_data.get('your_city')
        phone_number = form_data.get('phone_number')
        your_position = form_data.get('your_position')
        response = form_data.get('response')
        category = form_data.get('category')
        clarification = form_data.get('clarification')
        
        values = {
                  'user_id': False,
                  'medium_id' : medium_id,
                  'section_id' : section_id,
                  'name' : your_name,
                  'email_from': email,
                  'phone': phone_number,
                  'partner_name': org_name,
                  'city':your_city,
                  'description': clarification,
                  'position' : your_position,
                  'need_answer' : response,
                  'interested_category' : category
        }
        
        lead = request.registry['crm.lead'].create(cr, uid, values, context=dict(context, mail_create_nosubscribe=True))
        
        return redirect("/page/contactus_page")

    @route(['/contact/authform/<model("case.post"):case_posts>',
            ], type='http', auth="public", website=True)
    def case_authentication_for_download(self,case_posts, **form_data):
        cr, uid, context = request.cr, self._super_user, request.context
        medium_id = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'crm.crm_medium_website')
        section_id = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'website.salesteam_website_sales')
        your_name = form_data.get('last_name')
        email = form_data.get('email')
        attach_id = form_data.get('url')
        url = '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=datas_fname&id='
        url += attach_id

        values = {
                  'user_id': False,
                  'medium_id' : medium_id,
                  'section_id' : section_id,
                  'name' :case_posts.name,
                  'email_from': email,
                  'contact_name' :your_name
        }
        lead = request.registry['crm.lead'].create(cr, uid, values, context=dict(context, mail_create_nosubscribe=True))
        return redirect(url)

class website(openerp.addons.web.controllers.main.Home):
    @route('/website/attach', type='http', auth='user', methods=['POST'], website=True)
    def attach(self, func, upload=None, url=None, disable_optimization=None):
        Attachments = request.registry['ir.attachment']

        website_url = message = None
        if not upload:
            website_url = url
            name = url.split("/").pop()
            attachment_id = Attachments.create(request.cr, request.uid, {
                'name': name,
                'type': 'url',
                'url': url,
                'res_model': 'ir.ui.view',
            }, request.context)
        else:
            try:
                image_data = upload.read()
                image = Image.open(cStringIO.StringIO(image_data))
                w, h = image.size
                # ---Add by surekha technologies------------
                # to allow user to upload image of any size.......
                '''
                if w*h > 42e6: # Nokia Lumia 1020 photo resolution
                    raise ValueError(
                        u"Image size excessive, uploaded images must be smaller "
                        u"than 42 million pixel")
                        '''

                if not disable_optimization and image.format in ('PNG', 'JPEG'):
                    image_data = image_save_for_web(image)

                attachment_id = Attachments.create(request.cr, request.uid, {
                    'name': upload.filename,
                    'datas': image_data.encode('base64'),
                    'datas_fname': upload.filename,
                    'res_model': 'ir.ui.view',
                }, request.context)

                [attachment] = Attachments.read(
                    request.cr, request.uid, [attachment_id], ['website_url'],
                    context=request.context)
                website_url = attachment['website_url']
            except Exception, e:
                #logger.exception("Failed to upload image to attachment")
                message = unicode(e)

        return """<script type='text/javascript'>
            window.parent['%s'](%s, %s);
        </script>""" % (func, json.dumps(website_url), json.dumps(message))