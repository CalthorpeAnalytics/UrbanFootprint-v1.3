
/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2014 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/



// Allows the user to view and change the PresentationMedium's DbEntityInterest's DbEntity's key
// The user would most likely only change the key after uploading a new layer. For instance, if the
// user uploaded a new constraints layer they would want to key it with 'constraint' if they failed to so
// at the time of upload.
// In the future edits should only be permitted if the DbEntityInterest.interest indicates that the ConfigEntity
// owns the DbEntity.
Footprint.KeyInfoView = Footprint.InfoView.extend({
    classNames: "footprint-key-info-view".w(),
    title: 'Key',

    contentView: SC.View.extend({
        layout: {left: .2, width: .8},
        /*
        showKeySelect:YES,
        isEditable:YES,
        // The content of the key at keyitemPath
        contentBinding: parentViewPath(2,'*content'),

        // The path from content to the selected key
        keyItemPathBinding: parentViewPath(1,'*keyItemPath'),

        valueBinding: parentViewPath(3, '*editController.key'),
        // An Object that organizes the DbEntities by key. Used to determine if the DbEntity has a unique key
        itemsByKeyBinding: SC.Binding.oneWay(parentViewPath(3, '*recordSetController.dbEntityInterestsByKey')),
        // In the event that a key is shared, this Object maps each key to the selected DbEntity, which
        // determines if the item is checked
        selectedItemByKeyBinding: SC.Binding.oneWay(parentViewPath(3, '*recordSetController.selectedDbEntityInterestsByKey')),
        // All of the available keys from which to choose a new value. The user should also be able to make up
        // a new key.
        keysBinding: SC.Binding.oneWay(parentViewPath(3, '*recordSetController.keys'))
        */
    })
});
