/* 
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2012 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

/**
 * Library of javascript calls to Highcharts specifically for the footprint
 */

const BASE_CASE = 'Base Case';
const LOCALLY_PREFERRED = 'Locally Preferred';
const VALLEY_WIDE_HYBRID = 'Valley Wide Hybrid';
const DEFAULT_SERIES_COLORS = [
        '#4572A7',
        '#AA4643',
        '#89A54E',
        '#80699B',
        '#3D96AE',
        '#DB843D',
        '#92A8CD',
        '#A47D7C',
        '#B5CA92'];
// For stacked series we use different colors to highlight the different dimensionality
const DEFAULT_STACKED_SERIES_COLORS = Array.concat([
    'orange',
    '#CC7722'],
    DEFAULT_SERIES_COLORS);

/**
 * Creates a VMT chart for the given series
 */
function createVMTChart(options) {
    barOptions = {
        title: {text: 'Vehicle Miles Traveled'},
        series: [
        ],
        tooltip: {
            formatter: function() {
                return $.format("{1}: {0} Total",
                    this.series.name,
                    Highcharts.numberFormat(this.y, 0, ','))
            }
        },
        plotOptions: {
            line: {
                // We place a label on the plotLine instead
                dataLabels: {
                    enabled:false
                }
            }
        },
        yAxis: {
            title: {
                text: 'Total VMT',
                align: 'high'
            },
            plotLines: [{
                color: '#4572A7', // Color matches first series to match legend
                width: 3,
                value: options.series[0].data[0],
                zIndex:10,
                dashStyle: 'shortDash',
                label: {
                    // Grab the first series' only data value
                    text:Highcharts.numberFormat(options.series[0].data[0], 0, ','),
                    align:'left',
                    style:{
                        fontFamily:"'Lucida Grande', 'Lucida Sans Unicode', Verdana, Arial, Helvetica, sans-serif",
                        fontSize:'11px',
                        fontWeight:'bold',
                        color:'black',
                        lineHeight:'14px',
                        fill:'black'
                    }
                }
            }]
        }
    };
    combinedOptions = $.extend(true, {}, barOptions, options);
    return createBarChart(combinedOptions)
}

/**
 * Creates an Energy chart for the given series
 */
function createEnergyChart(options) {
    barOptions = {
        title: {text: 'Energy Usage'},
        subtitle: {text: 'Total per Scenario'},
        series: [
        ],
        yAxis: {
            startOnTick: true,
            title: {
                text: 'Total kWh',
                align: 'high'
            }
        },
        tooltip: {
            formatter: function() {
                return this.point.options.perUnit ?
                    $.format("{1}: {0} per household",
                        this.series.name,
                        Highcharts.numberFormat(this.point.options.perUnit, 0, ',') ) :
                    $.format("{1}: {0} Total",
                        this.series.name,
                        Highcharts.numberFormat(this.y, 0, ','))
            }
        },
        plotOptions: {
            series: {
                dataLabels: {
                    rotation:90,
                    y:50
                }
            }
        }
    };
    combinedOptions = $.extend(true, {}, barOptions, options);
    return createBarChart(combinedOptions);
}

/**
 * Creates a Water chart for the given series
 */
function createWaterChart(options) {
    barOptions = {
        title: {text: 'Water Usage'},
        subtitle: {text: 'Total per Scenario'},
        series: [],
        yAxis: {
            startOnTick: true,
            title: {
                text: 'Total H20 (area feet)',
                align: 'high'
            }
        },
        tooltip: {
            formatter: function() {
                    return $.format("{1}: {0} per household",
                        this.series.name,
                        Highcharts.numberFormat(this.point.options.perUnit, 0, ',') )
            }
        },
        plotOptions: {
            series: {
                dataLabels: {
                    rotation:90,
                    y:50
                }
            }
        }
    };
    combinedOptions = $.extend(true, {}, barOptions, options);
    return createBarChart(combinedOptions);
}

/**
 * Creates an Infrastructure chart for the given series
 */
