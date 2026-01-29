from odoo import models

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
        self.ensure_one() 
        node_name = f"{self.name} ({self.designation})"
        node = Node(
            node_name,
            part_id=self.id,
            part_name=self.name,
        )
        if not parent:
            # root node
            tree_root = node
        else:
            node.parent = parent

        for part in self:
            for bom_line in part.part_ids:
                child = bom_line.certificate_planer_part_id
                if child:
                    child.tree_down(tree_root=tree_root, parent=node)

        return tree_root

    def walk_up_bigtree(self):
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
        self.ensure_one()

        # Create node for current part with all relevant attributes
        node_name = f"{self.name} ({self.designation})"
        node = Node(
            node_name,
            part_id=self.id,
            part_name=self.name,
            certificate_id=self.env['certificate_planer.certificate'].search([("part_id", "=", self.id)]),
        )

        self._walk_up_bigtree_recursive(node)

        return node

    def _walk_up_bigtree_recursive(self, parent_node):
        """
        Helper method for walk_up_bigtree to recursively build the tree.

        Args:
            parent_node: The bigtree Node to attach children to
            visited: Set of part IDs already visited (to prevent cycles)
            level: Current depth level in the tree
        """
        self.ensure_one()

        for bom in self.parent_bom_ids:
            parent_part = bom.part_id

            if parent_part:
                _logger.warning(f"parent_part: {parent_part.id}")
                node_name = f"{parent_part.name} ({parent_part.designation})"
                child_node = Node(
                    node_name,
                    parent=parent_node,
                    part_id=parent_part.id,
                    part_name=parent_part.name,
                    certificate_id=self.env['certificate_planer.certificate'].search([("part_id", "=", parent_part.id)]),
                )

                # Recursively process this parent's parents
                parent_part._walk_up_bigtree_recursive(child_node)




