# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
import openerp.tools
import werkzeug
import logging
_logger = logging.getLogger(__name__)
#import re
#import time
#from datetime import date, datetime, timedelta
#from dateutil.relativedelta import relativedelta

class project_timereport(http.Controller):
        
    @http.route(['/timereport/<model("res.users"):user>', '/timereport/<model("res.users"):user>/list', '/timereport'], type='http', auth="user", website=True)
    def timereport_list(self, user=False, clicked=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if not user:
            return werkzeug.utils.redirect("/timereport/%s/list" %uid,302)
           
        ctx = {
            'user' : user,
            'tasks': request.registry.get('project.task').browse(cr,uid,request.registry.get('project.task').search(cr,uid,[("user_id","=",user.id)])
            ,context=context),             
            }
    

        return request.render('project_timereport.project_timereport', ctx)
        
    @http.route(['/timereport/<model("res.users"):user>/<model("project.task"):task>'], type='http', auth="user", website=True)
    def timereport_form(self, user=False, task=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        if not user:
            return werkzeug.utils.redirect("/timereport/%s/form" %uid,302)
            
        if request.httprequest.method == 'POST':
            _logger.warning("This is timereport post %s " % (post))
            
            work_id = pool.get('project.task.id').create(cr,uid,{
                'name': post.get('name'),
                'hours': post.get('hours'),
           #     'date': partner.property_account_position and partner.property_account_position.id or False,
                'user_id': user.id,
                })

           
        ctx = {
            'user' : user,
            'tasks': False,             
            }
    

        return request.render('project_timereport.project_timereport_form', ctx)
