Footprint.EditableInputFieldView = SC.View.extend({
    classNames: ['footprint-editable-input-view'],
    childViews:'nameTitleView contentView'.w(),
    titles: null,
    content: null,
    contentValueKey: null,
    layout: null,

    nameTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-11font-title-view'],
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {left:.01, width:.7}
    }),
    contentView: Footprint.EditableModelStringView.extend({
        textAlign: SC.ALIGN_CENTER,
        layout: {left:.7},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKeyBinding: SC.Binding.oneWay('.parentView.contentValueKey'),
        hint: '--',
        backgroundColor: '#f0f8ff'
    })
})


Footprint.LeftEditableInputFieldView = SC.View.extend({
    childViews:'nameTitleView contentView'.w(),
    titles: null,
    decimalValue: null,
    layout: null,
    contentLayout: null,
    contentLabel: null,
    isPercent: NO,

    nameTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-title-view'],
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {left:.38, width:.69}
    }),
    contentView: SC.View.extend({
        classNames: ['footprint-editable-content-view'],
        childViews:['editablePercentView', 'percentLabel'],
        layoutBinding: SC.Binding.oneWay('.parentView.contentLayout'),
        contentLabel: null,
        contentLabelBinding: SC.Binding.oneWay('.parentView.contentLabel'),
        content: null,
        contentBinding: SC.Binding.from('.parentView.decimalValue'),
        isPercent: null,
        isPercentBinding: SC.Binding.from('.parentView.isPercent'),

        editablePercentView: Footprint.EditableModelStringView.extend({
            layout: {width:.75},
            textAlign: SC.ALIGN_CENTER,
            contentBinding: SC.Binding.from('.parentView.content'),
            isPercent: null,
            isPercentBinding: SC.Binding.from('.parentView.isPercent'),
            value: function(propKey, value) {
                if (this.get('isPercent')) {
                    if (value) {
                        // parse the float and round. This eliminates anything the user enters beyond 2 decimal places.
                        var roundedValue = parseFloat(value).toFixed(0);
                        // Parse the rounded value and divide to a decimal for setting
                        this.set('content', parseFloat(roundedValue)/100);

                        // Still return the percent with rounding
                        return roundedValue;
                    }
                    else {
                        // Multiply to a percent
                        return (100*parseFloat(this.get('content'))).toFixed(0);
                    }
                }
                else {
                    if (value) {
                        // parse the float and round. This eliminates anything the user enters beyond 2 decimal places.
                        var roundedValue = parseFloat(value).toFixed(0);
                        // Parse the rounded value and divide to a decimal for setting
                        this.set('content', parseFloat(roundedValue));

                        // Still return the percent with rounding
                        return roundedValue;
                    }
                    else {
                        // Multiply to a percent
                        return (parseFloat(this.get('content'))).toFixed(0);
                    }

                }
            }.property('content').cacheable(),

            hint: '--'
        }),
        percentLabel: SC.LabelView.extend({
            classNames: ['footprint-editable-title-view'],
            layout: {left: .75, top: 1, bottom: 1},
            textAlign: SC.ALIGN_CENTER,
            valueBinding: SC.Binding.oneWay('.parentView.contentLabel'),
            backgroundColor: '#f0f8ff'
        })

    })
})


