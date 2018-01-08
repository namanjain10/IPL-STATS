console.log('yes');
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var arr = JSON.parse(this.responseText);
        var name = Object.getOwnPropertyNames(arr[1])
        console.log(name[0]);
        console.log(arr[0].Player_Id);
        console.log(arr[1].Player_Name);
      var str = document.getElementById("player").innerHTML ;
      str += '<table class = "table table-striped table-bordered table-hover">'
        str +=  '<thead><td>Year</td></thead><tbody>'

          for (i=0; i<arr.length; i++) {
          str += '<tr>'
          // for (j=0; j<name.length; j++) {
          str += '<td>' + arr[i].Player_Id + '</td>';
          str += '<td>' + arr[i].Player_Name + '</td>';
          str += '<td>' + arr[i].Player_DOB + '</td>';
          str += '<td>' + arr[i].Batting_Hand + '</td>';
          str += '<td>' + arr[i].Bowling_Skill + '</td>';
          str += '<td>' + arr[i].Country + '</td>';
          str += '<td>' + arr[i].Is_Umpire + '</td>';
          // }
          str += '</tr>'
       }
       str += '</tbody></table>'
     document.getElementById("player").innerHTML = str;  
    }
};
xhttp.open("GET", "http://127.0.0.1:8000/api", true);
xhttp.send();
