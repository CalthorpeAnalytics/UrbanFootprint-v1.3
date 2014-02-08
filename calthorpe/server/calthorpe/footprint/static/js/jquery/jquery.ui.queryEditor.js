/*! * jQuery UI QueryEditor *
 * Andy Likuski
 *
 * Depends: incomplete
 */
(function( $, undefined ) {

var uiQueryEditorClasses =
		'ui-queryEditor ' +
		'ui-widget ' +
		'ui-widget-content ' +
		'ui-corner-all ';
var SELECTION_RADIO_BUTTONS = ['Append', 'Replace'];

$.widget("ui.queryEditor", {
	options: {
        /* The data consists of a list of table view definitions that are registered with the geoserver. The primary table of the sql statement should be indicated by table_name and must be a layer in the geoserver
		data: {
		    tableViews: [{name:'all odd elements', table_name:'a geoserver-mapped table', query:'select ... from ... where ...'}, ...]
        },
        */
        data: {
            tableViews: [
                {name:'A is for apple', table_name:'a_table', query:'select a from apple'},
                {name:'B is for bagel', table_name:'b_table', query:'select b from bagel'},
                {name:'C is for cake', table_name:'c_table', query:'select c from cake'}
            ]},
		queryEditorClass: '',
        buttons: null, // pass in button ids. These will become <button class='ui-button-[id]' id="id"></button> in the buttons pane
        buttonsInit: null // pass in a function to init the buttons by #id or .ui-button-[id]. A single argument buttonsPane is a jQuery selector matching the buttonsPane of this widget
	},
    $undoredo: null,

    /**
     * Adjusts all data to the given object
     * @param data: {queryField:[], savedQuerySelect:[]}, where valueFields is optional
     * @param restor: optional true if this an undo/redo operation
     */
    setData: function(data, restore) {
        // Update the fields to match the data
        this._update(data, restore);
    },
    /***
     *  Clear the changes made by the user since loading or the last update
     */
    clearChanges: function() {
    },
    /**
     * Change is called after any change to the data fields or number of fields. It adds the data to the undo buffer and triggers the 'change' event.
     * @param restore: true if this change is the result of an undo/redo operation
     */
    _change: function(restore) {
       if (!restore) {
         this.$undoredo.undoredo('add', this.currentQuery());
       }
       this._trigger("change", null, {});
    },
    currentQuery: function() {
        return this._currentValuesOfControls('queryField');
    },
    currentSavedQueries: function() {
        return this._currentValuesOfControls('savedQuerySelect')
    },
    updateQuery: function(value) {
        this._update({'queryField':value});
    },
    updateSavedQueries: function(savedQueries) {
        this._update({'savedQuerySelect':savedQueries});
    },

	_create: function() {
        var self = this,
            options = self.options,
            data = options.data;

        // The top level div of the plugin, which is appended to the passed in element
        (self.uiQueryEditor = $('<div></div>'))
                .addClass(uiQueryEditorClasses + options.queryEditorClass)
                .attr({
                    role: 'queryEditor'
                })
                .appendTo(self.element);

        // Create the controls based on the initially supplied data
        self._createControls(data);
	},

	_init: function() {
	},

	widget: function() {
		return this.uiQueryEditor;
	},

    _currentValuesOfControls: function(fieldName) {
        return this._currentValues(this._uiPanes[fieldName].set)
    },
    _currentValues: function(set) {
        var selection = d3.selectAll(set).selectAll('.ui-queryEditor-Input');
        return selection.empty() ? [] : selection[0].map(function(d) {return d.value;})
    },
    _visibleFields: function() {
        return ['queryField', 'savedQuerySelect']
    },
	_createControls: function(data) {
		var self = this,
            // The panes of the control are a set of editable color inputs.
            // optional corresponding data values are the ranges of data represented by each color.
            // Thus there is always one fewer color than value
            panes = [].concat(this._visibleFields()).concat(['buttons']),
            inputPanes = this._visibleFields(),
            fieldPaneToControlCreator = {
                queryField: {
                    data:[$.lastItem(data.tableViews)],
                    mapIncomingDatum: function(d) {
                        return d;
                    },
                    createContainer: function($parent) {
                        return $('<div></div>').appendTo($parent);
                    },
                    itemType: 'textarea',
                    d3: function(selection) {
                    },
                    createControl: function(element, d, i) {
                        return self._queryField(element, d, i)
                    },
                    updateValue: function(element, d, i) {
                        $(element).value = d.query;
                    },
                    finalizeControl: function($set) {
                    }
                },
                savedQuerySelect: {
                    data:data.tableViews,
                    mapIncomingDatum: function(d) {
                        return d;
                    },
                    createContainer: function($parent) {
                        var $select = $('<select multiple="multiple"></select>');
                        $select.appendTo($parent);
                        return $select;
                    },
                    itemType: 'option',
                    d3: function(selection) {
                    },
                    createControl: function(element, d, i) {
                        return self._savedQuery(element, d, i)
                    },
                    updateValue: function(element, d, i) {
                        $(element).text(d.name); //$.format("{0} - {1}", d.name, d.query));
                    },
                    d3Sort: 'ascending',
                    finalizeControl: function($set) {
                        $set.selectBox('destroy').selectBox({
                            value:4
                        }).change(function() {
                            self.updateQuery($(this).value)
                        })
                    }
                }
            },
            // Create a dive pane and sub div for the rows of color fields, value fields, and for the slider
            $uiPanes = (self._uiPanes = $.mapToDictionary(
                panes,
                function(paneName) {
                    var paneClassName = $.format('ui-queryEditor-{0}Pane ', paneName),
                        $pane = $('<div></div>')
                            .addClass(
                                paneClassName +
                                    'ui-queryEditor-pane ' +
                                    'ui-widget-content ' +
                                    'ui-helper-clearfix'
                            )
                            .appendTo(self.uiQueryEditor),
                        $set = ($.has(self._visibleFields, paneName) ?
                                fieldPaneToControlCreator[paneName].createContainer($pane) :
                                $('<div></div>').appendTo($pane))
                            .addClass( $.format("ui-queryEditor-{0}Set", paneName))
                            .addClass("ui-queryEditor-set", true);
                        elements = {pane:$pane, set:$set};
                    // Remove the panel if it already exists
                    self.uiQueryEditor.find(paneClassName).remove();
                    return [paneName,elements];
                }
            )),
            $buttons = $uiPanes.buttons.pane;
        // Create each configured button
        $.each(self.options.buttons || [], self._buttonCreator($buttons));
        // Call the initializers of standard buttons
        self._createStandardButtons($buttons);
        // Call custom initializers
        if (self.options.buttonsInit)
            self.options.buttonsInit(self, $buttons);

        self.$undoredo = self.uiQueryEditor.undoredo({
            undo: function(event, ui) {
                self.setData(ui.data, true);
            },
            redo: function(event, ui) {
                self.setData(ui.data, true);
            }
        });

        // Craft an update method from the create controls
        // forceValues is in the form {} where one or both data sets may be present
        self._update = function(forceValues, restore) {

            var isRestore =  restore || false;

            // Map the two edit field panes to the corresponding sequence
            $.each(inputPanes, function(i,paneName) {
                var paneConfig = fieldPaneToControlCreator[paneName],
                    set = $uiPanes[paneName].set,
                    itemWidth = set.ancestorNonZeroValue('width'),
                    values = forceValues && forceValues[paneName] ?
                    // forced data or
                    forceValues[paneName] :
                    $.map($.arrayOrIfEmpty(
                        // inputs data or
                        self._currentValues(set),
                        // default data
                        paneConfig.data),
                        function(d) {
                            return paneConfig.mapIncomingDatum(d);
                });

                // Scale the font based on the number of values being shown
                function sizeControls(inputs) {
                    inputs.style("width", $.format("{0}px", itemWidth))
                }

                // calculate a linear range, this works for colors and ints
                // Use d3 to keep number of text fields in sync with the currentIntervalCount
                var controls = d3.selectAll(set)
                    .selectAll('.ui-queryEditor-Item')
                    // Bind the data using the index
                    .data(values, function(d, i) {return i});
                controls
                    .select('input')
                    .each(function(d,i) {
                        paneConfig.updateValue(this, d,i);
                    })
                    .call(sizeControls);

                // Give each new interval a control
                var elements = controls.enter()
                    .append(paneConfig.itemType)
                    .classed('ui-queryEditor-Item', true)
                    .classed('ui-queryEditor-Input', true);
                elements
                    .attr('id', function(d,i) {
                        return $.format('uiQueryEditor{0}Input{1}', paneName, i);
                    })
                    .classed($.format('ui-queryEditor-{0}Input', paneName), true)
                    .each(function(d,i) {
                        paneConfig.createControl(this, d,i);
                        paneConfig.updateValue(this, d,i);
                    })
                    .call(function(selection) {
                        paneConfig.d3(selection)
                    })
                    .call(sizeControls);

                controls.exit().remove();
                paneConfig.finalizeControl($(set))
            });
            // Call change to update the undo buffer and send the change event
            self._change(isRestore);
        };
        // Call update to initialize
        self._update()
	},
    _buttonCreator : function($buttons) {
        return function createButtons(i, buttonNameOrButtonArray) {
            if ($.isArray(buttonNameOrButtonArray)) {
                var buttonArray = buttonNameOrButtonArray;
                $.each(buttonArray, createButtons);
                $('<br/>').appendTo($buttons)
            }
            else {
                var buttonName = buttonNameOrButtonArray;
                var $button;
                if (buttonName == 'selectionType') {
                    var $selectionTypeButtons = $('<div></div>').appendTo($buttons);
                    $.each(SELECTION_RADIO_BUTTONS, function(i, selectionButton) {
                        $button = $('<input type="radio">').appendTo($selectionTypeButtons);
                        $button.attr('name', 'radio');
                        // Classify the button as a ui-button
                        $button.attr('id', selectionButton)
                            .addClass($.format('ui-button-{0}', selectionButton));
                        var $label = $('<label></label>');
                        $label.text(selectionButton);
                        $label.attr('for', selectionButton);
                        $label.appendTo($selectionTypeButtons);
                    });
                    $selectionTypeButtons.buttonset();
                }
                else {
                $button = $('<button></button>');
                // Classify the button as a ui-button
                $button.attr('id', buttonName)
                    .addClass($.format('ui-button-{0}', buttonName))
                    .appendTo($buttons);
                }

                // Classify undo/redo buttons as ui-undoredo buttons as well
                if ($.inArray(buttonName, ['undo','redo','clear']) != -1) {
                    $button.addClass($.format('ui-undoredo-{0}', buttonName))
                }
            }
        };
    },
    /**
     *  Defines functionality for the standard buttons
     * @param buttonsPane
     */
    _createStandardButtons: function(buttonsPane) {
        var self = this;
        buttonsPane.find( ".ui-button-unselectAll").button({
            label: 'Unselect All',
            icons: {
                primary: "ui-icon-radio-on"
            }
        })
            .click(function() {
                // Copy the updated data to a cloned data structure
                var clonedData = jQuery.extend(true, {}, data);
                // Save the data to the server. Only one property will change
                saveQueryData(data, function() {
                    $.each(layerManager.gridLayers, function(i, gridLayer) {
                        if (gridLayer.name.indexOf(property.name) != -1) {
                            gridLayer.redraw(true);
                        }
                    });
                });
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
			uiQueryEditor = self.uiQueryEditor;

		switch (key) {
			case "data":
				self._createControls(value);
				break;
			case "queryEditorClass":
				uiQueryEditor
					.removeClass(self.options.queryEditorClass)
					.addClass(uiQueryEditorClasses + value);
				break;
		}

		$.Widget.prototype._setOption.apply(self, arguments);
	},

    _queryField:function(element, d, i) {
        element.value = d.query;
    },
    _savedQuery:function(element, d, i) {
        element.value = d.name;
    }

});

}(jQuery));

