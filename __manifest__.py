# -*- coding: utf-8 -*-
{
    'name': "Certificate Planer",

    'summary': """
        Certificate Planer Summary
    """,

    'description': """
        Certificate Planer Description
    """,

    'author': "Mint System GmbH",
    'website': "https://www.mint-system.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/part.xml',
        'views/bom.xml',
        'views/specification.xml',
        'views/issue_group.xml',
        'views/certificate.xml',
        'views/issue.xml',
        'views/document.xml',
        'views/document_type.xml',
        'views/document_revision.xml',
        'views/document_revision_state.xml',
        'views/menu.xml',
        'report/document_report.xml',
        'demo/demo.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],

    # module registry settings
    'installable': True,
    'application': True,
}
