/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/5/13
 * Time: 12:32 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/info_views/built_form/built_form_color_picker_view');

Footprint.EditablePlacetypeAttributesView = SC.View.extend({

    classNames: ['footprint-editable-placetypes-attributes-view'],
    childViews:'titleView placetypePercentScrollView BuiltFormColorPickerView'.w(),
    layout: {bottom: 40, left: 340, right: 280, top:70},

    titleView: SC.LabelView.extend({
        value: 'Included Building Types in Placetype',
        layout: {left: 30, width: 250, height: 24, top: 0}
    }),

    placetypePercentScrollView: SC.ScrollView.extend({
        classNames: ['footprint-placetype-percent-scroll-view'],
        layout: {left: 40, width: 590, top: 25, height: 200},

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 20,
            isEditable: YES,
            actOnSelect: NO,
            canEditContent: YES,
            canDeleteContent: YES,
            canReorderContent: YES,
            contentBinding: SC.Binding.oneWay('Footprint.placetypesEditController*selection.firstObject.placetype_component_percents'),
            selectionBinding: SC.Binding.from('Footprint.placetypesEditController.selection.firstObject'),
            contentValueKey: 'name',

            exampleView: Footprint.editableBuiltFormSourceListView.extend({
                nameValueBinding:SC.Binding.oneWay('*content.placetype_component.name'),
                duValueBinding:SC.Binding.oneWay('*content.placetype_component.building_attribute_set.flat_building_densities.dwelling_unit_density'),
                empValueBinding:SC.Binding.oneWay('*content.placetype_component.building_attribute_set.flat_building_densities.employment_density'),
                percentValueBinding: SC.Binding.oneWay('*content.percent')
            })
        })
    }),

    BuiltFormColorPickerView: Footprint.BuiltFormColorPickerView
})