(function($){"use strict";var Wysihtml5=function(options){this.init('wysihtml5',options,Wysihtml5.defaults);this.options.wysihtml5=$.extend({},Wysihtml5.defaults.wysihtml5,options.wysihtml5);};$.fn.editableutils.inherit(Wysihtml5,$.fn.editabletypes.abstractinput);$.extend(Wysihtml5.prototype,{render:function(){var deferred=$.Deferred(),msieOld;this.$input.attr('id','textarea_'+(new Date()).getTime());this.setClass();this.setAttr('placeholder');$.extend(this.options.wysihtml5,{events:{load:function(){deferred.resolve();}}});this.$input.wysihtml5(this.options.wysihtml5);msieOld=/msie\s*(8|7|6)/.test(navigator.userAgent.toLowerCase());if(msieOld){this.$input.before('<br><br>');}
return deferred.promise();},value2html:function(value,element){$(element).html(value);},html2value:function(html){return html;},value2input:function(value){this.$input.data("wysihtml5").editor.setValue(value,true);},activate:function(){this.$input.data("wysihtml5").editor.focus();}});Wysihtml5.defaults=$.extend({},$.fn.editabletypes.abstractinput.defaults,{tpl:'<textarea></textarea>',inputclass:'editable-wysihtml5',placeholder:null,wysihtml5:{stylesheets:false}});$.fn.editabletypes.wysihtml5=Wysihtml5;}(window.jQuery));