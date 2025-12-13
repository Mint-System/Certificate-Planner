from odoo import models, fields, api
from lxml import etree
import base64

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
        certificate = self.env['certificate_planer.certificate'].search(
            [('part_id', '=', self.id)], limit=1
        )
        return certificate or False

    def walk_top(self, visited=[]):
        """Return the top part in the BOM structure."""
        for bom in self.parent_bom_ids:
            parent = bom.part_id
            if parent and parent not in visited:
                visited.append(parent)
                parent.walk_top(visited)
        
        return visited
            

    def walk_down(self, visited=None):
        """Collect ids of this part and all children (recursively) via BoM lines."""
        if visited is None:
            visited = set()
        for part in self:
            if part in visited:
            # if part.id in visited:
                continue
            visited.add(part)
            # part.part_ids are BomPartRel records
            for bom_line in part.part_ids:
                child = bom_line.certificate_planer_part_id
                if child and child.id not in visited:
                    # recursive call on Part record
                    child.walk_down(visited)

        return visited


    def walk_up(self, visited=None):
        """Collect ids of this part and all parents (recursively) via parent BoMs."""
        if visited is None:
            visited = set()
        # for part in self:
        #     if part.id in visited:
        #         continue
        #     visited.add(part.id)
        # parent_bom_ids are BoM records; bom.part_id is the parent part
        for bom in self.parent_bom_ids:
            parent = bom.part_id
            if parent and parent.id not in visited:
                visited.add(parent.id)
                parent.walk_up(visited)
        return visited


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




        
