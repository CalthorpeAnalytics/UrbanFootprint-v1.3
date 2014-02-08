(function() {

    var donutChart, dataset, fixture;

    module( "Test basic set up of a single chart", {

        setup: function(){


            dataset = [
                { "category" :"Category_A", "percentage" : 0.90},
                { "category" :"Category_B", "percentage": 0.10}
            ];

            donutChart = d3.edge.donutChart();
            donutChart.width(200);

            fixture = d3.select('body')
                .append('div')
                .attr("width", 200)
                .attr("height", 200)
                .attr('class','test-container')
                .attr('id', 'chart1');
            fixture.datum(dataset)
                .call(donutChart);

        }, teardown: function() {
            fixture.remove();
        }
    });

    test( "when given a single dataset, it should bind the dataset to a single svg as it's __data__ property", function() {

        var svgs = $('.test-container svg');

        equal(svgs.length, 1, "Test container contains a single svg");
        equal(svgs[0].__data__.length, dataset.length, "Length of __data__ bound to svg equal to length of dataset");

    });
    test( "__data__ bound to svg should be an array of objects, each with a valid 'category' and 'percentage' property",
        function() {

        var svg = $('.test-container svg')[0];

        strictEqual(svg.__data__[0]["category"], "Category_A", "__data__[0] has property 'category' with correct value");
        strictEqual(svg.__data__[0]["percentage"],0.90, "__data__[0] has property 'percentage' with correct value");

        for(var i = 0; i < dataset.length; i++) {

            strictEqual(typeof(svg.__data__[i]["category"]), "string", "typeof 'category' value for __data__[" + i + "] is 'string'");
            strictEqual(typeof(svg.__data__[i]["percentage"]), "number", "typeof 'percentage' value for __data__[" + i + "] is 'number'");

        }


    });
    test("pie(_data) should extract the percentages from each data object in the array __data__ bound to svg" +
        "and return a new array of objects, each with correct properties for creating arcs", function() {

        var arcs = $('svg g.arc');

        var startAngle = arcs[0].__data__.startAngle,
            endAngle = arcs[0].__data__.endAngle,
            category = arcs[0].__data__.data.category,
            percentage = arcs[0].__data__.data.percentage;

        equal(typeof(startAngle),"number","arcs[0].__data__ has a 'startAngle' property, type is 'number'")
        equal(typeof(category),"string","arcs[0].__data__.data has a 'category' property, type is 'string'")
        equal(typeof(percentage),"number","arcs[0].__data__ has a 'percentage' property, type is 'number'")
        ok(endAngle >= startAngle, "End angle of arc is greater than start angle")
        equal(arcs.length, dataset.length, "the number of <g> elements with a class 'arc' is equal to the length of the dataset");

    });
    test("it should update chart with new data when datum(newData).call(originalChart) is invoked on the fixture", function() {

        var svgs = $('.test-container svg');
        var svg = svgs[0];

        strictEqual(svg.__data__[0]["category"], "Category_A", "__data__[0] has property 'category' with correct value");
        strictEqual(svg.__data__[0]["percentage"], 0.90, "__data__[0] has property 'percentage' with correct value");


        var dataset2 = [
            { "category" :"Category_C", "percentage" : 0.65},
            { "category" :"Category_D", "percentage": 0.30},
            { "category" :"Category_E", "percentage" : 0.05}
        ];

        fixture.datum(dataset2)
            .call(donutChart);

        var svgs = $('.test-container svg');
        strictEqual(svgs.length, 1, "There is one svg after update");

        var svg = svgs[0],
            chartAndLegend = $('#chartAndLegend'),
            arcs = $('.arc'),
            legend = $('.legend'),
            legendItems = $('.legendItems'),
            rectsInALegendItem = $('.legendItems:first rect'),
            textInALegendItem = $('.legendItems:first text');


        equal(chartAndLegend.length, 1, "One group for chart and legend");
        equal(arcs.length, dataset2.length, "Same number of arcs as there are items in dataset");
        equal(legend.length, 1, "One group for legend");
        equal(legendItems.length, dataset2.length, "Same number of legend items as items in dataset");
        equal(rectsInALegendItem.length, 1, "One rect per legendItem");
        equal(textInALegendItem.length, 1, "One text per legendItem");


        strictEqual(svg.__data__[0]["category"], "Category_C", "__data__[0] has property 'category' with correct value");
        strictEqual(svg.__data__[0]["percentage"], 0.65, "__data__[0] has property 'percentage' with correct value");

    });

    test("after updating data pie(_data) should extract the percentages from each data object in the array __data__ bound to svg" +
        "and return a new array of objects, each with correct properties for creating arcs", function() {

        var arcs = $('svg g.arc');

        var startAngle = arcs[0].__data__.startAngle,
            endAngle = arcs[0].__data__.endAngle,
            category = arcs[0].__data__.data.category,
            percentage = arcs[0].__data__.data.percentage;

        equal(typeof(startAngle),"number","arcs[0].__data__ has a 'startAngle' property, type is 'number'")
        equal(typeof(category),"string","arcs[0].__data__.data has a 'category' property, type is 'string'")
        equal(typeof(percentage),"number","arcs[0].__data__ has a 'percentage' property, type is 'number'")
        ok(endAngle >= startAngle, "End angle of arc is greater than start angle")
        equal(arcs.length, dataset.length, "the number of <g> elements with a class 'arc' is equal to the length of the dataset");

    });
//        var largeDataSet = [ dataset, dataset2];
//        fixture.selectAll('div.container')
//            .data(largeDataSet)
//            .enter().append('div')
//            .classed('container', true)
//            .datum(function(d, i) {return d;})
//            .call(donutChart);
//
//        var charts = fixture.selectAll('.chart');
//        assert.equal(charts[0].length, largeDataSet.length);
//        assert.equal(charts[0][0].__data__, largeDataSet[0]);
//        assert.equal(charts[0][1].__data__, largeDataSet[1]);
//
//    });
//    test( "should create an svg element bound with the data" , function() {
//
//        fixture.datum(dataset).call(donutChart);
//        var charts = $('.chart');
//        assert.equal(charts.length, 1);
//
//    });
//
})();
//(function() {
//
//    var donutChart, donutChart2, dataset, dataset2, fixture;
//
//    module( "Test updating a chart with new data", {
//
//        setup: function(){
//
//            dataset = [
//                { "category" :"Category_A", "percentage" : 0.10},
//                { "category" :"Category_B", "percentage": 0.90}
//            ];
//            dataset2 = [
//                { "category" :"Category_C", "percentage" : 0.45},
//                { "category" :"Category_D", "percentage": 0.30},
//                { "category" :"Category_E", "percentage": 0.25}
//            ];
//
//            donutChart = d3.edge.donutChart();
//            donutChart2 = d3.edge.donutChart();
//
//            fixture = d3.select('body')
//                .append('div')
//                .classed('test-container', true);
//
//
//            fixture.append('div')
//                .datum(dataset)
//                .property('id', 'chart1')
//                .call(donutChart);
//
//
//            fixture.append('div')
//                .datum(dataset2)
//                .property('id', 'chart2')
//                .call(donutChart2);
//
//        }, teardown: function() {
//            fixture.remove();
//        }
//    });
//
//    test( "it should render two distinct divs, each containing one svg element", function() {
//
//        assert.equal($('#chart1 > svg').length, 1, "One svg element created inside first div");
//
//    });
//
//})();
(function() {

    var donutChart, donutChart2, dataset, dataset2, fixture, catAPct, catBPct, catCPct, catDPct;

    module( "Test setting up two distinct charts", {

        setup: function(){

            catAPct = .90, catBPct = .10,
                catCPct = .80, catDPct = .20;


            dataset = [
                { "category" :"Category_A", "percentage" : catAPct},
                { "category" :"Category_B", "percentage": catBPct}
            ];
            dataset2 = [
                { "category" :"Category_C", "percentage" : catCPct},
                { "category" :"Category_D", "percentage": catDPct}
            ];

            donutChart = d3.edge.donutChart();
            donutChart2 = d3.edge.donutChart();

            fixture = d3.select('body')
                .append('div')
                .classed('test-container', true);


            fixture.append('div')
                .datum(dataset)
                .property('id', 'chart1')
                .call(donutChart);


            fixture.append('div')
                .datum(dataset2)
                .property('id', 'chart2')
                .call(donutChart2);

        }, teardown: function() {
            fixture.remove();
        }
    });

    test( "it should render two distinct divs, each containing one svg element", function() {

        assert.equal($('#chart1 > svg').length, 1, "One svg element created inside first div");
        assert.equal($('#chart2 > svg').length, 1, "One svg element created inside second div");

    });
    test( "it should display correct labels and percentages for categories within each chart", function() {

        assert.equal($('#chart1 > svg')[0].__data__[0].category, "Category_A", "First chart displays correct category for first dataObject");
        assert.equal($('#chart1 > svg')[0].__data__[0].percentage, catAPct, "First chart displays correct percentage for first dataObject");

        assert.equal($('#chart2 > svg')[0].__data__[0].category, "Category_C", "Second chart displays correct cateogry for first dataObject");
        assert.equal($('#chart2 > svg')[0].__data__[0].percentage, catCPct, "Second chart displays correct percentage for first dataObject");

    });

})();

