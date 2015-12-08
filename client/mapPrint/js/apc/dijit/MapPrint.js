define([
	"dijit/_WidgetBase",
	"dojo/topic",
	"dojo/Evented",
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/_base/array",
	"dojo/parser",
	"dijit/_TemplatedMixin",
	"dijit/_WidgetsInTemplateMixin", 

    "dojo/on",
	"dojo/dom",
    "dojo/dom-construct",
    "dojo/dom-class",
    "dojo/dom-style",
    "dojo/ready",
	
	"dojo/store/Memory",
	"dijit/form/FilteringSelect", 

    "dojo/text!./templates/MapPrint.html", // template html
	
	"xstyle/css!./css/MapPrint.css" // widget style 
], function(
	_WidgetBase,
    topic, Evented, declare, lang, array, 
    parser, _TemplatedMixin, _WidgetsInTemplateMixin,
    on, dom, domConstruct, domClass, domStyle, ready, 
	Memory, FilteringSelect,  
    dijitTemplate
) {

    var mapPrint = declare("MapPrint", 
			[_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin, Evented], {

		templateString: dijitTemplate,
		baseClass: "MapPrint", // css base class

        options: {
            map: null, // required
            title: "Map Print",
			sizeOptions: [
				{name: "8.5x11", value: [8.5, 11]},
				{name: "8.5x14", value: [8.5, 14]},
				{name: "11x14", value: [11, 14]},
				{name: "17x22", value: [17, 22]},
				{name: "22x34", value: [22, 34]},
				{name: "34x44", value: [34, 44]}
			], 
			orientationOptions: [
				{name: "Portrait", value: "portrait"}, 
				{name: "Landscape", value: "landscape"}
			], 
			formatOptions: [
				{name: "PDF", value: "pdf"},
				{name: "JPG", value: "jpg"},
				{name: "PNG", value: "png"}
			], 
			dpiOptions: [
				{name: "96", value: 96},
				{name: "150", value: 150},
				{name: "300", value: 300},
				{name: "600", value: 600}
			], 
            visible: true
        }, 

        /* ------------------ */
        /* Private Variables  */
        /* ------------------ */


        /* ---------------------- */
        /* Public Class Functions */
        /* ---------------------- */
        
        constructor: function(options, srcRefNode) {
            // mix in settings and defaults
            declare.safeMixin(this.options, options);
            // properties
            this.set("map", this.options.map);
            this.set("title", this.options.title);
            this.set("sizeOptions", this.options.sizeOptions); 
			this.set("orientationOptions", this.options.orientationOptions); 
			this.set("formatOptions", this.options.formatOptions); 
			this.set("dpiOptions", this.options.dpiOptions); 
            this.set("visible", this.options.visible);
            // listeners
            this.watch("visible", this._visible);
        },

        startup: function () {
            // map not defined
            if (!this.map) {
              this.destroy();
              console.log('SearchData::map required');
            }
            // when map is loaded
            if (this.map.loaded) {
              this._init();
            } else {
              on(this.map, "load", lang.hitch(this, function () {
                this._init();
              }));
            }
        },

        // connections/subscriptions will be cleaned up during the destroy() lifecycle phase
        destroy: function () {
            this.inherited(arguments); 
        }, 

        /* ------------------------- */
        /* Private Utility Functions */
        /* ------------------------- */
        
        _init: function () {
			// populate the combobox stores
			var firstOption; 
			// - size
			this._sizeComboBox.set("store", new Memory({
				data: {
					identifier: 'value',
					label: "name",
					items: this.sizeOptions
				}
			})); 
			// - orientation
			this._orientationComboBox.set("store", new Memory({
				data: {
					identifier: 'value',
					label: "name",
					items: this.orientationOptions
				}
			})); 
			// - format
			this._formatComboBox.set("store", new Memory({
				data: {
					identifier: 'value',
					label: "name",
					items: this.formatOptions
				}
			})); 
			// - DPI
			this._dpiComboBox.set("store", new Memory({
				data: {
					identifier: 'value',
					label: "name",
					items: this.dpiOptions
				}
			})); 
			//
            this._visible();
            this.set("loaded", true);
            this.emit("load", {});
        },

        _visible: function () {
            if (this.get("visible")) {
                domStyle.set(this.domNode, 'display', 'block');
            } else {
                domStyle.set(this.domNode, 'display', 'none');
            }
        },

        showMessage: function (message) {
            if (message) {
                /* limit the message size */
                message = message.substr(0, 100); 
            }
            this._status.innerHTML = message;
        }, 
		
		_doPrint: function() {
			console.log("Gather the input");
			// - size
			var selectedSize = this._sizeComboBox.value; 
			console.log("size = " + selectedSize);
			// - orientation
			var selectedOrientation = this._orientationComboBox.value; 
			console.log("orientation = " + selectedOrientation);
			// - format
			var selectedFormat = this._formatComboBox.value; 
			console.log("format = " + selectedFormat);
			// - dpi
			var selectedDpi = this._dpiComboBox.value; 
			console.log("DPI = " + selectedDpi);
			// - title 
			var titleInput = this._titleInput.value; 
			console.log("title = " + titleInput);
			
		}, 
		
		_printFailed: function(err){
			console.log("Error in Print: " + err.message);
			var errMsg = (err && err.message && err.message.length > 0)?err.message:""; 
			this.showMessage("Failed to Print:" + errMsg);
		},
		
		_openPrintOut: function(data) {
			console.log("PrintOut ready: " + data["Url"]);
			window.open(data["Url"]); 
			this.showMessage("");
		}

        /* ---------------------- */
        /* Private Event Handlers */
        /* ---------------------- */
		

    });

    ready(function(){
        console.log("Widget MapPrint is ready!");
    });	

    return mapPrint;
                    
});