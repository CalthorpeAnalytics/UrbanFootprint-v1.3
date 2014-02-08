/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/3/13
 * Time: 5:43 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');

Footprint.BuiltFormSummaryAttributesView = SC.View.extend({
    classNames: ['footprint-built-form-summary-attributes-view'],
    childViews:'titleView dwellingUnitView singleFamilyLargeLotView singleFamilySmallLotView attachedSingleFamilyView multifamilyView employmentView retailEmploymentView officeEmploymentView industrialEmploymentView agriculturalEmploymentView'.w(),
    layout: {left: 970, height: 0.6},
    content: null,

    titleView: SC.LabelView.extend({
        layout: {top: 20, left: 10, width: 260, height:18},
        value: 'Summary Densities (per acre)'
    }),

    dwellingUnitView: Footprint.summaryFieldView.extend({
        layout: {top: 50, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.dwelling_unit_density'),
        value: 'Dwelling Unit Density',
        titleTextAlignment: SC.ALIGN_LEFT
    }),

    singleFamilyLargeLotView: Footprint.summaryFieldView.extend({
        layout: {top: 75, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.single_family_large_lot_density'),
        value: 'SF Large Lot Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    singleFamilySmallLotView: Footprint.summaryFieldView.extend({
        layout: {top: 100, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.single_family_small_lot_density'),
        value: 'SF Small Lot Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    attachedSingleFamilyView: Footprint.summaryFieldView.extend({
        layout: {top: 125, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.attached_single_family_density'),
        value: 'Attached SF Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    multifamilyView: Footprint.summaryFieldView.extend({
        layout: {top: 150, left: 10, width: 260, height:18},
        mf2to4: null,
        mf2to4Binding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.multifamily_2_to_4_density'),
        mf5plus: null,
        mf5plusBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.multifamily_5_plus_density'),

        content: function() {
            return this.get('mf5plus') + this.get('mf2to4')}.property('mf5plus', 'mf2to4').cacheable(),

        value: 'Multifamily Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    employmentView: Footprint.summaryFieldView.extend({
        layout: {top: 200, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.employment_density'),
        value: 'Employment Density',
        titleTextAlignment: SC.ALIGN_LEFT
    }),

    retailEmploymentView: Footprint.summaryFieldView.extend({
        layout: {top: 225, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.retail_density'),
        value: 'Retail Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    officeEmploymentView: Footprint.summaryFieldView.extend({
        layout: {top: 250, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.office_density'),
        value: 'Office Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    industrialEmploymentView: Footprint.summaryFieldView.extend({
        layout: {top: 275, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.industrial_density'),
        value: 'Industrial Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    agriculturalEmploymentView: Footprint.summaryFieldView.extend({
        layout: {top: 300, left: 10, width: 260, height:18},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_attribute_set.flat_building_densities.agricultural_density'),
        value: 'Agriculture Density',
        titleTextAlignment: SC.ALIGN_CENTER
    })
})