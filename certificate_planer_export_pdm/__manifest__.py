# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Certificate Planer Export Pdm",
    "summary": """
        Export of Parts to XML.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["certificate_planer"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/change_status_confirm.xml",
        "wizard/change.xml",
        "views/change_status.xml",
        "views/res_config_settings.xml",
        "views/parts_view.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}