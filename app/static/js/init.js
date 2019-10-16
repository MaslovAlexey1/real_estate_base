function updateURLParameter(url, param, paramVal) {
	var newAdditionalURL = "";
	var tempArray = url.split("?");
	var baseURL = tempArray[0];
	var additionalURL = tempArray[1];
	var temp = "";
	if (additionalURL) {
		tempArray = additionalURL.split("&");
		for (i = 0; i < tempArray.length; i++) {
			if (tempArray[i].split('=')[0] != param) {
				newAdditionalURL += temp + tempArray[i];
				temp = "&";
			}
		}
	}

	var rows_txt = temp + "" + param + "=" + paramVal;
	return baseURL + "?" + newAdditionalURL + rows_txt;
}

function developSelectChangeValue() {
	//Getting Value
	//var selValue = document.getElementById("singleSelectDD").value;
	var url = window.location.href
	// Developer
	var selObj = document.getElementById("developer");
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, 'dev', selValue);
	// Housing_complex
	var selObj = document.getElementById("housing_complex");
	var selValue = 0;
	url = updateURLParameter(url, 'hc', selValue);
	// House
	var selObj = document.getElementById("house");
	var selValue = 0;
	url = updateURLParameter(url, 'h', selValue);
	// Object type
	var selObj = document.getElementById("object_type");
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, 'ot', selValue);
	// Redirect
	window.location.replace(url);
}

function housingComplexSelectChangeValue() {
	//Getting Value
	//var selValue = document.getElementById("singleSelectDD").value;
	var url = window.location.href
	// Developer
	var selObj = document.getElementById("housing_complex");
	var selValue = selObj.options[selObj.selectedIndex].dataset.dev;
	url = updateURLParameter(url, 'dev', selValue);
	// Housing_complex
	var selObj = document.getElementById("housing_complex");
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, 'hc', selValue);
	// House
	var selObj = document.getElementById("house");
	var selValue = 0;
	url = updateURLParameter(url, 'h', selValue);
	// Object type
	var selObj = document.getElementById("object_type");
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, 'ot', selValue);
	// Redirect
	window.location.replace(url);
}

function houseSelectChangeValue() {
	//Getting Value
	//var selValue = document.getElementById("singleSelectDD").value;
	var url = window.location.href
	// Developer
	var selObj = document.getElementById("house");
	var selValue = selObj.options[selObj.selectedIndex].dataset.dev;
	url = updateURLParameter(url, 'dev', selValue);
	// Housing_complex
	var selObj = document.getElementById("house");
	var selValue = selObj.options[selObj.selectedIndex].dataset.hc;
	url = updateURLParameter(url, 'hc', selValue);
	// House
	var selObj = document.getElementById("house");
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, 'h', selValue);
	// Object type
	var selObj = document.getElementById("object_type");
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, 'ot', selValue);
	// Redirect
	window.location.replace(url);
}

function SelectChangeValue(element_id, url_name) {
	var url = window.location.href
	// is studio
	var selObj = document.getElementById(element_id);
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, url_name, selValue);
	// Redirect
	window.location.replace(url);
}

function SelectChangeValueWithErase(element_id, url_name) {
	var url = window.location.origin + window.location.pathname

	var selObj = document.getElementById(element_id);
	var selValue = selObj.options[selObj.selectedIndex].value;
	url = updateURLParameter(url, url_name, selValue);
	// Redirect
	window.location.replace(url);
}