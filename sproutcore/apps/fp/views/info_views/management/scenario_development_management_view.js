/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/14/13
 * Time: 3:48 PM
 * To change this template use File | Settings | File Templates.
 */


Footprint.scenarioDevelopmentManagementView = SC.View.extend({
    classNames: "footprint-scenario-development-management-view".w(),
    childViews: 'contentView reportHighLevelView reportResidentialLowLevelView reportEmploymentLowLevelView'.w(),
    contentView: SC.SegmentedView.extend({
        layout: { top:.02, height: 0.98, left: 4, width: 80 },
        layoutDirection: SC.LAYOUT_VERTICAL,
        selectSegmentWhenTriggeringAction: YES,
        itemTitleKey: 'title',
        itemValueKey: 'value',
        items: [
                {title: 'Base Year', value: ''},
                {title: 'End State', value: ''},
                {title: 'Increments', value: ''}
        ]
    }),

    reportHighLevelView: SC.View.extend({
        layout: {top: 16, width: 400, height: 60, left: 85},
        childViews: 'dwellingUnitTitleView dwellingUnitSummaryView employmentTitleView employmentSummaryView'.w(),
        classNames: "footprint-report-high-level-values-view".w(),

        dwellingUnitTitleView: SC.LabelView.design({
            classNames: "footprint-dwelling-unit-label-view".w(),
            value: 'Dwelling Units',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            layout: {left: 55, width: 85, height: 16}

        }),
        dwellingUnitSummaryView: SC.LabelView.extend({
            classNames: "footprint-dwelling-unit-summary-view".w(),

            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 18, left: 55, width: 85, height: 30}
//            recordType:null,
//            recordTypeBinding:Footprint.Feature,
//            contentBinding: SC.Binding.oneWay('Footprint.featuresActiveDbEntityKeysController.content'),
//            selectionBinding: SC.Binding.oneWay('Footprint.featuresActiveDbEntityKeysController')

        }),

        employmentTitleView: SC.LabelView.extend({
            classNames: "footprint-employment-label-view".w(),
            value: 'Employees',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            layout: {left: 250, width: 85, height: 16}

        }),
        employmentSummaryView: SC.LabelView.extend({
            classNames: "footprint-employment-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 18, left: 250, width: 85, height: 30}
        })
    }),

    reportResidentialLowLevelView: SC.View.extend({
        layout: {top: 72, bottom: 2, left: 90, width: 200},
        classNames: "footprint-report-residential-low-level-values-view".w(),
        childViews: 'singleFamilySmallTitleView singleFamilySmallSummaryView singleFamilyLargeTitleView singleFamilyLargeSummaryView attachedTitleView attachedUnitSummaryView multifamilyUnitTitleView multifamilyUnitSummaryView'.w(),

        singleFamilySmallTitleView: SC.LabelView.design({
            classNames: "footprint-single-family-small-title-view".w(),
            value: 'Single Family Small Lot: ',
            layout: {top: 2, left: 10, width: 130, height: 16}

        }),
        singleFamilySmallSummaryView: SC.LabelView.extend({
            classNames: "footprint-single-family-small-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 2, left: 140, width: 50, height: 16}

        }),
        singleFamilyLargeTitleView: SC.LabelView.extend({
            classNames: "footprint-single-family-large-title-view".w(),
            value: 'Single Family Large Lot:',
            layout: {top: 25, left: 10, width: 130, height: 16}

        }),
        singleFamilyLargeSummaryView: SC.LabelView.extend({
            classNames: "footprint-single-family-large-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 25, left: 140, width: 50, height: 16}

        }),
        attachedTitleView: SC.LabelView.extend({
            classNames: "footprint-attached-title-view".w(),
            value: 'Attached Single Family:',
            layout: {top: 48, left: 10, width: 130, height: 16}

        }),
        attachedUnitSummaryView: SC.LabelView.extend({
            classNames: "footprint-attached-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 48, left: 140, width: 50, height: 16}

        }),
        multifamilyUnitTitleView: SC.LabelView.extend({
            classNames: "footprint-multifamily-title-view".w(),
            value: 'Multifamily:',
            layout: {top: 71, left: 10, width: 130, height: 16}

        }),
        multifamilyUnitSummaryView: SC.LabelView.extend({
            classNames: "footprint-multifamily-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 71, left: 140, width: 50, height: 16}

        })
    }),

    reportEmploymentLowLevelView: SC.View.extend({
        layout: {top: 72, bottom: 2, left: 328, width: 150},
        classNames: "footprint-report-employment-low-level-values-view".w(),
        childViews: 'retailTitleView retailSummaryView officeTitleView officeSummaryView publicTitleView publicSummaryView industrialTitleView industrialSummaryView'.w(),

        retailTitleView: SC.LabelView.design({
            classNames: "footprint-retail-title-view".w(),
            value: 'Retail: ',
            layout: {top: 2, left: 10, width: 60, height: 16}

        }),
        retailSummaryView: SC.LabelView.extend({
            classNames: "footprint-retail-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 2, left: 70, width: 50, height: 16}

        }),
        officeTitleView: SC.LabelView.extend({
            classNames: "footprint-office-title-view".w(),
            value: 'Office:',
            layout: {top: 25, left: 10, width: 60, height: 16}

        }),
        officeSummaryView: SC.LabelView.extend({
            classNames: "footprint-office-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 25, left: 70, width: 50, height: 16}

        }),
        publicTitleView: SC.LabelView.extend({
            classNames: "footprint-public-title-view".w(),
            value: 'Public:',
            layout: {top: 48, left: 10, width: 60, height: 16}

        }),
        publicSummaryView: SC.LabelView.extend({
            classNames: "footprint-public-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 48, left: 70, width: 50, height: 16}

        }),
        industrialTitleView: SC.LabelView.extend({
            classNames: "footprint-industrial-title-view".w(),
            value: 'Industrial:',
            layout: {top: 71, left: 10, width: 60, height: 16}

        }),
        industrialSummaryView: SC.LabelView.extend({
            classNames: "footprint-industrial-summary-view".w(),
            value: '5',
            textAlign: SC.ALIGN_CENTER,
            fontWeight: 700,
            backgroundColor: '#F8F8F8',
            layout: {top: 71, left: 70, width: 50, height: 16}

        })

    })

})