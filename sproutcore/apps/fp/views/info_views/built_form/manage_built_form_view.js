Footprint.ManageBuiltFormView = SC.View.extend({

    // Set this to the BuiltForm subclass
    recordType: null,

    recordsEditController: null,

    content: null,
    contentBinding: SC.Binding.oneWay('*recordsEditController.arrangedObjects'),

    selection: null,
    selectionBinding: SC.Binding.from('*recordsEditController.selection'),

    selectedItem: null,
    selectedItemBinding: SC.Binding.from('*selection.firstObject')
});