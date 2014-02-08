/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/26/13
 * Time: 4:08 PM
 * To change this template use File | Settings | File Templates.
 */

sc_require('views/info_views/built_form/editable_input_field_view');


Footprint.EditableBuildingUsePercentView = SC.View.extend({
    classNames: ['footprint-editable-building-use-percents-view'],
    childViews:'titleView buildingUsePercentScrollView'.w(),
    layout: {left: 330, height:270, top:70, width: 650},
    content: null,

    titleView: SC.LabelView.extend({
        value: 'Building Use Percents',
        layout: {left: 30, width: 150, height: 24, top: 0}
    }),

    buildingUsePercentScrollView: SC.ScrollView.extend({
        classNames: ['footprint-building-use-percent-scroll-view'],
        layout: {left: 40, width: 600, top: 25},
        contentBinding: SC.Binding.oneWay('.parentView*content'),

        contentView: SC.View.extend({
            layout: {height: 500},
            childViews:'residentialView retailView officeView industrialView'.w(),
            isEditable: YES,
            isEnabled: YES,
            content:null,
            contentBinding: SC.Binding.oneWay('.parentView*parentView.content.building_attribute_set.building_uses'),

            residentialView: SC.View.extend({
                childViews:'titleView singleFamilyLargeLotView singleFamilySmallLotView attachedSingleFamilyView multifamily2to4View multifamily5plusView'.w(),
                content:null,
                contentBinding: SC.Binding.oneWay('.parentView.content'),

                layout: {height:111, top: 0},

                titleView: SC.LabelView.extend({
                   value: 'Residential',
                   textAlign: SC.ALIGN_LEFT,
                   layout: {left: 0, height:20, top: 0},
                   backgroundColor: '#99CCFF'
                }),
                singleFamilyLargeLotView: Footprint.EditableBuildingUseFieldView.extend({
                    title: 'Single Family Large Lot (> 5500 sqft per unit)',
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 21, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Single Family Large Lot'

                }),
                singleFamilySmallLotView:Footprint.EditableBuildingUseFieldView.extend({
                    title: 'Single Family Small Lot (< 5500 sqft per unit)',
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 39, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Single Family Small Lot'

                }),
                attachedSingleFamilyView:Footprint.EditableBuildingUseFieldView.extend({
                    title: 'Attached Single Family',
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 57, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Attached Single Family'
                }),
                multifamily2to4View:Footprint.EditableBuildingUseFieldView.extend({
                    title: 'Multifamily 2 to 4 Units',
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 75, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Multifamily 2 To 4'
                }),
                multifamily5plusView:Footprint.EditableBuildingUseFieldView.extend({
                    title: 'Multifamily 5 Plus Units',
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 93, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Multifamily 5 Plus'
                })
            }),

            retailView: SC.View.extend({
                childViews:'retailTitleView retailServicesView restaurantView accommodationView artsEntertainmentView otherServicesView'.w(),
                content:null,
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                layout: {height:111, top: 111},

                retailTitleView: SC.LabelView.extend({
                   value: 'Retail Employment',
                   fontWeight: 700,
                   textAlign: SC.ALIGN_LEFT,
                   layout: {left: 0, height:20, top: 0},
                   backgroundColor: '#99CCFF'
                }),
                retailServicesView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 21, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Retail Services'
                }),
                restaurantView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 39, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Restaurant'
                }),
                accommodationView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 57, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Accommodation'
                }),
                artsEntertainmentView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 75, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Arts Entertainment'
                }),
                otherServicesView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 93, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Other Services'
                })
            }),
            officeView: SC.View.extend({
                childViews:'officeTitleView officeServicesView publicAdminView educationServicesView medicalServicesView'.w(),
                content:null,
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                layout: {height:93, top: 222},

                officeTitleView: SC.LabelView.extend({
                   value: 'Office Employment',
                   fontWeight: 700,
                   textAlign: SC.ALIGN_LEFT,
                   layout: {left: 0, height:20, top: 0},
                   backgroundColor: '#99CCFF'
                }),
                officeServicesView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 21, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Office Services'
                }),
                publicAdminView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 39, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Public Admin'
                }),

                educationServicesView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 57, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Education Services'
                }),

                medicalServicesView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 75, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Medical Services'
                })
            }),
            industrialView: SC.View.extend({
                childViews:'industrialTitleView manufacturingView wholesaleView transportWarehousingServicesView constructionUtilitiesView agricultureView extractionView'.w(),
                content:null,
                contentBinding: SC.Binding.oneWay('.parentView.content'),
                layout: {height:128, top: 315},

                industrialTitleView: SC.LabelView.extend({
                   value: 'Industrial/Agriculture Employment',
                   textAlign: SC.ALIGN_LEFT,
                   layout: {height:20, top: 0},
                   backgroundColor: '#99CCFF'

                }),
                manufacturingView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 21, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Manufacturing'
                }),
                wholesaleView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 39, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Wholesale'
                }),
                transportWarehousingServicesView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 57, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Transport Warehousing'
                }),
                constructionUtilitiesView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 75, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Construction Utilities'
                }),
                agricultureView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 93, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Agriculture'
                }),
                extractionView:Footprint.EditableBuildingUseFieldView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    layout: {top: 111, height: 17},
                    buildingUseProperty: 'percent',
                    category: 'Extraction'
                })
            })
        })
    })
})