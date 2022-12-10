# -*- coding: utf-8 -*-
# from odoo import http


# class WheelSpeed(http.Controller):
#     @http.route('/wheel_speed/wheel_speed', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wheel_speed/wheel_speed/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wheel_speed.listing', {
#             'root': '/wheel_speed/wheel_speed',
#             'objects': http.request.env['wheel_speed.wheel_speed'].search([]),
#         })

#     @http.route('/wheel_speed/wheel_speed/objects/<model("wheel_speed.wheel_speed"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wheel_speed.object', {
#             'object': obj
#         })
