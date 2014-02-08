django.jQuery(function($){
    /**
     * jQuery Deserialize plugin
     * @author: Dawid Fatyga
     *
     * Forked from: http://github.com/jakubpawlowicz/jquery.deserialize
     *
    **/

    /* Builtin Array class extension, which converts itself to map */
    Array.prototype.toHash = function(){
    	var map = {}
    	for(var i = 0;i < this.length; i++)
    		map[this[i]] = ''
    	return map
    };

    function hightlight(elt){
        var formerColor = $(elt).css('backgroundColor')
        $(elt).animate({'backgroundColor': '#FAF66C'}, 200, function(){
            $(elt).animate({'backgroundColor': formerColor}, 200, function(){
                $(elt).css({'backgroundColor': formerColor})
            })
        })
    }

    $.fn.deserialize = function(s, options) {
    	var data = s.split("&")

    	options = options || {}
    	attr = options.attribute || "name"

    	if(options.only && options.except)
    		throw "You cannot pass both 'only' and 'except' options"

    	var names = (options.except || []).toHash()
    	var except = true
    	if(options.only){
    		names = options.only.toHash()
    		except = false
    	}

    	callback = options.callback
    	callback_on = options.callback_on || false
    	if(callback_on)
    		callback_on = callback_on.toHash()

        // uncheck everything in form
        $('form :checkbox').attr('checked', false)
        $('form :radio').attr('selected', false)

    	for (var i = 0; i < data.length; i++) {
    		var pair = data[i].split("=")
    		var _name = decodeURIComponent(pair[0])
    		var value = decodeURIComponent(pair[1]).replace(/\+/g, " ")
    		if(except != _name in names){
    		    var input = $("[" + attr + "='" + _name + "']", this)
    		    
    		    if (input.is(':checkbox')){
		            input.attr('checked', value == 'on')
    		    } else if(input.is(':radio')){
    		        input.attr('selected', input.is('[value="'+value+'"]'))
    		    } else if(input.is('textarea')){
                    input.val(value)
                    input.get(0).innerHTML = value
                    if (typeof tinyMCE != 'undefined'){
                        if (tinyMCE.get(input.id)){
                            var editor = tinyMCE.get(input.id)[0]
                            editor.setContent(value)
                            if (value != input.val()){
                                hightlight(editor.contentAreaContainer)
                            }
                        }
                	}
    		    } else {
    		        if (value != input.val()){
    		            hightlight(input)
            			input.val(value)
    		        }
    		    }
    			if(callback && ((!callback_on) || (_name in callback_on))){
    				callback(_name, value)
    			}
    		}
    	}
    }


    $(".saveDraft").parents(':hidden').andSelf().show()
    $(".saveDraft").click(function(e){
        // Redirect form to our own action
        $('form').attr('action', '/draft/save'+window.location.pathname)
    })


    var saved_form = $('form').serialize()
    var draft = null
    var hiddenLoadDraft = $(".loadDraft").parents(':hidden').andSelf()
    var hiddenReturnCurrent = $(".returnCurrent").parents(':hidden').andSelf()
    var hiddenDiscardDraft = $(".discardDraft").parents(':hidden').andSelf()
    $.get('/draft/load'+window.location.pathname, function(data){
        if (data){
            draft = data
        }
        if(draft){
            hiddenLoadDraft.show()
            $(".loadDraft").click(function(e){
                e.preventDefault()
                hiddenLoadDraft.hide()
                hiddenReturnCurrent.show()
                hiddenDiscardDraft.show()
                $('form').deserialize(draft, {except: ["csrfmiddlewaretoken"]})
            })
        }
    })
    
    

    $(".returnCurrent").click(function(e){
        e.preventDefault()
        hiddenLoadDraft.show()
        hiddenReturnCurrent.hide()
        hiddenDiscardDraft.hide()
        $('form').deserialize(saved_form, {except: ["csrfmiddlewaretoken"]})
    })    

    $(".discardDraft").click(function(e){
        e.preventDefault()
        $('form').attr('action', '/draft/discard'+window.location.pathname)
        $('form').get(0).submit()
    })    
})
