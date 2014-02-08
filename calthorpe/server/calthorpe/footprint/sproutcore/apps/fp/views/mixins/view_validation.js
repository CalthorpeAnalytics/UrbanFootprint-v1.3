
 /* 
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2013 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

Footprint.ViewValidation = {
    classNameBindings:'viewIsInvalid', // adds the is-invalid class if the view doesn't validate

    /***
     * A list of view properties that must be non-null whenever the validationController is READY_CLEAN
     */
    requiredProperties:''.w(),
    /***
     * A controller whose status triggers validation
     */
    validationController:null,

    /***
     * Property to set to YES if validation fails
     */
    viewIsInvalid:null,
    /***
     * The subset of requiredProperties that are null
     */
    invalidProperties:[],

    didCreateLayer: function() {
        //this.validate();
    }
    /*
    This is causing unbinding errors
    validate: function() {
        // Let all the bindings complete before validationg
        this.invokeLast(function() {
            if (this.getPath('validationController.status') === SC.Record.READY_CLEAN) {
                this.set('invalidProperties', this.get('requiredProperties').filter(function(requiredProperty) {
                    var value = this.getPath(requiredProperty);
                    return null === value || undefined === value;
                }, this));
            }
            else
                this.set('invalidProperties', []);
            this.set('viewIsInvalid', this.get('invalidProperties').length > 0);
            if (this.get('viewIsInvalid')) {
                logError("View %@ has null/undefined requiredProperties: %@".fmt(this.toString(), this.get('invalidProperties').join(',')));
                logError(this.$()[0]);
            }
        });
    }.observes('*validationController.status')
    */
};