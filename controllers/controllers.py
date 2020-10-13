# -*- coding: utf-8 -*-
# from odoo import http


# class CertificatePlaner(http.Controller):
#     @http.route('/certificate_planer/certificate_planer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/certificate_planer/certificate_planer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('certificate_planer.listing', {
#             'root': '/certificate_planer/certificate_planer',
#             'objects': http.request.env['certificate_planer.certificate_planer'].search([]),
#         })

#     @http.route('/certificate_planer/certificate_planer/objects/<model("certificate_planer.certificate_planer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('certificate_planer.object', {
#             'object': obj
#         })
