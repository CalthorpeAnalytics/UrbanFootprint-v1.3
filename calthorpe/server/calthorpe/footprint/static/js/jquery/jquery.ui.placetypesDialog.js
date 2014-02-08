/*
 * jquery.ui.placetypesDialog
 *
 * Andy Likuski
 *
 * Depends:
 *	jquery.ui.core.js
 *	jquery.ui.widget.js
 *	jquery.ui.draggable.js
 *	jquery.ui.mouse.js
 */
(function( $, undefined ) {

    var uiStyleEditorClasses =
        'ui-styleEditor ' +
            'ui-widget ' +
            'ui-widget-content ' +
            'ui-corner-all ';

    $.widget("ui.placetypesDialog", {
        options: {
            // Required PlacetypesManager which loads and manages the placetypes
            placetypesManager: null,
            // A jquery selector for 0 or more DOM elements to hold the compass rose control, if compass rose behavior is enabled
            compassRoseSelector: null, // $('.compass_rose')
            // A jquery selector for 0 or more DOM elements to function as buttons that open and close the dialog
            placetypesDialogButtonSelector: null, // $(".placetype_dialog_button")
            placetypeTableSelector: $('.placetype_table')
        },

        _create: function() {
            this.uiPlacetypesDialog = this.element;
            // Wire the controls load method to the manager's
            this._createControls();
        },

        _init: function() {
        },

        widget: function() {
            return this.uiPlacetypesDialog;
        },

        /**
         * Combines the currently selected placetype id and cardinal direction (if activated) to create a complete placetype.
         */
        activePlacetype : function(placetype) {
            var self = this;
            if (placetype) {
                this.activePlacetypeId = placetype.ptid;
                var matchingPlacetype = self.placetypes[this.activePlacetypeId];
                self.placetypeTableSelector.jqGrid(
                    "setSelection",
                    this.orderedPlacetypes.indexOf(matchingPlacetype)+1);
            }
            return $.extend({},
                self.placetypes[self.activePlacetypeId],
                {cardinalDirection:self.activeCardinalDirection()});
        },

        /**
         * Returns the cardinal direction of the active placetype if compassRoseEnabled is true
         * @return {*}
         */
        activeCardinalDirection : function() {
            // Search the table for the highlighted row and select it's compass rose button
            $compassRoseTableButton = $('.jqgrow.ui-row-ltr.ui-state-highlight').find('.compass_rose_table_button');
            return ($compassRoseTableButton.length > 0) ?
                $compassRoseTableButton[0].value :
                'C';
        },

        _createControls: function() {
            var self = this;
            self.options.placetypesManager.loadPlacetypes(function() {
                self.uiPlacetypesDialog.dialog({
                    show:"slide",
                    hide:"slide",
                    width : 'auto',
                    autoOpen:false,
                    zIndex: 11000,
                    resize: function(event, ui) {
                        self._positionCompassRose()
                    }
                });
            });
            self.placetypesDialogButtonSelector.button().click(function() {
                var theDialog = $(self.uiPlacetypesDialog);
                if (theDialog.dialog('isOpen')) {
                    theDialog.dialog('close');
                }
                else {
                    theDialog.dialog('open');
                }
            });

            if (self.compassRoseEnabled) {
                self._setupCompassRose()
            }
            self.compassRoseSelector.css('display', 'none');
        },
        /**
         * Creates a control that sets the compass rose direction of the active placetype.
         * @param $compassRose - selector for one or more compass roses
         * @param closeOnClick - if true hides when a compass rose button is selected
         * @private
         */
        _setupCompassRose : function($compassRose, closeOnClick) {
            $compassRose.find('.compass_rose_button').each(function(i,button) {
                $(button).button({
                    text: false,
                    icons: { primary: self._mapCompassRoseDirectionToIcon(button.value) }
                })
                    .click(function() {
                        self._updatePlacetypeCardinalDirection(this.value);
                        if (closeOnClick) {
                            $compassRose.css('display', 'none');
                        }
                    });
            });
            $compassRose.htmlClean(); // Needed to remove whitespace from line breaks between buttons!
        },
        /**
         * Creates a simple placetype rectangle of the given color
         * @param colorhex
         * @return {*}
         * @private
         */
        _makePlacetypeMarkup : function(colorhex) {
            // div is a dummy holder
            div = $("<div />");
            span = $("<span />");
            span.attr('style', $.format("background: {0}; color: {0}", [colorhex])).text('XXXX');
            div.append(span);

            return div.html();
        },

        _mapCompassRoseDirectionToIcon : function(cardinalDirection) {
            return cardinalDirection=='C' ?
                'ui-icon-bullet':
                $.format("ui-icon-arrowthick-1-{0}", cardinalDirection.toLowerCase());
        },

        // Load the placetype data into the Placetypes dialog
        _loadPlacetypes : function(placetypes) {
            var self = this;
            var config = {
                ptid:{title:'PTID',width:40, sorttype:'int',
                    map:function(ptid) {
                        // Make this an int for sorting
                        return parseInt(ptid);
                    }},
                name:{title:'Placetype Name',width:175},
                colorhex:{title:'Color',
                    width:52,
                    map:function(colorhex) {return self._makePlacetypeMarkup(colorhex)}
                },
                compassrose:{title:"<div class='compass_rose_header'></div>",
                    width:20,
                    map:function(nothing) {
                        return "<div class='compass_rose_table_cell'></div>";
                    },
                    postGridCreate:function() {
                        //This must happen post creation of the grid, othewise jquery ui function fails
                        self.placetypeTableSelector.select('.compass_rose_table_cell').each(function(i,div) {
                            $(div).append(self._getPlacetypeCardinalDirectionButton('C'));
                        });
                    }
                }
            };
            var columnOrder = ['ptid', 'name', 'colorhex'].concat(this.compassRoseEnabled ? ['compassrose'] : []);
            // Set up a jQuery.jqGrid to host the placetype data
            self.placetypeTableSelector.jqGrid({
                //cache : false,
                datatype : "local",
                height : "100%",
                colNames : $.map(columnOrder, function(field) {
                    return config[field].title;
                }),
                colModel : $.map(columnOrder, function(field) {
                    return {index:field, name:field, width:config[field].width, sorttype:config.sorttype ? config.sorttype : 'string'};
                }),
                multiselect: false,
                pager: '#placetype_pager',
                shrinkToFit: true,
                onSelectRow: function(id){
                    data_row = $("#placetype_table").getRowData(id);
                    // Update active placetype
                    self._updatePlacetype(data_row.ptid);
                }
            });

            self.placetypeTableSelector.jqGrid('navGrid',"#placetype_pager",{
                edit:false,
                add:false,
                del:false,
                autoResize:true
            }); //fix selection

            // Iterate through the placetypes, adding each to the grid as a row
            $.each(placetypes, function(index, placetype) {
                var rowData = jQuery.mapToDictionary(columnOrder, function(field) {
                    return [field, config[field].map ?
                        config[field].map(placetype[field]) :
                        placetype[field]];
                });
                self.placetypeTableSelector.jqGrid(
                    'addRowData',
                    index + 1,
                    rowData
                );
            });

            // Each field can post process its cells here, thought it has to select them
            // since the grid doesn't expose a function that returns the cell HTML DOM elements
            jQuery.map(columnOrder, function(field) {
                if (config[field].postGridCreate)
                    config[field].postGridCreate();
            });
        },

        /**
         *  Updates values and controls dependent on the current placetype selection
         * @param placetypeId
         */
        _updatePlacetype : function(placetypeId) {
            var self = this;
            this.activePlacetypeId = data_row.ptid;
            $(".activePlacetypeRow").html(data_row.name);
            // Copy the row data to our active label
            $('.activePlacetypeRow').empty();
            var cellData = $('.jqgrow.ui-row-ltr.ui-state-highlight > td').map(function(i,td) {
                return $(td).html();
            });
            var selection  =d3.select('.activePlacetypeRow').selectAll('span')
                .data(cellData, function(d) {return d});
            selection
                .enter()
                .append('span')
                .html(function(d) {return d;})
                .classed('activePlacetypeData', true);
            selection
                .exit()
                .remove();

            // Recreate the cloned button's jquery ui properties
            $('.activePlacetypeRow').find('button').empty().button({
                text: false,
                icons: {
                    primary:
                        mapCompassRoseDirectionToIcon(self.activeCardinalDirection())
                }
            })
                .click(function() {
                    if ($(this).find('.compass_rose').length > 0) {
                        $(this).find('.compass_rose').css('display', 'block');
                    }
                    else {
                        $compassRose = $('.placetype_container').find('.compass_rose');
                        if ($compassRose.length > 0) {
                            var $clone = $compassRose.clone(false,false)
                            .addClass('compass_rose_for_label')
                            .css('top','-30px')
                            .css('left','180px')
                            .css('z-index', 100000)
                            .appendTo($('.activePlacetypeRow'));
                        self.setupCompassRose($clone, true);
                    }
                }
            });
            // Update the position of the compass rose, if active, to that of the selected placetype ro

            $compassRose = $('.compass_rose');
            self._positionCompassRose($compassRose);
        },

        _updatePlacetypeCardinalDirection : function(cardinalDirection) {
            $compassRoseTableButton = $('.jqgrow.ui-row-ltr.ui-state-highlight').find('.compass_rose_table_button')
                .add($('.activePlacetypeRow').find('.compass_rose_table_button'));
            $compassRoseTableButton.each(function(i,button) {
                $(button).button('option', 'icons', {primary:mapCompassRoseDirectionToIcon(cardinalDirection)});
                button.value = cardinalDirection;
            });
            // Also store the actual value in the button
        },
        /**
     * TODO This makes no sense, since activePlacetypeId is a property delete it
     * The currently selected placetype's id
     * Optionally specifiy a placetypeId to set the placetype
     * @return {*}
     */
    /*
     this.activePlacetypeId = function(placetypeId) {
     if (placetypeId) {
     if (this.placetypes[placetypeId]) {
     this.activePlacetypeId = placetypeId;
     $('.placetype_table').jqGrid(
     "setSelection",
     this.orderedPlacetypes.indexOf(this.placetypes[placetypeId])+1);
     }
     }
     return this.activePlacetypeId;
     };
     */

        _getPlacetypeCardinalDirectionButton : function(cardinalDirection) {
            return $('<button></button>').button({
                text: false,
                icons: {
                    primary:
                        mapCompassRoseDirectionToIcon(cardinalDirection)
                }
            }).addClass('compass_rose_table_button').attr('value',cardinalDirection);
        },
        _positionCompassRose : function($compassRose) {
            if (!this.activePlacetypeId || !this.compassRoseEnabled) {
                return
            }
            $compassRose.css('display', 'block');
            var $placetypeContainer = $('.placetype_container'),
                $table = $('#gbox_placetype_table'),
                tableWidth = $table.position().left + $table.outerWidth(true);
            if ($placetypeContainer.width() - tableWidth < $compassRose.width()) {
                $placetypeContainer.width(tableWidth + $compassRose.outerWidth(true)+10);
            }
            // Find the position of the selected tr element relative to its parent
            $compassRose.position({
                of:  $placetypeContainer.find('.jqgrow.ui-row-ltr.ui-state-highlight'),
                my: 'left center',
                at: 'left center',
                offset:$.format("{0} {1}", $table.outerWidth(), 0),
                collision: 'fit'
            });
        }
    });

}(jQuery));