function createInfrastructureChart(options) {
    barOptions = {
        title: {text: 'Infrastructure'},
        subtitle: {text: 'Total Costs per Scenario'},
        series: [],
        yAxis: {
            startOnTick: true,
            title: {
                text: 'Capital + O&M ($)',
                align: 'high'
            }
        },
        tooltip: {
            formatter: function() {
                return $.format("{0}: ${1} Total",
                    this.series.name,
                    Highcharts.numberFormat(this.y, 0, ','))
            }
        },
        plotOptions: {
            series: {
                dataLabels: {
                    rotation:90,
                    y:50
                }
            }
        }
    };
    combinedOptions = $.extend(true, {}, barOptions, options);
    return createBarChart(combinedOptions);
}

function createHouseholdCosts(options) {
    barOptions = {
        title: {text: 'Household Costs'},
        subtitle: {text: 'Home Energy and Transportation Costs'},
        series: [
        ],
        xAxis: {
            categories: [BASE_CASE, LOCALLY_PREFERRED, VALLEY_WIDE_HYBRID],
            labels: {enabled:true}
        },
        yAxis: {
            min: null,
            title: {
                text: 'Household Costs ($)',
                align: 'high'
            }
        },
        tooltip: {
            formatter: function() {
                return $.format("{0}: {1} per household",
                    this.series.name,
                    Highcharts.numberFormat(this.point.options.perUnit, 0, ','))
            }
        }
    };
    combinedOptions = $.extend(true, {}, barOptions, options);
    return createStackedBarChart(combinedOptions);
}

function createGreenhouseGases(options) {
    barOptions = {
        title: {text: 'Greeenhouse Gases'},
        subtitle: {text: 'Home Energy and Transporation Emissions'},
        series: [
        ],
        xAxis: {
            categories: [BASE_CASE, LOCALLY_PREFERRED, VALLEY_WIDE_HYBRID],
            labels: {enabled:true}
        },
        yAxis: {
            min: null,
            title: {
                text: 'Greenhouse Gas (MMT C02E)',
                align: 'high'
            },
            stackLabels: {
                formatter: function() {
                    return ''+Highcharts.numberFormat(this.total, 3, '.', ',')
                }
            }
        },
        tooltip: {
            formatter: function() {
                return $.format("{0}: {1} per household",
                    this.series.name,
                    Highcharts.numberFormat(this.point.options.perUnit, 3, '.', ','))
            }
        },
        plotOptions: {
            series: {
                dataLabels: {
                    formatter: function() {
                        return Highcharts.numberFormat(this.y, 3, '.', ',')
                    }
                }
            }
        }
    };
    combinedOptions = $.extend(true, {}, barOptions, options);
    return createStackedBarChart(combinedOptions);
}
/**
 * A generic configuration for a bar chart
 */
