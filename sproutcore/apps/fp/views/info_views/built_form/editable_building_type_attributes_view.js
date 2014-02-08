/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/5/13
 * Time: 12:32 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/info_views/built_form/built_form_color_picker_view');

Footprint.EditableBuildingTypeAttributesView = SC.View.extend({

    classNames: ['footprint-editable-building-type-attributes-view'],
    childViews:'titleView duAcreTitleView empAcreTitleView usePctTitleView buildingTypePercentScrollView BuiltFormColorPickerView'.w(),
    layout: {bottom: 40, left: 340, right: 280, top:70},

    titleView: SC.LabelView.extend({
        value: 'Included Buildings in Building Type',
        layout: {left: 30, width: 250, height: 24, top: 0}
    }),

    duAcreTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-building-type-attributes-du-label'],
        layout: {width: 50, height: 22, left: 458, top: 10},
        value: 'Du/Acre'
    }),

    empAcreTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-building-type-attributes-emp-label'],
        layout: {width: 50, height: 22, left: 500, top: 10},
        value: 'Emp/Acre'
    }),

    usePctTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-building-type-attributes-use-pct-label'],
        layout: {width: 50, height: 22, left: 575, top: 10},
        value: 'Use Pct'
    }),

    buildingTypePercentScrollView: SC.ScrollView.extend({
        classNames: ['footprint-building-type-percent-scroll-view'],
        layout: {left: 40, width: 600, top: 25, height: 200},
        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 20,
            isEditable: YES,
            actOnSelect: NO,
            canEditContent: YES,
            canDeleteContent: YES,
            canReorderContent: YES,
            contentBinding: SC.Binding.oneWay('Footprint.buildingTypesEditController*selection.firstObject.primary_component_percents'),
            selectionBinding: SC.Binding.from('Footprint.buildingTypesEditController.selection.firstObject'),
            contentValueKey: 'name',

            exampleView: Footprint.editableBuiltFormSourceListView.extend({
                nameValueBinding:SC.Binding.oneWay('*content.primary_component.name'),
                duValueBinding:SC.Binding.oneWay('*content.primary_component.building_attribute_set.flat_building_densities.dwelling_unit_density'),
                empValueBinding:SC.Binding.oneWay('*content.primary_component.building_attribute_set.flat_building_densities.employment_density'),
                percentValueBinding: '*content.percent'
            })
        })
    }),

    BuiltFormColorPickerView: Footprint.BuiltFormColorPickerView.extend({
        selectionBinding: SC.Binding.oneWay('Footprint.buildingTypesEditController*selection.firstObject')
    })
})