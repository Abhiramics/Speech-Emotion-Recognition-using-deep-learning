$("#voice-input").change(function () {
  $("#predict-btn").show();
});



$("#predict-btn").click(() => {
  let myForm = document.getElementById('upload-form');
  let formData = new FormData(myForm);
  // let uploadedVoice = new FormData($("#upload-form")[0]);
  console.log(formData)
  $.ajax({
    type: "POST",
    url: "/predict",
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    async: true,
    success: function (data) {
      // Get and display the result
console.log(data)
let res=data['pred'];
$('#result').html('<h2 style="color:white;">'+'Prediction is '+res+'</h2>');
        }
      }
     
  );

});

