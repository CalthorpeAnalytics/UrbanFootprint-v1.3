/*! * jQuery UI StyleEditor
 *
 * Andy Likuski
 *
 * Depends:
 *	jquery.ui.core.js
 *	jquery.ui.widget.js
 *	jquery.ui.mouse.js
 *	jquery.ui.colorpicker.js
 */

(function( $, undefined ) {

var uiStyleEditorClasses =
		'ui-styleEditor ' +
		'ui-widget ' +
		'ui-widget-content ' +
		'ui-corner-all ';

$.widget("ui.styleEditor", {
	options: {
        /* Sample data
		data: {
            name:'Feature Name',
            intervalCount:5,
            // The colorSequence can be any length. Intermediate values are calculated by d3 to match the intervalCount
            colors: ['#FF0000','#00FF00'],
            // The values defining the intervals. There should be one more break than intervalCount
            breaks: [0, 0.2, 0.4, 0.6, 0.8, 1]
        },
        */
        minNumberOfIntervals:4, // The maximum number of data intervals (= number of colors and number breaks - 1)
        maxNumberOfIntervals:10, // The maximum number of data intervals (= number of colors and number breaks - 1)
        showValues:true, // Set false to only see the colors, not the value range inputs
		styleEditorClass: '',
		zIndex: 10000,
        buttons: null, // pass in button ids. These will become <button class='ui-button-[id]' id="id"></button> in the buttons pane
        buttonsInit: null // pass in a function to init the buttons by #id or .ui-button-[id]. A single argument buttonsPane is a jQuery selector matching the buttonsPane of this widget
	},
    // The slider is bi-directionally bound with this value
    currentIntervalCount: null,
    $undoredo: null,

    /**
     * Adjusts all data to the given count. If count is null all data is adjusted to the original count
     * @param [count]
     */
    setIntervalCount: function(count) {
        this.currentIntervalCount = count || this.options.data.intervalCount;
        // Update the slider value if it doesn't match
        this._updateSlider();
        // Update the fields to match the count
        this._update();
    },
    /**
     * Adjusts all data to the given object
     * @param data: {colorFields:[], valueFields:[]}, where valueFields is optional
     * @param [restore]: optional true if this an undo/redo operation
     */
    setData: function(data, restore) {
        this.currentIntervalCount = data.colorFields.length;
        // Update the slider value if it doesn't match
        this._updateSlider();
        // Update the fields to match the data
        this._update(data, restore);
    },
    /***
     *  Clear the changes made by the user since loading or the last update
     */
    clearChanges: function() {
        // Clear the input fields in order to recalculate them
        $.each(this._visibleFields(), function(i, fieldName) {
            this._removeControlsOfPane(fieldName);
        });
        // Reset the interval count to the original value and calculate the data accordingly
        this.setIntervalCount();
    },
    /**
     * Specifies the field input controls to show
     * @return {Array}
     * @private
     */
    _visibleFields:function() {
        return this.options.showValues ?
            ['colorFields', 'valueFields'] :
            ['colorFields'];
    },
    /**
     * Change is called after any change to the data fields or number of fields. It adds the data to the undo buffer and triggers the 'change' event.
     * @param restore: true if this change is the result of an undo/redo operation
     */
    _change: function(restore) {
       if (!restore) {
         this.$undoredo.undoredo('add', this.currentData());
       }
       this._trigger("change", null, {});
    },
    currentValues: function() {
        return this._currentValuesOfFields('valueFields');
    },
    currentColors: function() {
        return this._currentValuesOfFields('colorFields')
    },
    currentData: function() {
        var self = this;
        return $.mapToDictionary(this._visibleFields(), function(field) {
            return [field,self._currentValuesOfFields(field)];
        });
    },
    updateValues: function(values) {
        this._update({valueFields:values});
    },
    updateColors: function(colors) {
        this._update({colorFields:colors});
    },
    /**
     * Takes the first and last value and quantize the intermediate ones between them
     * @param values
     */
    quantizeValues: function(values) {
        this.updateValues($.extremes(this.currentValues()));
    },
    /**
     *
     * Takes the first and last colors and quantize the intermediate ones between them
     * @param colors
     */
    quantizeColors: function(colors) {
        this.updateColors($.extremes(this.currentColors()));
    },

	_create: function() {
        var self = this,
            options = self.options,
            data = options.data;

        // The top level div of the plugin, which is appended to the passed in element
        (self.uiStyleEditor = $('<div></div>'))
                .addClass(uiStyleEditorClasses + options.styleEditorClass)
                .css({
                    'z-index': options.zIndex
                })
                .attr({
                    role: 'styleEditor'
                })
                .appendTo(self.element);

        // Create the controls based on the initially supplied data
        self._createControls(data);
	},

	_init: function() {
	},

	widget: function() {
		return this.uiStyleEditor;
	},

    _currentValuesOfFields: function(fieldName) {
        return this._currentValues(this._uiPanes[fieldName].set)
    },
    _currentValues: function(set) {
        var selection = d3.selectAll(set).selectAll('.ui-styleEditor-Input');
        return selection.empty() ? [] : selection[0].map(function(d) {return d.value;})
    },
    _removeControlsOfPane: function(paneName) {
        set = this._uiPanes[paneName].set;
        var selection = d3.selectAll(set).selectAll('.ui-styleEditor-Item').remove();
    },
    _updateSlider: function() {
        if (this._slider.slider("option", "value") != this.currentIntervalCount) {
            this._slider.slider( "option", "value", this.currentIntervalCount);
        }
    },

	_createControls: function(data) {
		var self = this,
            // The panes of the control are a set of editable color inputs.
            // optional corresponding data values are the ranges of data represented by each color.
            // Thus there is always one fewer color than value
            panes = [].concat(this._visibleFields()).concat(['slider', 'buttons']),
            inputPanes = this._visibleFields(),
            // Create a dive pane and sub div for the rows of color fields, value fields, and for the slider
            $uiPanes = (self._uiPanes = $.mapToDictionary(
                panes,
                function(paneName) {
                    var paneClassName = $.format('ui-styleEditor-{0}Pane ', paneName),
                        $pane = $('<div></div>')
                            .addClass(
                                paneClassName +
                                    'ui-styleEditor-pane ' +
                                    'ui-widget-content ' +
                                    'ui-helper-clearfix'
                            )
                            .appendTo(self.uiStyleEditor),
                        $set = $( "<div></div>" )
                            .addClass( $.format("ui-styleEditor-{0}Set", paneName) )
                            .addClass("ui-styleEditor-set")
                            .appendTo( $pane );
                        elements = {pane:$pane, set:$set};
                    // Remove the panel if it already exists
                    self.uiStyleEditor.find(paneClassName).remove();
                    return [paneName,elements];
                }
            )),
            fieldPaneToControlCreator = {
                colorFields: {
                    data:data.colors,
                    // Color count matches the slider
                    deltaFromCount: 0,
                    mapIncomingDatum: function(d) {
                        return d;
                    },
                    mapSequencedDatum: function(d) {
                        return d;
                    },
                    d3: function(selection) {
                        selection.attr('type', 'color');
                    },
                    createControl: function(element, d, i) {
                        return self._colorPicker(element, d, i)
                    },
                    updateValue: function(element, d, i) {
                        $(element).colorpicker('setColor', d);
                    },
                    d3Sort: 'descending'
                },
                valueFields: {
                    data:data.breaks,
                    // Value count is one more than the slider, since they represent interval breaks
                    deltaFromCount: 1,
                    mapIncomingDatum: function(d) {
                        return parseInt(d);
                    },
                    mapSequencedDatum: function(d) {
                        return Math.round(d);
                    },
                    d3: function(selection) {
                        selection.attr('type', 'text');
                    },
                    createControl: function(element, d, i) {
                        return self._valuePicker(element, d, i)
                    },
                    updateValue: function(element, d, i) {
                        $(element).attr('value',d);
                    },
                    d3Sort: 'ascending'
                }
            };

        var $slider = (this._slider = $uiPanes.slider.set);
        $slider.slider({min:this.options.minNumberOfIntervals, max:this.options.maxNumberOfIntervals,
            change: function(event, ui) {
                // Silently update the currentIntervalCount to prevent a circular updates
                if (self.currentIntervalCount != ui.value)
                    self.setIntervalCount(ui.value);
            }
        });
        var $buttons = $uiPanes.buttons.pane;
        var buttonCreator = function(i, buttonNameOrButtonArray) {
            if ($.isArray(buttonNameOrButtonArray)) {
                var buttonArray = buttonNameOrButtonArray;
                $.each(buttonArray, buttonCreator);
                $('<br/>').appendTo($buttons)
            }
            else {
                var buttonName = buttonNameOrButtonArray;
                // Classify the button as a ui-button
                var $button = $('<button></button>')
                    .attr('id', buttonName)
                    .addClass($.format('ui-button-{0}', buttonName))
                    .appendTo($buttons);
                // Classify undo/redo/clear buttons as ui-undoredo buttons as well
                if ($.inArray(buttonName, ['undo','redo','clear']) != -1) {
                   $button.addClass($.format('ui-undoredo-{0}', buttonName))
                }
            }
        };
        // Create each configured button
        $.each(self.options.buttons || [], buttonCreator);
        // Call the initializers of standard buttons
        self._createStandardButtons($buttons);
        // Call custom initializers
        if (self.options.buttonsInit)
            self.options.buttonsInit(self, $buttons);

        self.$undoredo = self.uiStyleEditor.undoredo({
            undo: function(event, ui) {
                self.setData(ui.data, true);
            },
            redo: function(event, ui) {
                self.setData(ui.data, true);
            }
        });

        // Craft an update method from the create controls
        // Use force values to change the colors and or values to a given data set. The number actually used depends on the value of the slider, and only the extremes will be reliably used if the slider increment doesn't match the number of values given.
        // forceValues is in the form {colorFields:[], valueFields:[]} where one or both data sets may be present
        self._update = function(forceValues, restore) {

            var isRestore =  restore || false,
                intervalCount = parseInt(self.currentIntervalCount);

            // Map the two edit field panes to the corresponding sequence
            $.each(inputPanes, function(i,paneName) {
                paneConfig = fieldPaneToControlCreator[paneName];
                var set = $uiPanes[paneName].set;
                // Get the number of inputs to show based on the intervalCount
                // This will be on higher for values and identity for colors
                var numberOfData = intervalCount + paneConfig.deltaFromCount;
                // The values we use are in descending priority either the forced values, the current values of the inputs, or the default data
                values = forceValues && forceValues[paneName] ?
                    // forced data or
                    forceValues[paneName] :
                    $.map($.arrayOrIfEmpty(
                        // inputs data or
                        self._currentValues(set),
                        // default data
                        paneConfig.data),
                        function(d) {
                            // Apply parsing to the data
                            return paneConfig.mapIncomingDatum(d);
                });

                // Recalculates values after the user changes the number of values
                // Currently only the extreme values are considered.
                // Any intermediate values are ignored.
                var calculateSequence = d3.scale.linear()
                    .domain([0,numberOfData-1])
                    .range($.extremes(values));

                var fullSequence = $.map(values.length == numberOfData ?
                        // use specified values of the sequence
                        values :
                        // count changed so recalculate values between the extremes
                        $.map( Number.range(numberOfData), calculateSequence),
                    // Map the incoming values, such as rounding based on the set
                    function(value) {
                        return paneConfig.mapSequencedDatum(value);
                    });

                // Scale the font based on the number of values being shown
                var calculateFontSize = d3.scale.linear()
                    .domain([
                    paneConfig.deltaFromCount + self.options.minNumberOfIntervals,
                    paneConfig.deltaFromCount + self.options.maxNumberOfIntervals])
                    .range([1,0.7]);
                var itemWidth = Math.floor(set.ancestorNonZeroValue('width') / numberOfData)-5;
                var fontSize = $.roundFloat(calculateFontSize(numberOfData), 2);
                function sizeControls(inputs) {
                    inputs
                        .style("width", $.format("{0}px", itemWidth))
                        .style('font-size', $.format("{0}em", fontSize));
                }

                // calculate a linear range, this works for colors and ints
                // Use d3 to keep number of text fields in sync with the currentIntervalCount
                var controls = d3.selectAll(set)
                    .selectAll('.ui-styleEditor-Item')
                    // Bind the data using the index, which causes new values to be added to the end
                    // and removed values to be taken from the end
                    .data(fullSequence, function(d, i) {return i});
                controls
                    .select('input')
                    .each(function(d,i) {
                        paneConfig.updateValue(this, d,i);
                    })
                    .call(sizeControls);

                // Give each new interval a control
                var divs = controls.enter()
                    .append('div');
                divs
                    .classed('ui-styleEditor-Item', true)
                    .append('input')
                    .classed('ui-styleEditor-Input', true)
                    .attr('id', function(d,i) {
                        return $.format('uiStyleEditor{0}Input{1}', paneName, i);
                    })
                    .classed($.format('ui-styleEditor-{0}Input', paneName), true)
                    .each(function(d,i) {
                        paneConfig.createControl(this, d,i);
                        paneConfig.updateValue(this, d,i);
                    })
                    .call(function(selection) {
                        paneConfig.d3(selection)
                    })
                    .call(sizeControls);

                controls.exit().remove();
                //controls.sort(d3[paneConfig['d3Sort']]);
            });
            // Call change to update the undo buffer and send the change event
            self._change(isRestore);
        };

        // Set the interval count and thus set the slider and call self._update()
        self.setIntervalCount();
	},
    /**
     *  Defines functionality for the standard buttons
     * @param buttonsPane
     */
    _createStandardButtons: function(buttonsPane) {
        var self = this;
        // Updates the intermediate values to the extremes chosen by the user
        buttonsPane.find( ".ui-button-quantizeColors" ).button({
            label: 'Quantize Colors',
            icons: {
                primary: "ui-icon-arrowrefresh-1-e"
            }
        })
            .click(function() {
                self.quantizeColors();
            });
        // Updates the intermediate values to the extremes chosen by the user
        buttonsPane.find( ".ui-button-quantizeValues" ).button({
            label: 'Quantize Values',
            icons: {
                primary: "ui-icon-arrowrefresh-1-e"
            }
        })
            .click(function() {
                self.quantizeValues();
            });
    },
	_setOptions: function( options ) {
		var self = this;

		$.each( options, function( key, value ) {
			self._setOption( key, value );
		});

	},

	_setOption: function(key, value){
		var self = this,
			uiStyleEditor = self.uiStyleEditor;

		switch (key) {
			case "data":
				self._createControls(value);
				break;
			case "styleEditorClass":
				uiStyleEditor
					.removeClass(self.options.styleEditorClass)
					.addClass(uiStyleEditorClasses + value);
				break;
		}

		$.Widget.prototype._setOption.apply(self, arguments);
	},

    /***
     * Creates a jquery.ui.colorpicker out of the given dom element
     * @param element
     */
    _colorPicker:function(element, d, i) {
        var self = this;
        $(element).colorpicker({
            colorFormat: 'HEX',
            showOn: 'both',
            altOnChange: false,
            showNoneButton: false,
            buttonColorize: true,
            buttonImageOnly: true,
            limit: 'websafe',
            parts: ['header', 'bar', 'hex' ,
                'rgb', 'preview'],
            regional: 'en',
            /* This causes a jquery error
             alpha: true,
             */
            altProperties: 'background-color,color',
            zIndex:10000,
            close: function(event, ui) {
                self._change(false);
            }
        });

        return element;
    },

    _valuePicker:function(element, d, i) {
        var self = this;
        return $('<input type="text"></button>')
            .change(function() {
                self._change(false);
            });
    }

});

}(jQuery));

