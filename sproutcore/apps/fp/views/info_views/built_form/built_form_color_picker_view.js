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

    medium: null,
    mediumContent: null,
    mediumContentBinding: SC.Binding.oneWay('*medium.content'),
    mediumContentDidChange: function() {
        var cssText = this.getPath('mediumContent.fill.color') || null;
        // Use setIfChanged to prevent infinite loops in this dependency circle
        this.get('color').setIfChanged('cssText', cssText);
    }.observes('mediumContent'),
    color: null,

    cssText: null,
    cssTextBinding: SC.Binding.oneWay('.color.cssText'),
    cssTextDidChange: function() {
        if (!this.get('medium')) return;
        var cssText = this.getPath('color.cssText'),
            currentCssText = this.getPath('mediumContent.fill.color');
        if ((cssText || '').toUpperCase() !== (this.getPath('mediumContent.fill.color') || '').toUpperCase()) {
            var mediumContent = this.get('mediumContent');
            if (!mediumContent) return null;
            mediumContent = SC.clone(mediumContent, YES);
            mediumContent.fill.color = cssText;
            this.getPath('medium').setIfChanged('content', mediumContent);
        }
    }.observes('.color.cssText'),

    init: function() {
      this.color = SC.Color.create();
      return sc_super();
    },
    destroy: function() {
      this.color.destroy();
      return sc_super();
    },

    brighterColor: function() {
      var color = this.get('color'),
          ret = color.mult(1.25);

      return ret.set('a', 1);
    }.property('cssText').cacheable(),

    darkerColor: function() {
      var color = this.get('color'),
          ret = color.mult(0.75);

      return ret.set('a', 1);
    }.property('cssText').cacheable(),

    colorPreviewCV: SC.View.design({
      classNames: ['color-preview'],
      backgroundColorBinding: SC.Binding.oneWay('.parentView.color.validCssText'),

      displayProperties: ['backgroundColor'],

      layout: { border: 1, left: 15, top: 15, width: 170, height: 120 }
    }),

    colorPreview1CV: SC.ImageButtonView.design({
      action: function() {
        var brighterColor = this.parentView.get('brighterColor');
        this.parentView.color.set('cssText', brighterColor.get('cssText'));
      },
      isEnabledBinding: SC.Binding.oneWay('.parentView.color.isError').not(),
      backgroundColorBinding: SC.Binding.oneWay('.parentView*brighterColor.validCssText'),
      displayProperties: ['backgroundColor'],
      classNames: ['color-sub-preview'],
      layout: { border: 2, left: 20, top: 20, width: 20, height: 20 }
    }),

    colorPreview2CV: SC.ImageButtonView.design({
      action: function() {
        var darkerColor = this.parentView.get('darkerColor');
        this.parentView.color.set('cssText', darkerColor.get('cssText'));
      },
      isEnabledBinding: SC.Binding.oneWay('.parentView.color.isError').not(),
      backgroundColorBinding: SC.Binding.oneWay('.parentView*darkerColor.validCssText'),
      displayProperties: ['backgroundColor'],
      classNames: ['color-sub-preview'],
      layout: { border: 2, left: 158, top:105, width: 20, height: 20 }
    }),

    hslSlidersCV: SC.View.design({
      childViews: ['hTitle', 'hCV', 'hValueCV', 'sTitle', 'sCV', 'sValueCV', 'lTitle', 'lCV', 'lValueCV'],
      layout: { top: 10, right: 15, left:190, height:130 },

      isEnabledBinding: SC.Binding.oneWay('.parentView.color.isError').not(),

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
        valueBinding: SC.Binding.from('.parentView.parentView.color.hue')
      }),
      hValueCV: SC.LabelView.design({
        classNames: ['slider-value'],
        layout: { right: 10, width: 35, height: 24, top: 0 },
        valueBinding: SC.Binding.oneWay('.parentView.parentView.color.hue').
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
        valueBinding: SC.Binding.from('.parentView.parentView.color.saturation')
      }),
      sValueCV: SC.LabelView.design({
        classNames: ['slider-value'],
        layout: { right: 10, width: 35, height: 24, top: 35 },
        valueBinding: SC.Binding.oneWay('.parentView.parentView.color.saturation').
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
        valueBinding: SC.Binding.from('.parentView.parentView.color.luminosity')
      }),
      lValueCV: SC.LabelView.design({
        classNames: ['slider-value'],
        layout: { right: 10, width: 35, height: 24, top: 70 },
        valueBinding: SC.Binding.oneWay('.parentView.parentView.color.luminosity').
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

       valueBinding: SC.Binding.from('.parentView.color.cssText')
    })
})