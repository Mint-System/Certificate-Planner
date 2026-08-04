import datetime
import logging

from lxml import etree

from odoo import models

_logger = logging.getLogger(__name__)


class XmlExport(models.TransientModel):
    _name = "certificate_planer.xml_export"
    _description = "XML Export for PDM"

    def _treelist_to_xml(self, tree_list):
        """
        Convert tree list to XML format.
        """
        xml_parts_dict = {}
        for i, tree in enumerate(tree_list):
            root = tree
            part_id = root.part_id
            if part_id not in xml_parts_dict:
                xml_parts_dict[part_id] = {
                    "part": self.env["certificate_planer.part"].browse(part_id),
                }
                xml_parts_dict[part_id]["collected_certificates"] = root.collected_certificates
                xml_parts_dict[part_id]["collected_ems"] = root.collected_ems
            for node in root.descendants:
                part_id = node.part_id
                if part_id not in xml_parts_dict:
                    xml_parts_dict[part_id] = {
                        "part": self.env["certificate_planer.part"].browse(part_id),
                    }
                xml_parts_dict[part_id]["collected_certificates"] = node.collected_certificates
                xml_parts_dict[part_id]["collected_ems"] = node.collected_ems
        _logger.warning("xml_parts_dict created.")

        now_epoch = int(datetime.datetime.now().timestamp())

        xml_root = etree.Element("xml")
        transactions_el = etree.SubElement(xml_root, "transactions")

        for part_id in xml_parts_dict:
            if len(xml_parts_dict[part_id]["collected_certificates"]) == 0:
                continue

            part = xml_parts_dict[part_id]["part"]
            _logger.warning(f"part: {part.name}, cert: {part.certificate_id}")

            # don't export this part if certificate
            if part.certificate_id:
                continue

            # dont export this part if EMS equipment
            if part.is_ems_equipment:
                continue

            # no valid part
            if "EASA" in part.name:
                continue

            transaction_el = etree.SubElement(
                transactions_el,
                "transaction",
                date=f"{now_epoch}",
                type="wf_import_document_attributes",
                vaultname="Aerolite",
            )
            document_el = etree.SubElement(transaction_el, "document", aliasset="", pdmweid=part.name)

            # Artikelnummer
            conf_el = etree.SubElement(document_el, "configuration", name="Standard", quantity="1")
            attr_el = etree.SubElement(conf_el, "attribute", name="Artikelnummer", value=part.name)

            # EMS
            ems_names = {ems_name for ems_name in xml_parts_dict[part_id]["collected_ems"] if ems_name}
            ems_str = "; ".join(ems_names)
            attr_el = etree.SubElement(conf_el, "attribute", name="EMS", value=ems_str)

            # Certificate
            cert_display_names = {
                cert_id.part_id.name for cert_id in xml_parts_dict[part_id]["collected_certificates"] if cert_id
            }
            certificate_str = "; ".join(cert_display_names)
            attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=f"{certificate_str}")

            # aircraft_type
            aircraft_ids = [
                int(cert_id.aircraft_type_id)
                for cert_id in xml_parts_dict[part_id]["collected_certificates"]
                if cert_id
            ]
            aircraft_type_names = {
                self.env["certificate_planer.aircraft_type"].browse(ac_id).name for ac_id in aircraft_ids if ac_id
            }
            aircraft_ids_str = "; ".join(aircraft_type_names)
            attr_el = etree.SubElement(conf_el, "attribute", name="Aircraft type", value=aircraft_ids_str)

            attr_el = etree.SubElement(conf_el, "attribute", name="Typ", value="CPL")

        return etree.tostring(xml_root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
