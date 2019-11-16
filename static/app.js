// Call python get request 
function postData(input) {
	 $(document).ready(async function() {	
	  await $.ajax({
	        type: "GET",
	        url: "/proxy/"+input,
	        data:{"var":input},
	        success: changePopupText
	    });
	});
}

// Change the text in modal popup
function changePopupText(response) {
    document.getElementById("test").innerHTML = response;
    document.getElementById("myModal").style.display = "block";
}

// Call postData when a word is clicked
function wordClicked(input) {
	var text = $(input).text()
    postData(text);
}

// Close modal popup when outside of modal is clicked
window.onclick = function(event) {
  if (event.target == document.getElementById("myModal")) {
    document.getElementById("myModal").style.display = "none";
  }
}