function generalBarOptions(seriesCount) {
    return {
        chart: {
            renderTo: 'unknown',
            type: 'column'
        },
        title: {
            text: 'None'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            labels: {enabled:false},
            categories: [],
            title: {
                text:null
            }
        },
        yAxis: {
            min: null,
            title: {
                text: 'Unknown',
                align: 'high'
            },
            maxPadding: .18*seriesCount
        },
        tooltip: {
            formatter: function() {
                return Highcharts.numberFormat(this.y, 0, ',')
            }
        },
        plotOptions: {
            column: {
                groupPadding:0.30,
                dataLabels: {
                    enabled:true,
                    formatter: function() {
                        return Highcharts.numberFormat(this.y, 0, ',')
                    },
                    style: {
                        fontWeight:'bold',
                        color:'black'
                    }
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: 0,
            y: 45,
            floating: true,
            borderWidth: 1,
            backgroundColor: '#FFFFFF',
            shadow: true
        },
        exporting: {
            buttons: {
                exportButton:{
                    align:'left',
                    x:80,
                    y:54
                },
                printButton:{
                    align:'left',
                    x:110,
                    y:54
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [
        ]
    }
}

/**
 *  Create a standard bar chart extended with the given options object
 * @param options - Highcharts configuration object which provides series and optionally overrides the default bar chart options configured in generalBarOptions()
 */
function createBarChart(options) {
    combinedOptions = $.extend(true, {}, generalBarOptions(options.series.length), options);
    // Add the default series colors to the series if none are predefined
    $.dualMap(
        combinedOptions.series,
        DEFAULT_SERIES_COLORS.slice(0,combinedOptions.series.length),
        function(aSeries, color) {
            if (!aSeries['color']) {
                aSeries['color'] = color;
            }
    });
    chart = new Highcharts.Chart(
        combinedOptions
    );
}

/**
 * Create a stacked bar chart with the given options object
 * @param options - Highcharts configuration object which provides series and optionally overrides the default options
 */
function createStackedBarChart(options) {
    barOptions = $.extend(true, {},
        generalBarOptions(options.series.length),
        {
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled:true,
                        style: {
                            fontWeight:'bold'
                        }
                    }
                }
            },
            yAxis: {
                min: null,
                stackLabels: {
                    enabled:true,
                    style: {
                        fontWeight:'bold'
                    },
                    formatter: function() {
                        return ''+Highcharts.numberFormat(this.total, 0, ',')
                    }
                }
            }
        }
    );
    // Clone the options and apply default colors to the series if needed.
    coloredOptions = jQuery.extend(true, {}, options);
    $.dualMap(
        coloredOptions.series,
        DEFAULT_STACKED_SERIES_COLORS.slice(0,coloredOptions.series.length),
        function(aSeries, color) {
            if (!aSeries['color']) {
                aSeries['color'] = color;
            }
    });
    combinedOptions = $.extend(true, {}, barOptions, coloredOptions);
    chart = new Highcharts.Chart(
        combinedOptions
    );
}

/**
 * Creates a chart that displays data of one or more scenarios where each series takes one data point from
 * each scenario, and the scenario data_points are related. A simple example is new dwelling units, employment, and population.
 * Each scenario has a total population, dwelling units, and employment. Thus there are three series
 * and the number of points in each series equals the number of scenarios.
 * @param reportData - reportData.result_data contains arrays of scenario data, where each array contains the n data points for the n series desired
 * @param seriesNames - The names of the n series
 * @options - Mimics the highcharts options dictionary. Use this for title, subtitle, etc.
 */

function createRelatedScenarioDataBarChart(reportData, seriesNames, options, divId){
    // data is a 2D array. Each outer array should be a scenario.
    // Each inner array should represent one data point for each series given in seriesNames
    scenariosData = reportData.result_data
    // Calculate the sum of the series data points of each scenario to calculate percentages
    scenariosTotals = $.map(scenariosData, function(scenarioData) {
        return scenarioData.reduce(function(prev, cur, index, array) {
            return prev+cur
        });
    });
    newOptions = {
        subtitle: {text:(scenariosData.length > 1 ? 'per Scenario' : 'for Single Scenario')},
        chart: {renderTo:divId},
        xAxis: {
            // The scenario names
            categories: reportData.report_scenarios,
            labels: {enabled:true}
        },
        yAxis: {
            startOnTick: true,
            title: {
                text: options['yLabel'],
                align: 'high'
            }
        },
        tooltip: {
            formatter: function() {
                return $.format("{0}: {1} Total. {2}% of {3}",
                    this.series.name,
                    Highcharts.numberFormat(this.point.options.value, 0, ','),
                    Highcharts.numberFormat(this.point.options.percent, 2, '.', ','),
                    options.isPercent ? 'other values' : options['yLabel']
                )
            }
        },
        series:
        // Each series has one data point per scenario
        // Thus for a single scenario we only have on point per series
            $.map(seriesNames, function(seriesName, index) {
                return $.extend({
                    name:seriesName,
                    data:
                        $.map(scenariosData, function(scenarioData, scenarioIndex) {
                            // Create a hash for each datapoint in order to store the total
                            return {
                                y:options.usePercent ? 100*scenarioData[index]/scenariosTotals[scenarioIndex] : scenarioData[index],
                                // This is an added non-highcharts key
                                // It gives sum of the scenario datapoints where relevant
                                value: scenarioData[index],
                                percent: 100*scenarioData[index]/scenariosTotals[scenarioIndex],
                                total:scenariosTotals[scenarioIndex]
                            };
                        }),
                    type:'column'
                },
                options && options.seriesOptions || {})
            })
    };
    combinedOptions = $.extend(true, {}, newOptions, options);
    return createBarChart(combinedOptions);
}

/**
 *  Given an alphanumeric report id currently defined in class SqlReport.py,
 *  this function queries with ajax to fetch the report data.
 * @param reportId: a SQL report defined in views_reports.py
 * @param scenarios: an array of one or more scenario objects
 * @param createChart: a function to create the chart based on the object returned by dataToJson
 */
function requestChartData(reportId, scenarios, createChart) {
    $.ajax({
        url : scenarios.length > 1 ?
            // If we have multiple scenarios grab the study_area id
            requestChartDataStudyArea(reportId, scenarios[0].fields.study_area) :
            // Otherwise grab the scenario id
            requestChartDataScenario(reportId, scenarios[0].pk),
        type : "GET",
        cache: false,
        error : function() {
            jQuery.jGrowl("Error encountered while fetching report: " + reportId, { theme: 'calthorpe_bad', sticky: false });
        },
        success : function(data) {
            createChart(data);
        }
    });
}

function requestChartDataScenario(reportId, scenarioId) {
    return $.format("/footprint/scenario/{0}/report_data/{1}?format=json", scenarioId, reportId)
}
function requestChartDataStudyArea(reportId, studyAreaId) {
    return $.format("/footprint/study_area/{0}/report_data/{1}?format=json", studyAreaId, reportId)
}

////PIE CHART (in development)
//function createPieChart(reportData, seriesNames, options, divId){
//    scenariosData = reportData.result_data
//    scenariosTotals = $.map(scenariosData, function(scenarioData) {
//        return scenarioData.reduce(function(prev, cur, index, array) {
//            return prev+cur
//        });
//    });
//    new Highcharts.Chart({
//        plotOptions:{
//            pie:{
//                allowPointSelect:true,
//                cursor:'pointer',
//                dataLabels:{
//                    enabled:true,
//                    showInLegend: true,
//                    color:'#000000',
//                    connectorColor:'#000000',
//                    formatter: function() {
//                        return '<b>'+ this.Name + '</b><br>' + Highcharts.numberFormat(this.y, 0, ',') + ' ('+ this.percentage +' %)';
//                    }
//                }
//            }
//        },
//        legend: {
//            layout: 'vertical',
//            align: 'right',
//            verticalAlign: 'top',
//            x: 0,
//            y: 45,
//            floating: true,
//            borderWidth: 1,
//            backgroundColor: '#FFFFFF',
//            shadow: true
//        },
////        exporting:{
////            buttons:{
////                exportButton:{
////                    align:'left',
////                    x:80,
////                    y:54
////                },
////                printButton:{
////                    align:'left',
////                    x:110,
////                    y:54
////                }
////            }
////        },
//        credits:{
//            enabled:false
//        },
//        chart: {renderTo:divId},
//        series:
//        // Each series has one data point per scenario
//        // Thus for a single scenario we only have on point per series
//            $.map(seriesNames, function(seriesName, index) {
//                return {
//                    type:'pie',
//                    name:seriesName,
//                    data:
//                        $.map(scenariosData, function(scenarioData, scenarioIndex) {
//                            // Create a hash for each datapoint in order to store the total
//                            return {
//                                y:scenarioData[index],
//                                // This is an added non-highcharts key
//                                // It gives sum of the scenario datapoints where relevant
//                                total:scenariosTotals[scenarioIndex]
//                            };
//                        })
//
//                }
//            })
//    });
//    chart.renderTo = divId;
//    $.dualMap(
//        combinedOptions.series,
//        DEFAULT_SERIES_COLORS.slice(0,combinedOptions.series.length),
//        function(aSeries, color) {
//            if (!aSeries['color']) {
//                aSeries['color'] = color;
//            }
//        });
//}
/**
 *  A mock version of fetchChartData for charts that are hard-coded or for testing
 * @param dataToJson
 * @param createChart
 */
function fetchFakeChartData(dataToJson, createChart) {
    createChart(dataToJson(null))
}

