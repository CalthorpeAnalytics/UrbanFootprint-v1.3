/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/16/13
 * Time: 2:14 PM
 * To change this template use File | Settings | File Templates.
 */



Footprint.mainViewController = SC.ObjectController.create({

  content: SC.Color.from('steelblue').set('a', 1.0),

  brighterColor: function() {
    var color = this.get('content');

    return color.mult(1.25);
  }.property('cssText').cacheable(),

  brighterCssText: function() {
    var brighterColor = this.get('brighterColor');

    return brighterColor.get('cssText');
  }.property('brighterColor').cacheable(),

  darkerColor: function() {
    var color = this.get('content');

    return color.mult(0.75);
  }.property('cssText').cacheable(),

  darkerCssText: function() {
    var darkerColor = this.get('darkerColor');

    return darkerColor.get('cssText');
  }.property('darkerColor').cacheable()

});