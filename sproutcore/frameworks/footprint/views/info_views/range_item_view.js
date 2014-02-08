/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 10/21/13
 * Time: 10:26 AM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/info_views/info_view');

Footprint.RangeItemView = Footprint.InfoView.extend({
    classNames:'footprint-range-item-view'.w(),

    value:null,
    rangeValue:null,
    contentStatus:null,
    contentStatusBinding:SC.Binding.oneWay('*content.status'),

    init: function() {
        sc_super();
        // Bind value to the attribute {value} property
        this.bind('value', this, this.get('attribute'));
        // Bind rangeValue to the attribute {value}__range property
        this.bind('rangeValue', this, "%@__range".fmt(this.get('attribute'))).oneWay();
    }
});
