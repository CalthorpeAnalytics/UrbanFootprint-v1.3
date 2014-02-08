/**
 * This jQuery ui cass displays an undo, redo, clear button and keeps track of an undo buffer
 * The widget looks for buttons with andy of thgree classes: ui-undoredo-[undo|redo|clear] and makes them into the respective button. It uses the given text of the button element to label the buttons or default to English labels
 *
 * Andy Likuski
 */
(function( $, undefined ) {

var UNDO_CLASS = '.ui-undoredo-undo';
var REDO_CLASS = '.ui-undoredo-redo';
var CLEAR_CLASS = '.ui-undoredo-clear';
$.widget("ui.undoredo", {
    options: {
        compareFunction: function(data1, data2) {
            return $.deepEquals(data1,data2);
        },
        labels: {
            undo:'Undo',
            redo:'Redo',
            clear:'Clear'
        },
        clone: null // a function to clone the data. For use by the clear button
    },
    /**
     * Creates an Undo Buffer
     * @constructor
    **/
    _create: function() {
        var self = this;
        this.buffer = [];
        this.index = 0;

        var undoText = this.element.find(UNDO_CLASS).text();
        this.element.find(UNDO_CLASS).button({
            label: undoText || this.options.labels.undo,
            icons: {
                primary: "ui-icon-triangle-1-w"
            }
        })
            .click(function() {
                self.undo();
            });

        var redoText = this.element.find(REDO_CLASS).text();
        this.element.find(REDO_CLASS).button({
            label: redoText || this.options.labels.redo,
            icons: {
                primary: "ui-icon-triangle-1-e"
            }
        })
            .click(function() {
                self.redo();
            });
        var clearText = this.element.find(CLEAR_CLASS).text();
        this.element.find(CLEAR_CLASS).button({
            label: clearText || this.options.labels.clear,
            icons: {
                primary: "ui-icon-trash"
            }
        })
            .click(function() {
                self.clear();
            });
    },
    add: function(data) {
        // Only add the data to the buffer if it's different than the current data
        if (!this.current() || !this.options.compareFunction(this.current(), data)) {
            this._removeAfterCurrent();
            this.buffer.push(data);
            this.index = this.buffer.length-1;
            this._setButtonStates();
        }
    },
    _removeAfterCurrent:  function() {
        this.buffer = this.buffer.slice(0,this.index+1);
    },
    redo:  function() {
        if (this.index+2 > this.buffer.length) {
            throw "Tried to advance buffer index beyond last item";
        }
        this.index += 1;
        this._setButtonStates();
        this._trigger('redo', null, {data:this.current()});
        return this.current();
    },
    undo: function() {
        if (this.index==0) {
            throw "Tried to retract buffer index beyond first item";
        }
        this.index -=1;
        this._setButtonStates();
        this._trigger('undo', null, {data:this.current()});
        return this.current();
    },
    /**
     * Adds the initial state to the end of the buffer. This assumes the initial state is "clear"
     * By doing this we can still undo to previous states
     * @return {*}
     */
    clear: function() {
        if (this.options.clone) {
            this.add(this.options.clone(this.buffer[0]));
            this._trigger('clear', null, {data:this.current()});
            return this.current();
        }
        throw "clone function must be defined in order to use the clear button"
    },
    current: function() {
        return this.buffer[this.index];
    },
    _setButtonStates: function() {
        this.element.find(UNDO_CLASS).button('option','disabled', this.atFirstPosition());
        this.element.find(REDO_CLASS).button('option','disabled', this.atLastPosition());
        this.element.find(CLEAR_CLASS).button('option','disabled', this.atFirstPosition() ||
            this.options.compareFunction(this.current(), this._first()));
    },
    _first: function() {
        return this.buffer[0];
    },
    atFirstPosition: function() {
        return this.index == 0;
    },
    atLastPosition: function() {
        return this.index == this.buffer.length-1;
    }
});

}(jQuery));
