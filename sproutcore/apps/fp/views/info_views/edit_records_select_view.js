Footprint.EditRecordsSelectView = SC.ScrollView.extend({
    layout: {width:.36, left: 10, bottom: 10, top: 30},
    content: null,
    selection: null,
    /***
     * A property path relative to each item's content used for the name. Defaults to 'name'
    */
    contentNameProperty: 'name',
    /***
     * Uses the following record property or property path to determine if the record can be deleted
     */
    deletableNameProperty: null,

    contentView: SC.SourceListView.extend({
        isEnabledBinding: SC.Binding.oneWay('.content').bool(),
        rowHeight: 24,
        actOnSelect: NO,
        canReorderContent: NO,

        contentBinding: SC.Binding.oneWay('.parentView.parentView.content'),
        selectionBinding: SC.Binding.from('.parentView.parentView.selection'),

        // Show the selection so the user has any idea where they are.
        selectionDidChange: function() {
            this.invokeNext(this._selectionDidChange);
        }.observes('selection'),

        _selectionDidChange: function() {
            var sel = this.get('selection'),
                content = this.get('content'),
                selIndexes, scrollTo;
            if (sel && content) {
                selIndexes = sel.indexSetForSource(content);
                scrollTo = selIndexes ? selIndexes.get('min') : 0;
                this.scrollToContentIndex(scrollTo);
            }
        },

        exampleView: SC.View.extend(SC.Control, {
            layout: { height: 24 },
            childViews: 'nameLabelView copyButtonView deleteButtonView progressOverlayView'.w(),
            classNameBindings: ['isNew:new-record', 'isDirty:dirty-record'],

            status: null,
            statusBinding: SC.Binding.oneWay('*content.status'),

            isNew: function() {
                return this.get('status') === SC.Record.READY_NEW;
            }.property('status').cacheable(),

            isDirty: function() {
                return this.get('status') === SC.Record.READY_DIRTY;
            }.property('status').cacheable(),

            nameLabelView: SC.LabelView.extend({
                layout: { left: 48, top: 0.3 },
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                contentValueKey:'name'
            }),

            copyButtonView: Footprint.CopyButtonView.extend({
                layout: { left: 0, width: 16, centerY: 0, height: 16 },
                action: 'doCloneRecord',
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                isVisible: function() {
                    // Only allow clone on existing records
                    return (this.getPath('content.id') || 0) > 0
                }.property('content').cacheable()
            }),

            deleteButtonView: Footprint.DeleteButtonView.extend({
                layout: { left: 24, width: 16, centerY: 0, height: 16},
                action: 'doPromptDeleteRecord',
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                isVisible: function() {
                    return this.getPath('content.isDeletable');
                }.property('content').cacheable()
            }),

            progressOverlayView: Footprint.ProgressOverlayForNestedStoreView.extend({
                layout: { left:.5, width:.5, centerY: 0, height: 16},
                // Some records need to delegate to the main record, like Layer to DbEntityInterest
                record: null,
                recordBinding: SC.Binding.oneWay('.parentView.content'),
                nestedStoreContent: function() {
                    // normally this just returns record
                    return this.get('record') && this.get('record')._recordForCrudUpdates();
                }.property('record').cacheable()
            })
        })
    })
})
