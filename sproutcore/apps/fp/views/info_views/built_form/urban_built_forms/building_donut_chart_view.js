/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 2/26/14
 * Time: 2:20 PM
 * To change this template use File | Settings | File Templates.
 */

Footprint.buildingParcelAreaChartView = SC.View.design(SC.ContentDisplay, {
    classNames : ['buildingParcelChart'],

    displayProperties: ['content', 'selectedItem', 'status', 'buildingFootprint', 'parkingSpace', 'otherHardscape', 'nonIrrigated', 'irrigated', 'lotSqft'],
    content: null,
    selectedItem: null,
    status: null,
    statusBinding: SC.Binding.oneWay('*selectedItem.status'),

    buildingFootprint: null,
    parkingSpace: null,
    otherHardscape: null,
    nonIrrigated: null,
    irrigated: null,
    lotSqft: null,

    buildingFootprintBinding: SC.Binding.oneWay('*content.building_footprint_square_feet'),
    parkingSpaceBinding: SC.Binding.oneWay('*content.surface_parking_square_feet'),
    otherHardscapeBinding: SC.Binding.oneWay('*content.hardscape_other_square_feet'),
    nonIrrigatedBinding: SC.Binding.oneWay('*content.nonirrigated_softscape_square_feet'),
    irrigatedBinding: SC.Binding.oneWay('*content.irrigated_softscape_square_feet'),
    lotSqftBinding: SC.Binding.oneWay('*content.lot_size_square_feet'),

    update: function(context) {
        if (this.getPath('selectedItem.status') & SC.Record.READY) {

            this._buildingParcelUseCategories = [];

            var building_footprint_pct = parseFloat(this.getPath('content.building_footprint_square_feet')) / parseFloat(this.getPath('content.lot_size_square_feet'))
            var surface_parking_pct = parseFloat(this.getPath('content.surface_parking_square_feet')) / parseFloat(this.getPath('content.lot_size_square_feet'))
            var other_hardscape_pct = parseFloat(this.getPath('content.hardscape_other_square_feet')) / parseFloat(this.getPath('content.lot_size_square_feet'))

            var non_irrigated_pct = parseFloat(this.getPath('content.nonirrigated_softscape_square_feet')) / parseFloat(this.getPath('content.lot_size_square_feet'))

            var irrigated_pct = parseFloat(this.getPath('content.irrigated_softscape_square_feet')) / parseFloat(this.getPath('content.lot_size_square_feet'))

            var dataManager = d3.building.dataManager();
            //dataManager contains the helper function "createDataObject"
            //dataObjects represent the pieces of the pie chart, and contain "category" and "percentage" attributes

            // for each of the landUse categories within the flat built form,
            // gets percentage data from API
            // creates data object with "category" and "percentage" attributes,
            // adds to array of landUseCategories

            this._buildingParcelUseCategories.push(
                dataManager.createDataObject("Building Footprint", building_footprint_pct),
                dataManager.createDataObject("Surface Parking", surface_parking_pct),
                dataManager.createDataObject("Other Hardscape", other_hardscape_pct),
                dataManager.createDataObject("Non-Irrigated Softscape", non_irrigated_pct),
                dataManager.createDataObject("Irrigated Softscape", irrigated_pct)
            );

            // d3.building.donutChart is a function that takes a div bound with data as an argument
            // we select the div that will hold the chart (using the context); bind the data (this._landUseCategories),
            // and then call the donutChartMaker function
            d3.selectAll(context).datum(this._buildingParcelUseCategories)
                .call(d3.building.buildingDonutChart());
        }
    }
})