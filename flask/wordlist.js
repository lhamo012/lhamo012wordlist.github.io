// for drop down options for max and min
function generateOptions() {
	var select = document.getElementsByClassName('len');
	console.log(select.length);
	for(var j=0; j<select.length;j++){
		for(var i = 3; i <= 10; i++) {
   	 		var el = document.createElement('option');
    		el.textContent = i;
    		el.value = i;
    		el.innerHTML = i;
    		select[j].appendChild(el);
		}
	}
}

function filterWords(word) {
	var s = document.getElementById('select');
	var selectlength = s.options[s.selectedIndex].text;

	return word.length == selectlength;
}

function filterPattern(word) {
	document.getElementById("selecttext").pattern = document.getElementById("selecttext").value
	var x = document.getElementById("selecttext").pattern;
	var pattern = new RegExp(x);
	console.log("pattern is: "+pattern);
	console.log(word);
	console.log("is matching: " + word.match(pattern));
	return pattern.test(word);
}

function submit() {
	fetch('test.txt')
		.then((res)=>res.text())
		.then((data)=> {
			var result = data.split("\n");
			// sort alphabetically
			result.sort();
			// sort into ascending order 
			result.sort(function(a, b){ return a.length - b.length});
			var r = result.filter(filterPattern);
			console.log(r);
			if (document.getElementById('select').selectedIndex == 0){
				document.getElementById('output').innerHTML = r;
			}else {
				document.getElementById('output').innerHTML = result.filter(filterWords);
			}
		}) 
		.catch((err) => console.log(err))
}
window.onload = function() { generateOptions(); }