(function() {

    var dataManager;

    module( "Test the creation of the data objects comprising the data array that is used by the model", {

        setup: function(){

            dataManager = d3.edge.dataManager();

        },

    });

    test( "it should create an object with a category as string and a percent as a float", function() {

        var dataObject1 = dataManager.createDataObject("Mixed-Use", 0.45);
        assert.equal(dataObject1.category, "Mixed-Use", "When given a string, data object has a category field with correct string value");
        assert.equal(dataObject1.percentage, 0.45, "When given a percent float, data object has a percentage field with correct float value");

        var dataObjectWithStringPct = dataManager.createDataObject("Mixed-Use", "0.45");
        assert.strictEqual(dataObjectWithStringPct.percentage, 0.45, "When given a percent as a string, data object has a percentage field with correct float value");

    });


})();
(function() {

    var donutChart, fixture, newWidth, newInnerRadiusPct, newOuterRadiusPct;

    module( "Test getter and setter functionality", {

        setup: function(){

            newWidth = 1000;
            newInnerRadiusPct = 0.1;
            newOuterRadiusPct = 0.3;

            donutChart = d3.edge.donutChart();
            fixture = d3.select('body')
                .append('div')
                .classed('test-container', true);

        }, teardown: function() {
            fixture.remove();
        }
    });

    test( "it should provide getters and setters for chart width", function() {

        var defaultWidth = donutChart.width();

        donutChart.width(newWidth);

        var resetWidth = donutChart.width();

        assert.notEqual(defaultWidth, resetWidth, "Width is not equal to default after it is reset");
        assert.equal(newWidth, resetWidth, "Width is equal to the newly defined width after it is reset");

    });
    test( "it should provide getters and setters for chart title", function() {

        var defaultTitle = donutChart.title();

        donutChart.title("New title");

        var resetTitle = donutChart.title();

        assert.notEqual(defaultTitle, resetTitle, "Title is not equal to default after it is reset");
        assert.equal(resetTitle, "New title", "Title is equal to newly defined title after it is reset");

    });
    test( "it should provide getters and setters for inner and outer radius and width of chart", function() {

        var defaultInnerRadiusPct = donutChart.innerRadius();
        var defaultOuterRadiusPct = donutChart.outerRadius();

        donutChart.innerRadius(newInnerRadiusPct);
        donutChart.outerRadius(newOuterRadiusPct);

        var resetInnerRadius = donutChart.innerRadius();
        var resetOuterRadius = donutChart.outerRadius();

        assert.notEqual(defaultInnerRadiusPct, resetInnerRadius, "Inner radius not equal to default after it is reset");
        assert.notEqual(defaultOuterRadiusPct, resetOuterRadius, "Inner radius not equal to default after it is reset");

        assert.equal(newInnerRadiusPct, resetInnerRadius, "Inner radius equal to new default after it is reset");
        assert.equal(newOuterRadiusPct, resetOuterRadius, "Inner radius equal to new default after it is reset");

    });

    test( "it should allow chaining of setter methods", function() {

        var defaultInnerRadiusPct = donutChart.innerRadius();
        var defaultOuterRadiusPct = donutChart.outerRadius();
        var defaultWidth = donutChart.width();

        donutChart.width(newWidth)
            .outerRadius(newOuterRadiusPct)
            .innerRadius(newInnerRadiusPct);

        var resetWidth = donutChart.width();
        var resetOuterRadius = donutChart.outerRadius();
        var resetInnerRadius = donutChart.innerRadius();

        assert.equal(resetWidth, newWidth, "Width is equal to new value after it is reset");
        assert.equal(resetOuterRadius, newOuterRadiusPct, "Outer radius is equal to new value after it is reset");
        assert.equal(resetInnerRadius, newInnerRadiusPct, "Inner radius is equal to new value after it is reset");

        assert.notEqual(resetInnerRadius, defaultInnerRadiusPct);
        assert.notEqual(resetOuterRadius, defaultOuterRadiusPct);
        assert.notEqual(resetWidth, defaultWidth);

    });

})();
