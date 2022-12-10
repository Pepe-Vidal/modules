# -*- coding: utf-8 -*-
{
    'name': "WheelSpeed",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/car_type.xml',
        'views/car.xml',
        'views/engine_type.xml',
        'views/engine.xml',
        'views/chassis_type.xml',
        'views/chassis.xml',
        'views/suspension_type.xml',
        'views/suspension.xml',
        'views/brake_type.xml',
        'views/brake.xml',
        'views/wheel_type.xml',
        'views/wheel.xml',
        'views/player.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
