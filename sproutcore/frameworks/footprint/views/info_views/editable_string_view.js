/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 10/21/13
 * Time: 10:23 AM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/editable_model_string_view');
sc_require('views/info_views/info_view');
sc_require('views/info_views/range_item_view');

Footprint.EditableStringView = Footprint.InfoView.extend({
    classNames:'footprint-editable-string-view'.w(),
    value:null,
    contentStatus:null,
    contentStatusBinding:SC.Binding.oneWay('*content.status'),

    contentView: Footprint.EditableModelStringView.extend({
        layout: {width:.99, height: 0.99},
        isEditableBinding: parentViewPath(1, '.isEditable'),
        valueBinding: parentViewPath(1, '*value')
    }),

    // Don't use the range to display string ranges
    initBindings: function() {
        this.bind('value', this, "%@".fmt(this.get('attribute')));
    }
});


Footprint.StringRangeItemView = Footprint.RangeItemView.extend({
    classNames:'footprint-string-range-item-view'.w(),
    contentView: Footprint.EditableModelStringView.extend({
        layout: {width:.99, height: 0.99},
        isEditableBinding: parentViewPath(1, '.isEditable'),
        valueBinding: parentViewPath(1, '*value')
    }),

    // Don't use the range to display string ranges
    initBindings: function() {
        this.bind('value', this, "%@".fmt(this.get('attribute')));
    }

});
