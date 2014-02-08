


Footprint.editableInputFieldView = SC.View.extend({
    classNames: ['footprint-editable-input-view'],
    childViews:'NameTitleView ContentView'.w(),
    value: null,
    content: null,
    layout: null,

    NameTitleView: SC.LabelView.extend({
        valueBinding: SC.Binding.oneWay('.parentView.value'),
        layout: {left:.01, width:.59}
    }),
    ContentView: Footprint.EditableModelStringView.extend({
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.content'),
        layout: {left:.6},
        hint: '--',
        backgroundColor: '#F8F8F8'
    })
})


Footprint.summaryFieldView = SC.View.extend({
    classNames: ['footprint-summary-field-view'],
    childViews:'nameTitleView contentView'.w(),
    value: null,
    content: null,
    layout: null,
    rawData: null,
    titleTextAlignment: null,

    nameTitleView: SC.LabelView.extend({
        textAlignBinding: SC.Binding.oneWay('.parentView.titleTextAlignment'),
        valueBinding: SC.Binding.oneWay('.parentView.value'),
        layout: {width:.65},
        backgroundColor: '#99CCFF'
    }),
    contentView: SC.LabelView.extend({
        textAlign: SC.ALIGN_CENTER,
        rawData: null,
        rawDataBinding: SC.Binding.oneWay('.parentView.content'),
        value: function(){
            var value = this.get('rawData')
            if (value)
                return parseFloat(this.get('rawData')).toFixed(1);
            return '--'
        }.property('rawData').cacheable(),
        layout: {left:.65},
        hintEnabled: YES,
        hint: '0',
        backgroundColor: '#F8F8F8'
    })
})


Footprint.editableTableField= SC.View.extend({
    classNames: ['footprint-editable-table-row-view'],
    childViews:'NameTitleView ContentView'.w(),
    content: null,
    layout: null,
    title: null,

    NameTitleView: SC.LabelView.extend({
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {left: 0, width: 0.8, height: 17},
        backgroundColor: '#E0E0E0'
    }),
    ContentView: Footprint.EditableModelStringView.extend({
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.content'),
        layout: {left: 0.8, height: 17},
        hint: '--',
        backgroundColor: '#F8F8F8'
    })
})


Footprint.editableUseTypeRowView = SC.View.extend({
    childViews:'useTypeNameView efficiencyView sqftUnitView'.w(),
    layout: null,
    use: null,
    efficiencyValue: null,
    sqftValue: null,

    useTypeNameView: SC.LabelView.extend({
        valueBinding: SC.Binding.oneWay('.parentView.use'),
        layout: {left: 6, top: 3, width: 0.35},
        textAlign: SC.ALIGN_LEFT
    }),
    efficiencyView:  Footprint.EditableModelStringView.extend({
        valueBinding: SC.Binding.oneWay('.parentView.efficiencyValue'),
        layout: {left: 0.35, width: 0.25},
        hint: '--',
        textAlign: SC.ALIGN_CENTER,
        backgroundColor: '#F8F8F8'
    }),
    sqftUnitView:  Footprint.EditableModelStringView.extend({
        valueBinding: SC.Binding.oneWay('.parentView.sqftValue'),
        textAlign: SC.ALIGN_CENTER,
        layout: {left: 0.6, width: 0.4},
        hint: '--',
        backgroundColor: '#F8F8F8'
    })
})



Footprint.editableBuiltFormSourceListView = SC.View.extend(SC.Control, {
    classNames: ['footprint-built-form-percent-list-scroll-view'],
    layout: { height: 24 },
    childViews: 'nameLabelView dwellingUnitLabelView employmentLabelView percentLabelView'.w(),
    duValue: null,
    empValue: null,
    nameValue: null,
    percentValue: null,

    nameLabelView: SC.LabelView.extend({
        layout: { left: 0, width:.69 },
        valueBinding: SC.Binding.oneWay('.parentView.nameValue')

    }),
    dwellingUnitLabelView: SC.LabelView.extend({
        layout: { left: 0.69, width:.08 },

        rawData: null,
        rawDataBinding: SC.Binding.oneWay('.parentView.duValue'),
        value: function(){
            return parseFloat(this.get('rawData')).toFixed(1);
        }.property('rawData').cacheable(),
        backgroundColor: '#F0F8FF',
        textAlign: SC.ALIGN_CENTER
    }),
    employmentLabelView: SC.LabelView.extend({
        layout: { left: 0.77, width:.08 },
        rawData: null,
        rawDataBinding: SC.Binding.oneWay('.parentView.empValue'),
        value: function(){
            return parseFloat(this.get('rawData')).toFixed(1);
        }.property('rawData').cacheable(),
        backgroundColor: '#F0F8FF',
        textAlign: SC.ALIGN_CENTER
    }),

    percentLabelView: SC.LabelView.extend({
        layout: { left: 0.85 },
        rawData: null,
        rawDataBinding: SC.Binding.oneWay('.parentView.percentValue'),
        value: function(){
            return parseFloat(this.get('rawData')).toFixed(2);
        }.property('rawData').cacheable(),
        backgroundColor: '#F0F8FF',
        textAlign: SC.ALIGN_CENTER
    })
})


Footprint.EditableBuildingUseFieldView = SC.View.extend({

    classNames: ['footprint-editable-list-view'],
    childViews:'nameTitleView contentView'.w(),
    content: null,
    layout: null,
    buildingUseProperty: null,
    category: null,


    nameTitleView: SC.LabelView.extend({
        valueUpdateObserver: function () {
            if (this.get('content')) {
                this.setPath('parentView.parentView.layerNeedsUpdate', YES);
                this.setPath('parentView.layerNeedsUpdate', YES);
                this.set('layerNeedsUpdate', YES);
            }
        }.observes('.content'),
        valueBinding: SC.Binding.oneWay('.parentView.category'),
        layout: {left: 0, width: 0.8, height: 17}
    }),
    contentView: SC.LabelView.extend({
        textAlign: SC.ALIGN_CENTER,
        buildingUseProperty: null,
        buildingUsePropertyBinding: SC.Binding.oneWay('.parentView.buildingUseProperty'),
        category: null,
        categoryBinding: SC.Binding.oneWay('.parentView.category'),
        content: null,
        contentBinding:SC.Binding.oneWay('.parentView.content'),
        value: function(){
            var buildingUseProperty = this.get('buildingUseProperty');
            var category = this.get('category');
            var content = this.get('content');
            if (!content)
                return '--';
            var building_attribute_set = content.filter(function(building_use,i) {
                return building_use.getPath('building_use_definition.name') == category})[0];
            if (!building_attribute_set)
                return '--'
            return building_attribute_set.get(buildingUseProperty);
        }.property('content', 'category', 'buildingUseProperty', 'building_use_definition.name').cacheable(),

        layout: {left: 0.8, height: 17},
        backgroundColor: '#F8F8F8',
        classNameBindings: ['isEditable'], // adds the is-editable when isEditable is YES
        isEditable:YES,
        needsEllipsis:YES,
        renderDelegateName:'ellipsesLabelRenderDelegate',
        mouseDown: function(evt) {
            // Capture the event if it's a double click and we are editable.
            return this.get('isEditable') && evt.clickCount === 2;
        }
    })
})






