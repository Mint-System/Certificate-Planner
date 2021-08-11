{
    'name': "Certificate Planner",

    'summary': """
        Approve and manage aircraft documents and certificates.
    """,

    'author': 'Mint System GmbH, Odoo Community Association (OCA)',
    'website': "https://www.mint-system.ch",

    'category': 'Operations',
    'version': '13.0.2.3.1',
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
        'views/document_part_report.xml',
        'views/change_status.xml',
        'views/change_classification.xml',
        'views/post_certification_item_status.xml',
        'views/post_certification_item.xml',
        'views/document_class.xml',
        'views/part_category.xml',
        'views/bom_prerequisite_rel.xml',
    ],

    # module registry settings
    'installable': True,
    'application': True,
}
