import os
import logging
from lxml import etree
import base64
import datetime

# from anytree import Node
# from anytree.exporter import UniqueDotExporter

from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class Change(models.Model):
    _inherit = "certificate_planer.change"
    
    def _collect_parts(self, root_part):
        """Collect all parts in the BOM structure starting from root part (initiator of the change).
        Called by _export_change_to_xml.
        """
        # find all children of the root part
        # root_part.walk_down()

        # construct tree from change to children
        tree_root = root_part.tree_down()
        tree_root.vshow()

        # children without children (leaf nodes)
        leaf_nodes = [node for node in tree_root.descendants if not node.children]
        child_part_list = [self.env['certificate_planer.part'].browse(leaf_node.part_id) for leaf_node in leaf_nodes]

        tree_list = []
        for part in child_part_list:
            tree = part.walk_up_bigtree()
            tree_list.append(tree)
        
        # NOTE: meaning?
        return tree_list
        # return visited, paths_dict
        # return self.env['certificate_planer.part'].browse(list(visited))

    # NOTE: Old version, may be not needed anymore
    # def _collect_parts(self, root_part):
    #     """Collect all parts in the BOM structure starting from root_part.
    #     Called by _export_change_to_xml.
    #     """
    #     visited = root_part.walk_down()
    #     visited = root_part.walk_up(visited)
    #     return self.env['certificate_planer.part'].browse(list(visited))

    def _collect_certificates(self, tree_list):
        for tree in tree_list:
            root = tree
            part = self.env['certificate_planer.part'].browse(root.part_id)
            certificate_id = part._get_certificate().id if part._get_certificate() else None
            root.collected_certificates = [certificate_id] if certificate_id else []
            for i, node in enumerate(root.descendants):
                part = self.env['certificate_planer.part'].browse(node.part_id)
                certificate_id = part._get_certificate().id if part._get_certificate() else None
                root.collected_certificates.append(certificate_id)

            for node in root.descendants:
                part = self.env['certificate_planer.part'].browse(node.part_id)
                certificate_id = part._get_certificate().id if part._get_certificate() else None
                node.collected_certificates = [certificate_id] if certificate_id else []
                for tmp_node in node.descendants:
                    part = self.env['certificate_planer.part'].browse(tmp_node.part_id)
                    certificate_id = part._get_certificate().id if part._get_certificate() else None
                    node.collected_certificates.append(certificate_id)


    # def _collect_certificates(self, parts, paths_dict):
    #     """Collect certificates for each part in path of parts.
    #     called by _export_change_to_xml.
    #     """
    #     certificate_collection = {}
    #     for part in parts:

    #         # part id's as part names to one string separated by ;
    #         if part.id in paths_dict:

    #             # ignore this path if last part of path has no certificate
    #             last_part_in_path_id = paths_dict[part.id][-1]
    #             last_part_in_path = self.env['certificate_planer.part'].browse(last_part_in_path_id)
    #             if not last_part_in_path._get_certificate():
    #                 certificate_collection[part.id] = ""
    #                 continue
    #             certificate_list = []
    #             for part_id in paths_dict[part.id]:
    #                 path_list_part = self.env['certificate_planer.part'].browse(part_id)
    #                 if path_list_part._get_certificate():
    #                     certificate_list.append(path_list_part.name)
    #                     # certificate_list.append(path_list_part._get_certificate())
    #                 # part_name_list.append(path_list_part.name)
    #                 # certificate_str = path_list_part._get_certificate() if ._has_certificate() else 
    #                 # certificate = path_list_part._get_certificate() if ._has_certificate() else 
    #             certificate_collection[part.id] = ";".join(certificate_list)                      
    #             # certificate_collection[part.id] = ";".join(f"{part_id}" for part_id in paths_dict[part.id])
    #         else:
    #             certificate_collection[part.id] = part.name if part._get_certificate() else ""

    #             # for part_id in paths_dict[part.id]:
    #                 # certificate_collection[part_id] = ";".join(f"{part_id}" for part_id in paths_dict[part.id])
    #     return certificate_collection
    #     # for part in parts:
    #     #     certs = []
    #     #     certificate = part._get_certificate()
    #     #     if certificate:
    #     #         certs.append(certificate.display_name)
    #     #     certifcate_collection[part.id] = certs
    #     # return certifcate_collection

    def _find_top_part(self, parts):
        """Return the part with no parents.
        called by _export_change_to_xml."""
        for part in parts:
            if not part.parent_bom_ids:
                return part
        return None

    def _action_export_to_attachment(self):
        self.ensure_one()

        xml_data = self._export_change_to_xml() 

        fname = f'change_{self.id}_approved.xml'
        xml_b64 = base64.b64encode(xml_data)

        attachment = self.env['ir.attachment'].create({
            'name': fname,
            'type': 'binary',
            'datas': xml_b64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/xml',
        })

        _logger.warning(f"attachment: {attachment}")

        return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }

    def _action_export_to_file(self):
        self.ensure_one()
        xml_data = self._export_change_to_xml()
        _logger.warning(f"xml_data: {xml_data}")

        export_dir = '/tmp/odoo_exports'
        os.makedirs(export_dir, exist_ok=True)

        # File name
        fname = f'change_{self.id}_export.xml'
        file_path = os.path.join(export_dir, fname)

        # Write the file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_data.decode('utf-8'))

            _logger.info(f"Exported Change {self.id} to {file_path}")
            self.message_post(
                body=f"XML export created: {file_path}",
                subject="XML Export",
                message_type='notification'
            )
        except:
            raise UserError(_('no export'))

        return True


    def _export_change_to_xml(self):
        """Called by _action_export_to_file and _action_export_to_attachment.
        Export XML for this change, including all parts in the BOM structure.
        """
        self.ensure_one()

        _logger.warning(f"self: {self}")

        certificate = self.certificate_id
        _logger.warning(f"certificate: {certificate}")
        part = certificate.part_id
        _logger.warning(f"part: {part}")
        

        # print("Up tree:", flush=True)
        tree_list = self._collect_parts(part)
        for tree in tree_list:
            tree.hshow()
        # print("====", flush=True)

        self._collect_certificates(tree_list)

        xml_parts_dict = {}
        for i, tree in enumerate(tree_list):
            # print(f"Tree: {i}")
            root = tree
            part_id = root.part_id
            if part_id not in xml_parts_dict:
                xml_parts_dict[part_id] = {
                    'part': self.env['certificate_planer.part'].browse(part_id),
                }
                xml_parts_dict[part_id]['collected_certificates'] = root.collected_certificates
            for node in root.descendants:
                part_id = node.part_id
                if part_id not in xml_parts_dict:
                    xml_parts_dict[part_id] = {
                        'part': self.env['certificate_planer.part'].browse(part_id),
                    }
                xml_parts_dict[part_id]['collected_certificates'] = node.collected_certificates
        # print(xml_parts_dict)
            # part = self.env['certificate_planer.part'].browse(part_id)
            # print(f"part_id: {root.part_id}, collected_certificates: {root.collected_certificates}")
            # for node in root.descendants:
            #     print(f"part_id: {node.part_id}, collected_certificates: {node.collected_certificates}")

        # parts, paths_dict = self._collect_parts(part)

        # collecting certificates for each part
        # certifcate_collection = self._collect_certificates(parts, paths_dict)

        # _logger.critical(f"collected parts: {parts}")
        # for part in parts:
        #     _logger.critical(f"PDMEXP: part: {part.name}")
            # _logger.critical(f"PDMEXP: part: {part}, certificate: {part.certificate_id.id if part.certificate_id else 'None'}")
            # _logger.critical(f"part: {part}, certificate: {part._get_certificate()}")

        # for part in parts:            
        #     # part._get_certificate().part_id.name if part._get_certificate() else ""
        #     _logger.critical(f"part: {part}")
        #     # _logger.critical(f"part: {part}, certificate: {part.certificate_id.id if part.certificate_id else 'None'}")
        #     # _logger.critical(f"part: {part}, certificate: {part._get_certificate()}")

        # return etree.tostring(
        #     etree.Element(
        #         "test"
        #     ),
        #     pretty_print=True,
        #     xml_declaration=False,
        #     encoding="UTF-8",
        # )

        # TODO: does top part have a certificate?
        # top = self._find_top_part(parts)

        # _logger.critical(f"PDMEXP: parts: {parts}")
        # _logger.warning(f"top: {top}")



        # top_certificate = top._get_certificate()
        # _logger.warning(f"top certificate: {top_certificate}")

        now_epoch = int(datetime.datetime.now().timestamp())
        # NOTE: Temporary simple XML for testing
        # Top-level attribute if certificate exists
        # if top and top_certificate:
        xml_root = etree.Element("transactions")
        # transaction_el = etree.SubElement(root, "transaction", date=f"{now_epoch}", type="wf_import_document_attributes", vaultname="Aerolite") 
        # document_el = etree.SubElement(transaction_el, "document") 
        # conf_el = etree.SubElement(document_el, "configuration", name="Standard", quantity="1") 
        # attr = etree.SubElement(root, "attribute")
        # attr.set("name", "Certificate")
        # attr.text = top_certificate.part_id.name

        for part_id in xml_parts_dict:
            if len(xml_parts_dict[part_id]['collected_certificates']) == 0:
                continue
            transaction_el = etree.SubElement(xml_root, "transaction", date=f"{now_epoch}", type="wf_import_document_attributes", vaultname="Aerolite") 
            document_el = etree.SubElement(transaction_el, "document") 

            # Artikelnummer
            conf_el = etree.SubElement(document_el, "configuration", name="Standard", quantity="1")
            part = xml_parts_dict[part_id]['part']
            attr_el = etree.SubElement(conf_el, "attribute", name="Artikelnummer", value=part.name)

            # EMS
            attr_el = etree.SubElement(conf_el, "attribute", name="EMS", value=f"{1 if part.is_ems_equipment else 0}")

            # cert_str = ""
            # for i, cert_id in enumerate(xml_parts_dict[part_id]['collected_certificates']):
            cert_display_names = [self.env['certificate_planer.certificate'].browse(cert_id).display_name for cert_id in xml_parts_dict[part_id]['collected_certificates'] if cert_id]
            certificate_str = ";".join(cert_display_names)
            attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=f"{certificate_str}")

            # aircraft_type
            aircraft_ids = [int(self.env['certificate_planer.certificate'].browse(cert_id).aircraft_type_id) for cert_id in xml_parts_dict[part_id]['collected_certificates'] if cert_id]
            aircraft_type_names = [self.env['certificate_planer.aircraft_type'].browse(ac_id).name for ac_id in aircraft_ids if ac_id]
            aircraft_ids_str = ";".join(aircraft_type_names)
            attr_el = etree.SubElement(conf_el, "attribute", name="Aircraft type", value=aircraft_ids_str)

            attr_el = etree.SubElement(conf_el, "attribute", name="Typ", value="CPL")


            # if len(aircraft_ids):
            #     aircraft_ids_str = ";".join(aircraft_ids)
            # else:
            #     aircraft_ids_str = ""
            # attr_el = etree.SubElement(conf_el, "attribute", name="Aircraft type", value=aircraft_ids_str)

                # attr_el = etree.SubElement(conf_el, "attribute", name=f"Certificate_Level_{i+1}", value=certificate.display_name if certificate else "")


            # attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=';'.join(cert_collection[part.id]) if part.id in cert_collection else "")
            # attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=certificate.display_name if certificate else "")
            # attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=f"{certificate}")
            # attr_el = etree.SubElement(conf_el, "attribute", name="Certificate", value=certificates_str)
            
        #     # <attribute name="Aircraft type" value="PC-24"/>
        #     attr_el = etree.SubElement(conf_el, "attribute", name="Aircraft type", value=part.designation)
        #     # part.certificate_id.aircraft_type_id.name if part.certificate_id else ""
            
        #     # configuration_el = etree.SubElement(document_el, "configuration") 
        #     # certificate = part._get_certificate().part_id.name if part._get_certificate() else ""
        #     # attribute_el = etree.SubElement(configuration_el, "attribute", Certificate=certificate)

        return etree.tostring(
            xml_root, 
            pretty_print=True, 
            xml_declaration=True, 
            encoding="UTF-8"
        )

    # @api.model
    # def write(self, vals):
    #     _logger.warning(f"vals: {vals}")
    #     # Capture previous statuses before write
    #     previous_status = {rec.id: rec.status_id for rec in self}
    #     _logger.warning(f"previous_status: {previous_status}")

    #     res = super().write(vals)

    #     for rec in self:
    #         new_status = rec.status_id
    #         _logger.warning(f"new status: {new_status}")

    #         if 'status_id' in vals:
    #             old = previous_status.get(rec.id)
    #             _logger.warning(f"old: {old}")
    #             if not old or old != new_status:
    #                 if new_status and new_status.pdm_export_trigger:
    #                     rec._action_export_to_file()

    #     return res

    def _build_tree(self, root_parts):
        root_nodes = []
        for root_part in root_parts:
            root_node = Node(root_part.name)
            root_nodes.append(root_node)
            self._build_tree_helper(root_part, root_node)
        return root_nodes

    def _build_tree_helper(self, part, node):
        for bom_line in part.part_ids:
            child_part = bom_line.certificate_planer_part_id
            child_node = Node(child_part.name, parent=node)
            self._build_tree_helper(child_part, child_node)

    def _print_tree(self, tree):
        export_dir = '/tmp/odoo_exports'
        os.makedirs(export_dir, exist_ok=True)

        for tree_node in tree:
            fname = f'change_{self.id}_export_{tree_node.name}.png'
            file_path = os.path.join(export_dir, fname)
            UniqueDotExporter(tree_node).to_picture(file_path)        