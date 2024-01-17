{
    "name": "Certificate Planner",
    "summary": """
        Approve and manage aircraft documents and certificates.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Operations",
    "version": "14.0.1.14.0",
    "license": "AGPL-3",
    "depends": ["base", "mail", "survey"],
    "data": [
        "wizard/change.xml",
        "views/menu.xml",
        "data/report_paperformat.xml",
        "security/certificate_planner_security.xml",
        "security/ir.model.access.csv",
        "views/part.xml",
        "views/bom.xml",
        "views/specification.xml",
        "views/change_id.xml",
        "views/certificate.xml",
        "views/aircraft_type.xml",
        "views/change.xml",
        "views/document.xml",
        "views/document_type.xml",
        "views/document_revision.xml",
        "views/document_revision_index.xml",
        "report/document_report.xml",
        "views/document_part_report.xml",
        "views/change_status.xml",
        "views/change_classification.xml",
        "views/post_certification_item_status.xml",
        "views/post_certification_item.xml",
        "views/document_class.xml",
        "views/part_category.xml",
        "views/bom_part_rel.xml",
        "views/bom_prerequisite_rel.xml",
        "views/survey.xml",
        "views/assets.xml",
        "views/res_config_settings.xml",
        "report/mdl_report.xml",
        "report/tpi_report.xml",
        "report/mcr_report.xml",
    ],
    "installable": True,
    "application": True,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
