// ==========================================================================
// Project:   MyApp.CustomItemListView
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals MyApp */

/** @class

    (Document Your View Here)

 @extends SC.View
 */
MyApp.CustomListItemView = SC.View.extend(SC.ContentDisplay, {

    classNames: ['custom-list-item-view'],

    isTitleVisible: YES,

    displayProperties: 'isSelected isEnabled isTitleVisible'.w(),

    contentDisplayProperties: 'fname lname company title',

    render: function(context, firstTime) {

        var content = this.get('content');
        var fname = content.get('fname');
        var lname = content.get('lname');
        var company = content.get('company');
        var title = content.get('title');
        var isSelected = this.get('isSelected');
        var isEnabled = this.get('isEnabled');
        var contentIndex = this.get('contentIndex');
        var isTitleVisible = this.get('isTitleVisible');
        var isCompanyVisible = this.get('isCompanyVisible');

        var isEven = contentIndex % 2 ? YES : NO;

        context = context.setClass({ 'odd': !isEven, 'even': isEven });

        var standard = isEnabled && !isSelected;
        var selected = isEnabled && isSelected;
        var disabled = !isEnabled;
        var classes = { 'standard': standard, 'selected': selected, 'disabled': disabled };

        context = context.begin().addClass('top').setClass(classes);
        context = context.begin('p').addClass('name').push('%@, %@'.fmt(lname, fname)).end();
        context = context.end(); // div.top

        context = context.begin().addClass('bottom').setClass(classes);

        context = context.begin('p').addClass('item').addClass('company');
        context = context.begin('span').addClass('label').push('Company:').end();
        context = context.begin('span').addClass('value').push(company).end();
        context = context.end(); // p.label.company

        if (isTitleVisible) {
            context = context.begin('p').addClass('item').addClass('title');
            context = context.begin('span').addClass('label').push('Title:').end();
            context = context.begin('span').addClass('value').push(title).end();
            context = context.end(); // p.label.title
        }

        context = context.end(); // div.bottom

        sc_super();
    }

});

