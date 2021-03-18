# -*- coding: utf-8 -*-
{
    'name': "Certificate Planner",

    'summary': """
        Approve and manage aircraft documents and certificates.
    """,

    'description': """
        Approve and manage aircraft documents and certificates.
    """,

    'author': "Mint System GmbH",
    'website': "https://www.mint-system.ch",

    'category': 'Operations',
    'version': '13.0.1.2.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/certificate_planner_security.xml',
        'security/ir.model.access.csv',
        'views/part.xml',
        'views/bom.xml',
        'views/specification.xml',
        'views/issue_group.xml',
        'views/certificate.xml',
        'views/aircraft_type.xml',
        'views/issue.xml',
        'views/document.xml',
        'views/document_type.xml',
        'views/document_revision.xml',
        'views/document_revision_state.xml',
        'views/menu.xml',
        'report/document_report.xml',
        'views/document_part_report.xml'
        #'demo/demo.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],

    # module registry settings
    'installable': True,
    'application': True,
}
