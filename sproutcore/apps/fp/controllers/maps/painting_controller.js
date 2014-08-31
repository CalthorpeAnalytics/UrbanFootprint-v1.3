
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

Footprint.paintingController = SC.Object.create({

    // sends geometry to a view that will use it for intersecting with a DB layer
    query_result_ids: [],

    selectWithBrush: function() {
        if (d3.select('.polybrush').node != null) {
            this.sendPolyBrush()
        }
        else this.sendBrush();
    },

    sendBrush: function() {
        var bGeom = Footprint.Geometry.makeBrushGeom();

        if (!bGeom) {
            return;
        }
        geom = Footprint.Geometry.projectPolygon(bGeom);
        Footprint.Painting.sendGeometry(geom, "run_intersection_query")
    },

    sendPolyBrush: function() {
        bGeom = Footprint.Geometry.makePolybrushGeom();

        if (!bGeom) {return;}

        geom = Footprint.Geometry.projectPolygon(bGeom);
        Footprint.Painting.sendGeometry(geom, "run_intersection_query");
    },

    activeBuiltFormId: function() {
        if (Footprint.builtFormActiveController.get('content', false)) {
            return Footprint.builtFormActiveController.get('content').get('id'); }
        else { return false; }
    },

    updateBuiltFormWithSelection: function() {
        var activeGroup = Footprint.mapLayerGroups.scenario_built_form_layer;
        var layer = activeGroup.raster;
        var selection = activeGroup.selection;

        if (selection.length == 0) {
            SC.Logger.warn("Nothing selected!");
            return false }
        else {
            SC.Logger.debug("Appling built forms to %@ selectinos".fmt(selection.length));
            var featureData = this.getTableInfo();
            //        var style = builtForm.color;
            postData = 'feature_data=%@'.fmt(encodeURIComponent(JSON.stringify(featureData)));

            var self = this;
            $.ajax({
                url : "/footprint/update_with_selection",
                type : "POST",
                data : postData,
                dataType:'json',
                error : function() {
                    layer.reload();
                    self.deselectAll();
                },
                success : function() {
                    //                stylePaintedParcels(builtForm.color);
                    layer.reload();
                    self.deselectAll();
                }
            });
            return true;
        }
    },

    getTableInfo: function() {
        var activeGroup = Footprint.mapLayerGroups.scenario_built_form_layer
        var scenario = Footprint.scenarioActiveController.get('content')
        var layer = activeGroup.raster;
        var selection = activeGroup.selection;
        return {
            scenario: scenario.get('id'),
            layer: Footprint.layerActiveController.get('content').toJSON(),
            built_form: this.activeBuiltFormId(),
            user: Footprint.userController.get('content').firstObject().toJSON()
        };
    },

    updateBuiltFormWithGeography: function() {
        featureData = this.getTableInfo();
        featureData.geometry = projectPolygon(bGeom);
        featureData.built_form = this.activeBuiltFormId();
        layer = Footprint.mapLayerGroups.scenario_built_form_layer
        postData = "feature_data=%@".fmt(encodeURIComponent(JSON.stringify(featureData)));

        result = $.ajax({
            url : "/footprint/update_with_geography",
            type : "POST",
            data : postData,
            error : function() {
                layer.vector.reload();
                layer.raster.reload();
            },
            success : function() {
                layer.raster.reload();
                layer.vector.reload();
            }
        });
    },

    deselectAll: function() {
        featureData = this.getTableInfo();
        layer = Footprint.mapLayerGroups.scenario_built_form_layer
        postData = "feature_data=%@".fmt(encodeURIComponent(JSON.stringify(featureData)));
        result = $.ajax({
            url : "/footprint/deselect_all",
            type : "POST",
            data : postData,
            error : function() {
                layer.selection_layer.reload();
                layer.selection_layer.reload();
            },
            success :  function() {
                layer.selection_layer.reload();
                layer.selection_layer.reload();
            }
        });
    },

    // TODO this isn't working yet
    getSelectedFeatures: function(success) {
        var featureData = this.getTableInfo();
        var featureDataString = encodeURIComponent(JSON.stringify(featureData));
        $.ajax({
            url : "/footprint/get_selected_features",
            type : "GET",
            data : featureDataString,
            error : function() { return alert('update failed') },
            success: function(data) {
                success(data);
            }
        });
    },

    getExtentFromSelection: function() {
        var layer = findActiveLayer();
        if (layer.selection.length == 0) { return false }

        else {
            var post = {
                selection: layer.selection,
                layer: layer.id()
            };
        }
        postData = $.format("feature_data={0}",
            encodeURIComponent(JSON.stringify(post))
        );
        $.ajax({
            url : "/footprint/get_selection_bbox",
            type : "POST",
            data : postData,
            error : function() { return alert('update failed') },
            success: parsePostGISExtent
        });
    },

    parsePostGISExtent: function(postGISExtent) {
        var bbox = postGISExtent.bbox.replace('(','').replace(')','').replace('BOX','').split(',');
        bbox[0] = bbox[0].split(" "); bbox[1] = bbox[1].split(" ");
        var Extent = [{'lon': parseFloat(bbox[0][0]), 'lat': parseFloat(bbox[0][1])},
            {'lon':parseFloat(bbox[1][0]), 'lat': parseFloat(bbox[1][1])} ];
        return Extent;
    },

    getInfoFromSelection: function(field) {
        var layer = findActiveLayer();

        if (layer.selection.length == 0) { return false }
        else {

            var post = {
                selection: layer.selection,
                field: field,
                layer: layer.id()
            };

            var postData = $.format("feature_data={0}", encodeURIComponent(JSON.stringify(post)));

            $.ajax({
                url : "/footprint/scenario/1/get_info_from_selection",
                type : "POST",
                data : postData,
                error : function() { return alert('update failed') },
                success: getInfoResponse
            });
        }
    },

    selectionResponse: function(resultData) {

        var activeLayerKey = Footprint.layerActiveController.get('content').toJSON().db_entity_key;
        var layerGroup = Footprint.mapLayerGroups[activeLayerKey];

        layerGroup.selection = resultData['selected_ids'];

        if (layerGroup.vector.visible() === true) {
            var parcels = d3.selectAll('.parcel_geometry');
            selectFeaturesByIdArray(parcels, resultData['selected_ids'])
        }

        if (layerGroup.raster.visible() === true) {
            layerGroup.selection_layer.reload();
        }
    },

    getInfoResponse: function(resultData) {
        var resultString= resultData.selected_values;
        window.resultDataList.append[resultData];
    },

    stylePaintedParcels: function(style) {
        return d3.selectAll('.selected').style('fill', style).classed('selected', false);
    },

    updateParcelAttributes: function(id) {

    },

    selectFeature: function(f, event) {
        // identify a vector feature as selected to represent selection visually
        var selected_class =  f.element.getAttribute("class") + " selected";
        f.element.setAttribute("class", selected_class);
    },

    unselect: function() {
        var sel = d3.selectAll(".selected");
        if (sel.node()!=null) {
            var unsel = sel.attr("class").replace(" selected", "");
            sel.attr("class", unsel);
        }
        Footprint.mapLayerGroups.scenario_built_form_layer.selection = [];
        Footprint.Painting.deselectAll();
        Footprint.mapLayerGroups.scenario_built_form_layer.raster.reload();
    },

    renderSelection: function(e) {
        var layer = getActiveLayer();
        if (layer == undefined) {return false}
        var group = getActiveLayerGroup();
        if (group.selection.length > 0) {
            for (var i = 0; i < e.features.length; i++) {
                var f = d3.select(e.features[i].element);
                f.classed("selected", function() {
                    var id = parseInt(this.id.slice(2));
                    if ($.inArray(id, group.selection) == -1) {return false}
                    else {return true}
                })
            }
        }
    },

    selectFeaturesByIdArray: function(selection, array) {
    // takes a d3 selection and classes them as "selected" if they have IDs contained in the array
        selection.classed("selected", function() {
            var id = parseInt(this.id.slice(2));
            if ($.inArray(id, array) == -1) {return false}
            else {return true}
        })
    },

    switchSelection: function(f, event) {
        // a way to refine the selections, whether you are clicking on svg or png tiles
        var layer = getActiveLayerGroup();
        if (layer.raster.visible() === true) {
            rasterSelectionRefinement(f, event, layer);
        }
        if (layer.vector.visible() === true) {
            vectorSelectionRefinement(f, event, layer);
        }
    },

    vectorSelectionRefinement: function(f, event) {
        // this just styles the parcel correctly and adds the element to the selection array stored in the layer
        // we need to send this selection layer to the server before we can run a update_with_selection
        var layer = getActiveLayerGroup();
        var g = d3.select(f.element);

        var id = parseInt(g.node().id.slice(2));
        var selected = g.classed('selected') == true;

        if (selected) {
            var index = selectionArray.indexOf(id);
            layer.selection.splice(index, 1);
        }

        else {
            layer.selection.push(id);
        }

        g.classed("selected", !selected)
    },

    rasterSelectionRefinement: function(event, layer) {
        coord = po.pointLocation(map.mouse)
    }
});
