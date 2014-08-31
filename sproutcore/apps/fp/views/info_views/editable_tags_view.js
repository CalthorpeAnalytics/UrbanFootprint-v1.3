/* 
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 * 
 * Copyright (C) 2012 Calthorpe Associates
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('views/copy_button_view');
sc_require('views/editable_model_string_view');
sc_require('views/label_select_view');
sc_require('views/delete_button_view');

Footprint.EditableTagsView = SC.View.extend({

    classNames: ['footprint-editable-tags-view'],
    childViews:['titleView', 'tagsScrollView', 'tagsSelectOrAddView'],
    // The distint tags of the FeatureBehavior
    content: null,
    // The tags of the FeatureBehavior and those inherited from the Behavior
    computedTags: null,

    titleView: SC.LabelView.extend({
        layout: {height: 12, top: 0},
        classNames: ['footprint-editable-title-view'],
        value: 'Tags'
    }),

    tagsScrollView: SC.ScrollView.extend({
        classNames: ['footprint-editable-tags-scroll-view'],
        layout: {top: 15, bottom: 60},

        content:null,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        computedTags:null,
        computedTagsBinding: SC.Binding.oneWay('.parentView.computedTags'),

        contentView: SC.SourceListView.extend({
            isEnabledBinding: SC.Binding.oneWay('.content').bool(),
            rowHeight: 20,
            isEditable: NO,
            actOnSelect: NO,
            tags: null,
            tagsBinding: SC.Binding.oneWay('.parentView.parentView.content'),
            contentBinding:SC.Binding.oneWay('.parentView.parentView.computedTags'),

            exampleView: SC.View.extend(SC.Control, {
                classNames: ['footprint-tag-source_list_item-view'],
                layout: { height: 24 },
                childViews: ['removeButtonView', 'nameLabelView'],
                // Content is what we are editing, which is a Tag instance
                content: null,

                removeButtonView: Footprint.DeleteButtonView.extend({
                    layout: { left: 0, width: 16, centerY: 0, height: 16},
                    action: 'doRemoveRecord',
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    tags: null,
                    tagsBinding: SC.Binding.oneWay('.parentView.parentView.tags'),
                    // Only allow removal of tags owned by the FeatureBehavior, not
                    // those of the Behavior
                    isVisible: function() {
                        return (this.get('tags') || []).contains(this.get('content'));
                    }.property('content', 'tags').cacheable()
                }),

                nameLabelView: Footprint.EditableModelStringView.extend({
                    classNames: ['footprint-editable-content-view'],
                    layout: { left: 20, width:370 },
                    isEditable: NO,
                    valueBinding: SC.Binding.oneWay('.parentView*content.tag')
                })
            })
        })
    }),

    tagsSelectOrAddView: SC.View.extend({
        layout: {bottom:0, height: 60},
        childViews: ['tagsLabelSelectView', 'tagsAddView'],
        /***
         * Select an existing tag to add to the content.
         */
        tagsLabelSelectView: Footprint.LabelSelectView.extend({
            layout: { height: 24, top: 5},
            classNames: ['footprint-editable-tags-label-select-view'],
            contentBinding: SC.Binding.oneWay('Footprint.behaviorTagsEditController.arrangedObjects'),
            // Clicking will add the tag--no need to select
            isSelectable: NO,
            // Our content is aggregated from behaviors--it has no status
            contentStatus: SC.Binding.oneWay('Footprint.behaviorsEditController.status'),
            itemTitleKey: 'name',
            nullTitle: 'Add an existing tag',
            selectionAction: 'doPickTag'
        }),

        /***
         * Add a new tag
         */
        tagsAddView: SC.View.extend({
            layout: {top: 34, height: 24},
            classNames: ['footprint-editable-tags-add-view'],
            childViews: ['inputView', 'addButtonView'],

            content:null,
            contentBinding: SC.Binding.oneWay('.parentView.content'),

            inputView: Footprint.EditableModelStringView.extend({
                classNames: ['footprint-editable-content-view'],
                layout: {left: 25},

                // The tags of the FeatureBehavior
                content:null,
                contentBinding: SC.Binding.oneWay('.parentView.content'),

                tagIsInFeatureBehavior: function() {
                    return (this.get('content') || []).find(function(tag) {
                        return tag.get('tag') == this.get('value');
                    }, this);
                }.property('content').cacheable()
            }),
            addButtonView: Footprint.CopyButtonView.extend({
                layout: {left: 0, width: 16, centerY:0, height: 16},
                value: null,
                valueBinding: SC.Binding.oneWay('.parentView.inputView.value'),
                tagIsInFeatureBehavior: null,
                // Just block tag names already in the feature_behavior.tags
                isEnabledBinding: SC.Binding.oneWay('.parentView.inputView.tagIsInFeatureBehavior').not(),
                action: 'doAddTag'
            })
        })
    })
});

// Depricated
Footprint.TagsInfoView = Footprint.InfoView.extend({
    classNames: "footprint-tags-info-view".w(),
    title: 'Tags',
    contentView: Footprint.LabelSelectView.extend({
        contentBinding: parentViewPath(2, '.content'),
        selectedItemBinding: '.parentView.parentView*controller.selection.firstObject',
        itemsBinding: parentViewPath(3,'*recordSetController.keyObjects'),
        valuesBinding: parentViewPath(2,'*content.tags')
    })
});