Footprint.EditableUsePercentFieldView = SC.View.extend(SC.Control, {
    classNames: ['footprint-editable-use-percent-field-view'],
    childViews: ['removeButtonView', 'nameView', 'sqftUnitView', 'efficiencyView', 'percentView'],

    content: null,
    decimalValue: null,

    removeButtonView: Footprint.DeleteButtonView.extend({
        layout: { left: 0, width: 16, centerY: 0, height: 16},
        action: 'doRemoveRecord',
        contentBinding: SC.Binding.oneWay('.parentView.content')
    }),

    nameView: SC.LabelView.extend({
        layout: {width:190, top: 1, left: 26},
        contentBinding: SC.Binding.oneWay('.parentView*content.building_use_definition'),
        contentValueKey: 'name'
    }),
    sqftUnitView: Footprint.EditableModelStringView.extend({
        classNames: ['footprint-editable-content-view'],
        layout: {width: 100, left: 190, top: 1},
        textAlign: SC.ALIGN_CENTER,
        contentBinding: SC.Binding.from('.parentView.content'),
        contentValueKey: 'square_feet_per_unit',
        hint: '--'
    }),
    efficiencyView: Footprint.EditableModelStringView.extend({
        classNames: ['footprint-editable-content-view'],
        layout: {width: 100, left: 341, top: 1},
        childViews:['editablePercentView', 'percentLabel'],
        content: null,
        contentBinding: SC.Binding.from('.parentView.content'),

        editablePercentView: Footprint.EditableModelStringView.extend({
            classNames: ['footprint-content-view'],
            layout: {width: 84},
            textAlign: SC.ALIGN_CENTER,
            contentBinding: SC.Binding.from('.parentView*content.efficiency'),
            value: function(propKey, value) {
                if (value) {
                    // parse the float and round. This eliminates anything the user enters beyond 2 decimal places.
                    var roundedValue = parseFloat(value).toFixed(0);
                    // Parse the rounded value and divide to a decimal for setting
                    this.set('content', parseFloat(roundedValue)/100);

                    // Still return the percent with rounding
                    return roundedValue;
                }
                else {
                    // Multiply to a percent
                    return (100*parseFloat(this.get('content'))).toFixed(0);
                }
            }.property('content').cacheable(),

            hint: '--'
        }),
        percentLabel: SC.LabelView.extend({
            layout: {left: 84, top: 1, bottom: 1},
            textAlign: SC.ALIGN_CENTER,
            value: '%',
            backgroundColor: '#f0f8ff'
        })
    }),

    percentView: SC.View.extend({
        layout: {width: 100, left: 490, top: 1},
        classNames: ['footprint-editable-content-view'],
        childViews:['editablePercentView', 'percentLabel'],
        content: null,
        contentBinding: SC.Binding.from('.parentView.decimalValue'),

        editablePercentView: Footprint.EditableModelStringView.extend({
            classNames: ['footprint-content-view'],
            layout: {width: 84},
            textAlign: SC.ALIGN_CENTER,
            contentBinding: SC.Binding.from('.parentView.content'),
            value: function(propKey, value) {
                if (value) {
                    // parse the float and round. This eliminates anything the user enters beyond 2 decimal places.
                    var roundedValue = parseFloat(value).toFixed(0);
                    // Parse the rounded value and divide to a decimal for setting
                    this.set('content', parseFloat(roundedValue)/100);

                    // Still return the percent with rounding
                    return roundedValue;
                }
                else {
                    // Multiply to a percent
                    return (100*parseFloat(this.get('content'))).toFixed(0);
                }
            }.property('content').cacheable(),

            hint: '--'
        }),
        percentLabel: SC.LabelView.extend({
            layout: {left: 84, top: 1, bottom: 1},
            textAlign: SC.ALIGN_CENTER,
            value: '%',
            backgroundColor: '#f0f8ff'
        })
    })
})


Footprint.EditableFieldView = SC.View.extend(SC.Control, {
    classNames: ['footprint-editable-view'],
    childViews:'nameTitleView contentView'.w(),
    title: null,
    content: null,
    contentValueKey: null,
    layout: null,

    nameTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-title-view'],
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {height:0.4}
    }),
    contentView: Footprint.EditableModelStringView.extend({
        classNames: ['footprint-editable-content-view'],
        textAlign: SC.ALIGN_CENTER,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKeyBinding: SC.Binding.oneWay('.parentView.contentValueKey'),
        layout: {top:.4, width: 100},
        hint: '--'
    })
})

