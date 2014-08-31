/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/3/13
 * Time: 5:43 PM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/built_form/editable_input_field_view');
sc_require('views/info_views/built_form/urban_built_forms/built_form_summary_field_view');

Footprint.BuiltFormSummaryAttributesView = SC.View.extend({
    classNames: ['footprint-built-form-summary-attributes-view'],
    childViews:'titleView dwellingUnitView singleFamilyLargeLotView singleFamilySmallLotView attachedSingleFamilyView multifamilyView employmentView retailEmploymentView officeEmploymentView publicEmploymentView industrialEmploymentView agriculturalEmploymentView militaryEmploymentView'.w(),
    content: null,
    status: null,
    componentType: null,
    componentPercentObserver: null,
    editController: null,

    titleView: SC.LabelView.extend({
        classNames: ['footprint-bold-title-view'],
        layout: {top: 10, left: 10, height:18},
        value: 'Summary Densities'
    }),

    dwellingUnitView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 50, left: 10, height:18},

        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.single_family_large_lot_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.single_family_small_lot_density'),
        field3Property: null,
        field3PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.attached_single_family_density'),
        field4Property: null,
        field4PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.multifamily_2_to_4_density'),
        field5Property: null,
        field5PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.multifamily_5_plus_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.single_family_large_lot_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.single_family_small_lot_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.attached_single_family_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.multifamily_2_to_4_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.multifamily_5_plus_density'))
                ).toFixed(1)
            }
        }.property('flatBuiltFormStatus', 'field1Property', 'field2Property', 'field3Property', 'field4Property', 'field5Property').cacheable(),
        value: 'Dwelling Unit Density',
        titleTextAlignment: SC.ALIGN_LEFT
    }),

    singleFamilyLargeLotView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 75, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.single_family_large_lot_density'),
        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'single_family_large_lot_density', this.get('componentType'))

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }
        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),


        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return this.getPath('content.flat_building_densities.single_family_large_lot_density').toFixed(1)
            }
        }.property('flatBuiltFormStatus', 'field1Property').cacheable(),
        value: 'Single Family Large Lot',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    singleFamilySmallLotView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 100, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.single_family_small_lot_density'),
        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'single_family_small_lot_density', this.get('componentType'))

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),


        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return this.getPath('content.flat_building_densities.single_family_small_lot_density').toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'field1Property').cacheable(),

        value: 'SF Small Lot Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    attachedSingleFamilyView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 125, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.attached_single_family_density'),
        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'attached_single_family_density', this.get('componentType'))

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),


        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return this.getPath('content.flat_building_densities.attached_single_family_density').toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'field1Property').cacheable(),
        value: 'Attached SF Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    multifamilyView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 150, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.multifamily_2_to_4_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.multifamily_5_plus_density'),
        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'multifamily_2_to_4_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'multifamily_5_plus_density', this.get('componentType'));

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    this.getPath('content.flat_building_densities.multifamily_2_to_4_density') +
                    this.getPath('content.flat_building_densities.multifamily_5_plus_density')
                    ).toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'status', 'field1Property' , 'field2Property').cacheable(),

        value: 'Multifamily Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    employmentView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 200, left: 10, height:18},
        cfield1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.retail_services_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.accommodation_density'),
        field3Property: null,
        field3PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.arts_entertainment_density'),
        field4Property: null,
        field4PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.other_services_density'),
        field5Property: null,
        field5PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.restaurant_density'),

        field6Property: null,
        field6PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.office_services_density'),
        field7Property: null,
        field7PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.public_admin_density'),
        field8Property: null,
        field8PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.education_services_density'),
        field9Property: null,
        field9PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.medical_services_density'),
        field10Property: null,
        field10PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.manufacturing_density'),

        field11Property: null,
        field11PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.wholesale_density'),
        field12Property: null,
        field12PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.transport_warehouse_density'),
        field13Property: null,
        field13PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.construction_utilities_density'),
        field14Property: null,
        field14PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.agriculture_density'),
        field15Property: null,
        field15PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.extraction_density'),
        field16Property: null,
        field16PropertyBinding: SC.Binding.oneWay('*content.flat_building_densities.armed_forces_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),
        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.retail_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.accommodation_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.arts_entertainment_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.other_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.restaurant_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.office_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.public_admin_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.education_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.medical_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.manufacturing_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.wholesale_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.transport_warehouse_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.construction_utilities_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.agriculture_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.extraction_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.armed_forces_density'))
                    ).toFixed(1)
            }
        }.property('flatBuiltFormStatus', 'field1Property', 'field2Property', 'field3Property', 'field4Property' , 'field5Property', 'field6Property', 'field7Property', 'field8Property', 'field9Property' , 'field10Property', 'field11Property', 'field12Property', 'field13Property', 'field14Property' , 'field15Property', 'field16Property' ).cacheable(),
        value: 'All Employment',
        titleTextAlignment: SC.ALIGN_LEFT
    }),

    retailEmploymentView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 225, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.retail_services_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.accommodation_density'),
        field3Property: null,
        field3PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.arts_entertainment_density'),
        field4Property: null,
        field4PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.other_services_density'),
        field5Property: null,
        field5PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.restaurant_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'retail_services_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'accommodation_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'arts_entertainment_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'other_services_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'restaurant_density', this.get('componentType'));

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.retail_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.accommodation_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.arts_entertainment_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.other_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.restaurant_density'))
                    ).toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'field1Property', 'field2Property', 'field3Property', 'field4Property' , 'field5Property').cacheable(),
        value: 'Retail Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    officeEmploymentView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 250, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.office_services_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.medical_services_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView..status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'office_services_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'medical_services_density', this.get('componentType'));

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.office_services_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.medical_services_density'))
                    ).toFixed(1)
            }
        }.property('flatBuiltFormStatus', 'field1Property', 'field2Property').cacheable(),
        value: 'Office Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    publicEmploymentView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 275, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.public_admin_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.education_services_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'public_admin_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'education_services_density', this.get('componentType'));

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.public_admin_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.education_services_density'))
                    ).toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'field1Property', 'field2Property').cacheable(),
        value: 'Public Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    industrialEmploymentView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 300, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.manufacturing_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.wholesale_density'),
        field3Property: null,
        field3PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.transport_warehouse_density'),
        field4Property: null,
        field4PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.construction_utilities_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'manufacturing_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'wholesale_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'transport_warehouse_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'construction_utilities_density', this.get('componentType'));

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.manufacturing_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.wholesale_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.transport_warehouse_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.construction_utilities_density'))
                    ).toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'field1Property', 'field2Property', 'field3Property', 'field4Property').cacheable(),
        value: 'Industrial Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    agriculturalEmploymentView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 325, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.agriculture_density'),
        field2Property: null,
        field2PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.extraction_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView*.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'agriculture_density', this.get('componentType'));
            updateFlatBuiltForm(this.get('content'), 'extraction_density', this.get('componentType'));

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.agriculture_density')) +
                    parseFloat(this.getPath('content.flat_building_densities.extraction_density'))
                    ).toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'field1Property', 'field2Property').cacheable(),
        value: 'Agriculture Density',
        titleTextAlignment: SC.ALIGN_CENTER
    }),

    militaryEmploymentView: Footprint.BuiltFormSummaryFieldView.extend({
        layout: {top: 350, left: 10, height:18},
        editControllerBinding: SC.Binding.oneWay('.parentView.editController'),
        componentSummaryObserverBinding: SC.Binding.oneWay('.parentView.componentPercentObserver'),
        componentTypeBinding: SC.Binding.oneWay('.parentView.componentType'),
        field1Property: null,
        field1PropertyBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.armed_forces_density'),

        flatBuiltFormStatusBinding: SC.Binding.oneWay('.parentView*content.flat_building_densities.status'),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),

        computeValueObserver: function() {
            var status = this.get('status');
            var editController = this.get('editController');
            if (status != SC.Record.READY_DIRTY & status != SC.Record.READY_NEW) {
                return
            }
            updateFlatBuiltForm(this.get('content'), 'armed_forces_density', this.get('componentType'));

            if (this.get('componentSummaryObserver') == YES) {
                editController.set('updateSummaryAttributes', NO);
            }

        }.observes('content', 'status', '*content.status', 'componentSummaryObserver'),

        computedValue: function() {
            if (this.getPath('flatBuiltFormStatus') & SC.Record.READY) {
                return (
                    parseFloat(this.getPath('content.flat_building_densities.armed_forces_density'))
                    ).toFixed(1)
            }

        }.property('flatBuiltFormStatus', 'field1Property').cacheable(),
        value: 'Armed Forces Density',
        titleTextAlignment: SC.ALIGN_CENTER
    })
})