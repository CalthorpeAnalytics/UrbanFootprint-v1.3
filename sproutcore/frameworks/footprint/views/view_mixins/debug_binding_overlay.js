/***
 * Adds a mouseEntered and mouseExited function to any view to display its bindings and the
 * current value of those bindings in a popup window.
***/
Footprint.DebugBindingOverlay = {
    mouseExited: function(evt) {
        if (this._debugPane && this._debugPane.get('isPaneAttached'))
            this._debugPane.remove();
        try {
            sc_super()
        }
        catch(e) {}
    },
    mouseEntered: function(evt) {
        // If the metaKey was pressed. This is the command key on Macintosh or the ? key on PCs
        if (evt.metaKey) {
            this._debugPane = this._debugPane || SC.PickerPane.create({
                layout: { width: 800, height: 200 },
                // Override popup to create a reference to the anchor view
                popup: function (anchorViewOrElement, preferType, preferMatrix, pointerOffset) {
                    sc_super();
                    if (this._anchorView) {
                        this.set('anchor', this._anchorView);
                    }
                },
                contentView: SC.ScrollView.extend({
                    contentView: SC.SourceListView.extend({
                        anchorBinding: SC.Binding.oneWay('.parentView.parentView.parentView.anchor'),
                        // Content is the list of binding properties
                        contentBinding: SC.Binding.oneWay('.anchor').transform(function(value) {
                            return value && value._bindings;
                        }),
                        /***
                         * Displays a toString version of each binding
                         */
                        exampleView: SC.LabelView.extend({
                            anchor: null,
                            anchorBinding: SC.Binding.oneWay('.parentView.anchor'),
                            value: function() {
                                if (this.get('content') && this.get('anchor')) {
                                    var binding = this.get('anchor')[this.get('content')];
                                    return 'Binding: %@. Current Value: %@'.fmt(
                                        binding.toString(),
                                        binding._transformedBindingValue ?
                                            binding._transformedBindingValue.toString() :
                                            (typeof(binding) === 'undefined' ? 'undefined' : 'null')
                                    )
                                }
                                else {
                                    return "Loading binding %@...".fmt(this.get('content'))
                                }
                            }.property('content', 'anchor').cacheable()
                        })
                    })

                })
            })
            if (!this._debugPane.get('isPaneAttached'))
                this._debugPane.popup(this);
        }
        else {
            try {
                sc_super()
            }
            catch(e) {}

        }
    }
}