Footprint.EditableBottomLabelledView = SC.View.extend(SC.ContentDisplay, {
    classNames: ['footprint-bottom-labelled-view'],
    childViews:'nameTitleView contentView'.w(),
    title: null,
    content:null,
    contentValueKey: null,
    layout: null,

    nameTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-10font-title-view'],
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {top:0.6}
    }),
    contentView: Footprint.EditableModelStringView.extend({
        classNames: ['footprint-bottom-labelled-content-view'],
        classNameBindings: ['positiveNegative:is-negative'],
        positiveNegative: function() {
            return this.get('value') < 0
        }.property('value').cacheable(),
        textAlign: SC.ALIGN_CENTER,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKeyBinding: SC.Binding.oneWay('.parentView.contentValueKey'),
        layout: {height:.5}
    })
})

Footprint.NonEditableBottomLabelledView = SC.View.extend(SC.ContentDisplay, {
    classNames: ['footprint-bottom-labelled-view'],
    childViews:'nameTitleView contentView'.w(),
    status: null,
    title: null,
    content:null,
    contentValueKey: null,
    layout: null,

    nameTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-10font-title-view'],
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {top:0.6}
    }),
    contentView: SC.LabelView.extend({
        classNames: ['footprint-noneditable-bottom-labelled-content-view'],
        classNameBindings: ['positiveNegative:is-negative'],
        positiveNegative: function() {
            return this.get('value') < 0
        }.property('value').cacheable(),
        textAlign: SC.ALIGN_CENTER,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKeyBinding: SC.Binding.oneWay('.parentView.contentValueKey'),
        layout: {height:.5}
    })
})


Footprint.EditableTableField= SC.View.extend({
    classNames: ['footprint-editable-table-row-view'],
    childViews:'nameTitleView contentView'.w(),
    content: null,
    contentValueKey: null,
    layout: null,
    title: null,

    nameTitleView: SC.LabelView.extend({
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {left: 0, width: 0.8, height: 17},
        backgroundColor: '#E0E0E0'
    }),
    contentView: Footprint.EditableModelStringView.extend({
        textAlign: SC.ALIGN_CENTER,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        contentValueKeyBinding: SC.Binding.oneWay('.parentView.contentValueKey'),
        layout: {left: 0.8, height: 17},
        hint: '--',
        backgroundColor: '#F8F8F8'
    })
})

Footprint.EditableBuildingUsePercentRowView = SC.View.extend({
    childViews:'useTypeNameView efficiencyView sqftUnitView'.w(),
    layout: null,
    use: null,
    // The BuildingUsePercent array
    content: null,
    /***
     * The parent buildingUsePercent whose values are shown in efficiencyValue and sqftValue
     * When either of those values are updated, values are also set upon the children of the buildingUsePercent
     */
    buildingUsePercent: function() {
        if (!this.get('content'))
            return null;
        var buildingUsePercent = this.get('content').filter(function(buildingUsePercent, i) {
            return buildingUsePercent.getPath('building_use_definition.name') == category})[0];
        if (!buildingUsePercent)
            return null;
        return buildingUsePercent;
    }.property('content').cacheable(),
    efficiencyValue: null,
    efficiencyValueBinding: SC.Binding.oneWay('.parentView.content').propertyTransform('efficiency', 'Residential'),
    sqftValue: null,
    sqftValueBinding: SC.Binding.oneWay('.parentView.content').propertyTransform('square_feet_per_unit', 'Residential'),


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
});





Footprint.NonEditableValueBottomLabelledView = SC.View.extend(SC.ContentDisplay, {
    classNames: ['footprint-bottom-labelled-view'],
    childViews:'nameTitleView contentView'.w(),
    status: null,
    title: null,
    value:null,
    layout: null,

    nameTitleView: SC.LabelView.extend({
        classNames: ['footprint-editable-10font-title-view'],
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.title'),
        layout: {top:0.6}
    }),
    contentView: SC.LabelView.extend({
        classNames: ['footprint-noneditable-bottom-labelled-content-view'],
        classNameBindings: ['positiveNegative:is-negative'],
        positiveNegative: function() {
            return this.get('value') < 0
        }.property('value').cacheable(),
        textAlign: SC.ALIGN_CENTER,
        valueBinding: SC.Binding.oneWay('.parentView.value'),
        layout: {height:.5}
    })
})
