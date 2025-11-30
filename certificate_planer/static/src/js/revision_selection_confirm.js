odoo.define('certificate_planer.RevisionSelectionConfirm', function (require) {
    "use strict";

    const ListRenderer = require('web.ListRenderer');
    const Dialog = require('web.Dialog');
    const core = require('web.core');
    const _t = core._t;

    const RevisionSelectionConfirm = ListRenderer.include({

        /**
         * Override selection update to add confirmation when selecting a revision
         * linked to another change.
         */
        _updateSelection: function () {

            // Save previous selection state
            const previousSelection = JSON.stringify(this.selection);

            // Run original selection logic (updates this.selection)
            this._super.apply(this, arguments);

            // Compare new/old selection
            const newSelection = this.selection;

            // Find which ID was added
            let newlyAdded = null;
            const oldList = JSON.parse(previousSelection);

            for (const id of newSelection) {
                if (!oldList.includes(id)) {
                    newlyAdded = id;
                    break;
                }
            }

            // If no newly added row → nothing to do
            if (!newlyAdded) {
                return;
            }

            // Retrieve the corresponding record data
            const record = this.state.data.find(r => r.id === newlyAdded);

            if (!record) {
                return; 
            }

            // Is this a document_revision row?
            if (record.data.change_id && record.data.change_id.data.id) {

                const linkedChangeId = record.data.change_id.data.id;
                const currentChangeId = this.state.getContext().active_id;

                // Only prompt if linked to *another* change
                if (linkedChangeId !== currentChangeId) {

                    Dialog.confirm(this,
                        _t("This revision is already linked to another Change.\nDo you really want to reassign it?"),
                        {
                            confirm_callback: () => {
                                // do nothing (keep new selection)
                            },
                            cancel_callback: () => {
                                // Restore previous selection
                                this.selection = oldList;

                                // Restore UI checkboxes
                                this.$('tbody .o_list_record_selector input').each((i, input) => {
                                    const id = $(input).closest('tr').data('id');
                                    input.checked = oldList.includes(id);
                                });

                                this._updateFooter();
                            }
                        }
                    );
                }
            }
        },

    });

 return RevisionSelectionConfirm

});
