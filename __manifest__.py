{
    'name': "Certificate Planner",

    'summary': """
        Approve and manage aircraft documents and certificates.
    """,

    'author': 'Mint System GmbH, Odoo Community Association (OCA)',
    'website': "https://www.mint-system.ch",

    'category': 'Operations',
    'version': '13.0.2.1.0',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/certificate_planner_security.xml',
        'security/ir.model.access.csv',
        'views/part.xml',
        'views/bom.xml',
        'views/specification.xml',
        'views/change_id.xml',
        'views/certificate.xml',
        'views/aircraft_type.xml',
        'views/change.xml',
        'views/document.xml',
        'views/document_type.xml',
        'views/document_revision.xml',
        'views/document_revision_state.xml',
        'views/menu.xml',
        'report/document_report.xml',
        'views/document_part_report.xml'
    ],

    # module registry settings
    'installable': True,
    'application': True,
}
