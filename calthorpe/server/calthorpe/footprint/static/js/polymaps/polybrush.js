/*
 Copyright (c) 2012 Geoffrey T. Bell

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
(function(d3) {
    d3.svg.polybrush = function() {
        var dispatch = d3.dispatch("brushstart", "brush", "brushend"),
            x = null,
            y = null,
            extent = [],
            firstClick = true,
            firstTime = true,
            wasDragged = false,
            origin = null,
            line = d3.svg.line()
                .x(function(d) {
                    return d[0];
                })
                .y(function(d) {
                    return d[1];
                });
        var brush = function(g) {
            g.each(function() {
                var bg, e, fg;
                g = d3.select(this);
                bg = g.selectAll(".background").data([0]);
                fg = g.selectAll(".extent").data([extent]);
                g.style("pointer-events", "all").on("click.brush", addAnchor);
                bg.enter().append("rect").attr("class", "background").style("visibility", "hidden").style("cursor", "crosshair");
                fg.enter().append("path").attr("class", "extent").classed("polybrush", true).style("cursor", "move");
                if (x) {
                    e = scaleExtent(x.range());
                    bg.attr("x", e[0]).attr("width", e[1] - e[0]);
                }
                if (y) {
                    e = scaleExtent(y.range());
                    bg.attr("y", e[0]).attr("height", e[1] - e[0]);
                }
            });
        };
        var drawPath = function() {
            return d3.selectAll(".polybrush").attr("d", function(d) {
                return line(d) + "Z";
            });
        };
        var scaleExtent = function(domain) {
            var start, stop;
            start = domain[0];
            stop = domain[domain.length - 1];
            if (start < stop) {
                return [start, stop];
            } else {
                return [stop, start];
            }
        };
        var withinBounds = function(point) {
            var rangeX, rangeY, _x, _y;
            rangeX = scaleExtent(x.range());
            rangeY = scaleExtent(y.range());
            _x = Math.max(rangeX[0], Math.min(rangeX[1], point[0]));
            _y = Math.max(rangeY[0], Math.min(rangeY[1], point[1]));
            return point[0] === _x && point[1] === _y;
        };
        var moveAnchor = function(target) {
            var moved, point;
            point = d3.mouse(target);
            if (firstTime) {
                extent.push(point);
                firstTime = false;
            } else {
                if (withinBounds(point)) {
                    extent.splice(extent.length - 1, 1, point);
                }
                drawPath();
                dispatch.brush();
            }
        };
        var closePath = function() {
            var w;
            w = d3.select(window);
            w.on("dblclick.brush", null).on("mousemove.brush", null);
            firstClick = true;
            if (extent.length === 2 && extent[0][0] === extent[1][0] && extent[0][1] === extent[1][1]) {
                extent.splice(0, extent.length);
            }
            d3.select(".extent").on("mousedown.brush", moveExtent);
            return dispatch.brushend();
        };
        var addAnchor = function() {
            var g, w,
                _this = this;
            g = d3.select(this);
            w = d3.select(window);
            firstTime = true;
            if (wasDragged) {
                wasDragged = false;
                return;
            }
            if (firstClick) {
                extent.splice(0, extent.length);
                firstClick = false;
                d3.select(".extent").on("mousedown.brush", null);
                w.on("mousemove.brush", function() {
                    return moveAnchor(_this);
                }).on("dblclick.brush", closePath);
                dispatch.brushstart();
            }
            if (extent.length > 1) {
                extent.pop();
            }
            extent.push(d3.mouse(this));
            return drawPath();
        };
        var dragExtent = function(target) {
            var checkBounds, fail, p, point, scaleX, scaleY, updateExtentPoint, _i, _j, _len, _len1;
            point = d3.mouse(target);
            scaleX = point[0] - origin[0];
            scaleY = point[1] - origin[1];
            fail = false;
            origin = point;
            updateExtentPoint = function(p) {
                p[0] += scaleX;
                p[1] += scaleY;
            };
            for (_i = 0, _len = extent.length; _i < _len; _i++) {
                p = extent[_i];
                updateExtentPoint(p);
            }
            checkBounds = function(p) {
                if (!withinBounds(p)) {
                    fail = true;
                }
                return fail;
            };
            for (_j = 0, _len1 = extent.length; _j < _len1; _j++) {
                p = extent[_j];
                checkBounds(p);
            }
            if (fail) {
                return;
            }
            drawPath();
            return dispatch.brush({
                mode: "move"
            });
        };
        var dragStop = function() {
            var w;
            w = d3.select(window);
            w.on("mousemove.brush", null).on("mouseup.brush", null);
            wasDragged = true;
            return dispatch.brushend();
        };
        var moveExtent = function() {
            var _this = this;
            d3.event.stopPropagation();
            d3.event.preventDefault();
            if (firstClick && !brush.empty()) {
                d3.select(window).on("mousemove.brush", function() {
                    return dragExtent(_this);
                }).on("mouseup.brush", dragStop);
                origin = d3.mouse(this);
            }
        };
        brush.isWithinExtent = function(x, y) {
            var i, j, len, p1, p2, ret, _i, _len;
            len = extent.length;
            j = len - 1;
            ret = false;
            for (i = _i = 0, _len = extent.length; _i < _len; i = ++_i) {
                p1 = extent[i];
                p2 = extent[j];
                if ((p1[1] > y) !== (p2[1] > y) && x < (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1]) + p1[0]) {
                    ret = !ret;
                }
                j = i;
            }
            return ret;
        };
        brush.x = function(z) {
            if (!arguments.length) {
                return x;
            }
            x = z;
            return brush;
        };
        brush.y = function(z) {
            if (!arguments.length) {
                return y;
            }
            y = z;
            return brush;
        };
        brush.extent = function(z) {
            if (!arguments.length) {
                return extent;
            }
            extent = z;
            return brush;
        };
        brush.clear = function() {
            extent.splice(0, extent.length);
            return brush;
        };
        brush.empty = function() {
            return extent.length === 0;
        };

        d3.rebind(brush, dispatch, "on");

        return brush;
    };
})(d3);