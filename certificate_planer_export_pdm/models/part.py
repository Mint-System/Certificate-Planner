from odoo import models, fields, api
from lxml import etree
import base64

from bigtree import Node

import logging
_logger = logging.getLogger(__name__)

class Part(models.Model):
    _inherit = 'certificate_planer.part'


    def _has_certificate(self):
        self.ensure_one()
        return bool(self.certificate_id)

    def _get_certificate(self):
        """Return a singleton certificate for this part (or False)"""
        self.ensure_one() 
        part = self
        # model
        certificate = self.env['certificate_planer.certificate'].search(
            [('part_id', '=', part.id)], limit=1
        )
        return certificate or False

    def tree_down(self, tree_root=None, parent=None):
        """
        Recursively build a bigtree Node structure representing the BOM hierarchy.
        Walks from this part down to all child parts (top-to-bottom).
        """
        node_name = f"{self.name} ({self.designation})"
        node = Node(
            node_name,
            part_id=self.id,
            part_name=self.name,
        )
        if not parent:
            # root node
            tree_root = node
            # parent = tree_root
        else:
            node.parent = parent

        for part in self:
            for bom_line in part.part_ids:
                child = bom_line.certificate_planer_part_id
                if child:
                    child.tree_down(tree_root=tree_root, parent=node)

        return tree_root


    # def walk_down(self, visited=None):
    #     """Collect ids of this part and all children (recursively) via BoM lines."""
    #     if visited is None:
    #         visited = set()
    #     for part in self:
    #         if part in visited:
    #         # if part.id in visited:
    #             continue
    #         visited.add(part)
    #         # part.part_ids are BomPartRel records (certificate_planer_bom_certificate_planer_part_rel)
    #         for bom_line in part.part_ids:
    #             child = bom_line.certificate_planer_part_id
    #             if child and child not in visited:
    #             # if child and child.id not in visited:
    #                 # recursive call on Part record
    #                 child.walk_down(visited)

    #     return visited


    # def walk_up(self, path_list, visited=None):
    #     """Collect ids of this part and all parents (recursively) via parent BoMs."""
    #     if visited is None:
    #         visited = set()

    #     path_list.append(self.id)
    #     # certificate = self._get_certificate().display_name if self._get_certificate() else ""
    #     # if not root_part_id in cert_collection:
    #     #     cert_collection[root_part_id] = [certificate]
    #     # else:
    #     #     cert_collection[root_part_id].append(certificate)

        
    #     # parent_bom_ids are BoM records; bom.part_id is the parent part
    #     for bom in self.parent_bom_ids:
    #         parent = bom.part_id
    #         # path_list.append(parent.id)
    #         if parent and parent not in visited:
    #             # certificate = parent.certificate_id if parent.certificate_id else None
    #             # parent.certificate_id
    #             # logger.warning(f"walk_up: parent part {parent.designation} has certificate {certificate}")
    #             visited.add(parent)
    #         # TEST
    #         parent.walk_up(path_list, visited)
    #     return visited
    #     # return visited, cert_collection


    # def walk_up(self, visited=None):
    #     """Collect ids of this part and all parents (recursively) via parent BoMs."""
    #     if visited is None:
    #         visited = set()
    #     for part in self:
    #         if part.id in visited:
    #             continue
    #         visited.add(part.id)
    #         # parent_bom_ids are BoM records; bom.part_id is the parent part
    #         for bom in part.parent_bom_ids:
    #             parent = bom.part_id
    #             if parent and parent.id not in visited:
    #                 parent.walk_up(visited)
    #     return visited


    def walk_up_bigtree(self, visited=None):
        """
        Build a bigtree Node structure representing the reverse BOM hierarchy.
        Walks from this part up to all parent assemblies (bottom-to-top).

        Returns:
            bigtree.Node: Root node representing this part, with children nodes
                          representing parent assemblies in the BOM hierarchy.
                          Returns None if bigtree is not installed.

        Example:
            part = self.env['certificate_planer.part'].search([('name', '=', 'F partnr')])
            tree = part.walk_up_bigtree()
            if tree:
                from bigtree import print_tree
                print_tree(tree, attr_list=["part_id", "level"])
        """
        # if not BIGTREE_AVAILABLE:
        #     _logger.warning("bigtree package is not installed. Please install it with: pip install bigtree")
        #     return None

        self.ensure_one()

        if visited is None:
            visited = set()

        # Create node for current part with all relevant attributes
        node_name = f"{self.name} ({self.designation})"
        node = Node(
            node_name,
            part_id=self.id,
            part_name=self.name,
        )
        # node = Node(
        #     node_name,
        #     part_id=self.id,
        #     part_name=self.name,
        #     part_designation=self.designation,
        #     level=0,  # Will be updated for child nodes
        #     has_bom=bool(self.bom_id),
        #     parent_bom_count=self.parent_bom_count
        # )
            # has_certificate=bool(self._get_certificate()),

        # Mark this part as visited
        visited.add(self.id)

        # Recursively process parent BOMs
        self._walk_up_bigtree_recursive(node, visited, level=1)

        return node

    def _walk_up_bigtree_recursive(self, parent_node, visited, level=1):
        """
        Helper method for walk_up_bigtree to recursively build the tree.

        Args:
            parent_node: The bigtree Node to attach children to
            visited: Set of part IDs already visited (to prevent cycles)
            level: Current depth level in the tree
        """
        # parent_bom_ids are BoM records; bom.part_id is the parent part
        for bom in self.parent_bom_ids:
            parent_part = bom.part_id

            if parent_part and parent_part.id not in visited:
                # Create node for parent part
                node_name = f"{parent_part.name} ({parent_part.designation})"
                child_node = Node(
                    node_name,
                    parent=parent_node,
                    part_id=parent_part.id,
                    part_name=parent_part.name,
                )
                # child_node = Node(
                #     node_name,
                #     parent=parent_node,
                #     part_id=parent_part.id,
                #     part_name=parent_part.name,
                #     part_designation=parent_part.designation,
                #     level=level,
                #     has_bom=bool(parent_part.bom_id),
                #     has_certificate=bool(parent_part._get_certificate()),
                #     parent_bom_count=parent_part.parent_bom_count
                # )

                # Mark as visited
                visited.add(parent_part.id)

                # Recursively process this parent's parents
                parent_part._walk_up_bigtree_recursive(child_node, visited, level + 1)



