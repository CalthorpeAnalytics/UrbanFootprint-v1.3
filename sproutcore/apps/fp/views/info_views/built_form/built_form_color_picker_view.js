/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/16/13
 * Time: 2:11 PM
 * To change this template use File | Settings | File Templates.
 */


Footprint.BuiltFormColorPickerView = SC.View.design({
    childViews: ['colorPreviewCV', 'colorPreview1CV', 'colorPreview2CV', 'hslSlidersCV', 'cssTextCV'],
    classNames: ['demo-content'],
    layout: { left: 30, width: 600, height: 260, top: 250 },
    selection: null,

    color: null,
    colorBinding: SC.Binding.oneWay('*selection.medium').transform(function(medium) {
        if (medium)
            return medium.getPath('content.fill.color');
        return '#4682B4'
    }),

    colorPreviewCV: SC.View.design({
      classNames: ['color-preview'],
      backgroundColorBinding: SC.Binding.oneWay('.parentView.color'),

      displayProperties: ['backgroundColor'],

      layout: { border: 1, left: 15, top: 15, width: 170, height: 120 }
    }),

    colorPreview1CV: SC.ImageButtonView.design({
      action: function() {
        var brighterColor = Footprint.mainViewController.get('brighterColor');

        Footprint.mainViewController.set('hue', brighterColor.get('hue'));
        Footprint.mainViewController.set('saturation', brighterColor.get('saturation'));
        Footprint.mainViewController.set('luminosity', brighterColor.get('luminosity'));
      },
      backgroundColorBinding: SC.Binding.oneWay('Footprint.mainViewController.brighterCssText'),
      classNames: ['color-sub-preview'],
      layout: { border: 2, left: 20, top: 20, width: 20, height: 20 }
    }),

    colorPreview2CV: SC.ImageButtonView.design({
      action: function() {
        var darkerColor = Footprint.mainViewController.get('darkerColor');

        Footprint.mainViewController.set('hue', darkerColor.get('hue'));
        Footprint.mainViewController.set('saturation', darkerColor.get('saturation'));
        Footprint.mainViewController.set('luminosity', darkerColor.get('luminosity'));
      },
      backgroundColorBinding: SC.Binding.oneWay('Footprint.mainViewController.darkerCssText'),
      classNames: ['color-sub-preview'],
      layout: { border: 2, left: 158, top:105, width: 20, height: 20 }
    }),

    hslSlidersCV: SC.View.design({
      childViews: ['hTitle', 'hCV', 'hValueCV', 'sTitle', 'sCV', 'sValueCV', 'lTitle', 'lCV', 'lValueCV'],
      layout: { top: 10, right: 15, left:190, height:130 },

      hTitle: SC.LabelView.design({
        classNames: ['slider-title'],
        layout: { left: 10, width: 20, height: 24, top: 0 },
        localize: true,
        value: 'H'
      }),
      hCV: SC.SliderView.design({
        layout: { left: 50, right: 50, height: 24, top: 0 },
        minimum: 0,
        maximum: 359,
        step: 1,
        valueBinding: SC.Binding.from('Footprint.mainViewController.hue')
      }),
      hValueCV: SC.LabelView.design({
        classNames: ['slider-value'],
        layout: { right: 10, width: 35, height: 24, top: 0 },
        valueBinding: SC.Binding.oneWay('Footprint.mainViewController.hue').
          transform(function(hue) {
            return parseInt(hue, 10) + '°';
          })
      }),

      sTitle: SC.LabelView.design({
        classNames: ['slider-title'],
        layout: { left: 10, width: 20, height: 24, top: 35 },
        localize: true,
        value: 'S'
      }),
      sCV: SC.SliderView.design({
        layout: { left: 50, right: 50, height: 24, top: 35 },
        step: 0.01,
        valueBinding: SC.Binding.from('Footprint.mainViewController.saturation')
      }),
      sValueCV: SC.LabelView.design({
        classNames: ['slider-value'],
        layout: { right: 10, width: 35, height: 24, top: 35 },
        valueBinding: SC.Binding.oneWay('Footprint.mainViewController.saturation').
          transform(function(saturation) {
            return parseInt(saturation * 100, 10) + '%';
          })
      }),

      lTitle: SC.LabelView.design({
        classNames: ['slider-title'],
        layout: { left: 10, width: 20, height: 24, top: 70 },
        localize: true,
        value: 'L'
      }),
      lCV: SC.SliderView.design({
        layout: { left: 50, right: 50, height: 24, top: 70 },
        step: 0.01,
        valueBinding: SC.Binding.from('Footprint.mainViewController.luminosity')
      }),
      lValueCV: SC.LabelView.design({
        classNames: ['slider-value'],
        layout: { right: 10, width: 35, height: 24, top: 70 },
        valueBinding: SC.Binding.oneWay('Footprint.mainViewController.luminosity').
          transform(function(luminosity) {
            return parseInt(luminosity * 100, 10) + '%';
          })
      })
    }),

    cssTextCV: SC.TextFieldView.design({
      classNames: ['color-text'],
      controlSize: SC.LARGE_CONTROL_SIZE,
      isEditable: YES,
      layout: { left: 100, right: 100, bottom: 75, height: 30 },

//      parentColor: null,
//      parentColorBinding: SC.Binding.oneWay('.parentView.color'),
//
//      newColor: null,
//      newColorBinding: SC.Binding.oneWay('Footprint.mainViewController.cssText'),
//      value: function(){
//            var value = this.get('parentColor');
//            if (value)
//                return value;
//            return this.get('newColor')
//           }.property('parentColor').cacheable()

       valueBinding: SC.Binding.oneWay('Footprint.mainViewController.cssText')
    })
})