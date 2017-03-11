function formroute(id){
  var buttonId = id;
  switch (buttonId){
    case 'taillogbtn':
      document.getElementById('dashboardform').action = '/log/tail';
      var lines = prompt("Last x lines to show?","30");
      var isNumber =  /^\d+$/.test(lines);
      if (isNumber === true){
          document.getElementById('dashboardform').action = '/log/tail/'+ lines;
      } else {
          alert('Entry is NOT a number.  Command Canceled!\n');
          document.getElementById('dashboardform').action = '/';
          document.getElementById('dashboardform').method = '';
      };
      break;
    case 'clearlogsbtn':
      var response = confirm("Are you sure you wish to remove ALL Log Files?");
      if (response == true) {
              document.getElementById('dashboardform').action = '/log/clear';
      } else {
              document.getElementById('dashboardform').action = '/';
              document.getElementById('dashboardform').method = '';
      };
      break;
    case 'videocapbtn':
      var time = prompt("Recording length? (in seconds)","60");
      var isNumber =  /^\d+$/.test(time);
      if (isNumber === true){
          document.getElementById('dashboardform').action = '/video/capture/'+ time;
      } else {
          alert('Entry is NOT a number.  Command Canceled!\n');
          document.getElementById('dashboardform').action = '/';
          document.getElementById('dashboardform').method = '';
      };
      break;
    case 'clearvideosbtn':
      var response = confirm("Are you sure you wish to remove ALL Video Files?");
      if (response == true) {
              document.getElementById('dashboardform').action = '/video/clear';
      } else {
              document.getElementById('dashboardform').action = '/';
              document.getElementById('dashboardform').method = '';
      };
      break;
    case 'pcapbtn':
      var time = prompt("Capture length? (in seconds)","60");
      var isNumber =  /^\d+$/.test(time);
      if (isNumber === true){
          document.getElementById('dashboardform').action = '/pcap/start/'+ time;
      } else {
          alert('Entry is NOT a number.  Command Canceled!\n');
          document.getElementById('dashboardform').action = '/';
          document.getElementById('dashboardform').method = '';
      };
      break;
    case 'clearpcapbtn':
      var response = confirm("Are you sure you wish to continue?");
      if (response == true) {
              document.getElementById('dashboardform').action = '/pcap/clear';
      } else {
              document.getElementById('dashboardform').action = '/';
              document.getElementById('dashboardform').method = '';
      };
      break;
    case 'motionstartbtn':
      document.getElementById('dashboardform').action = '/motion/start';
      break;
    case 'motionstopbtn':
      var response = confirm("Are you sure you wish to continue?");
      if (response == true) {
              document.getElementById('dashboardform').action = '/motion/stop';
      } else {
              document.getElementById('dashboardform').action = '/';
              document.getElementById('dashboardform').method = '';
      };
      break;
    case 'uptimebtn':
      document.getElementById('dashboardform').action = '/system/uptime';
      break;
    case 'updatebtn':
      var response = confirm("Are you sure you wish to continue?");
      if (response == true) {
              document.getElementById('dashboardform').action = '/system/update';
      } else {
              document.getElementById('dashboardform').action = '/';
              document.getElementById('dashboardform').method = '';
      };
      break;
    case 'restartbtn':
      var response = confirm("Are you sure you wish to Restart the System?");
      if (response == true) {
              document.getElementById('dashboardform').action = '/system/restart';
      } else {
              document.getElementById('dashboardform').action = '/';
              document.getElementById('dashboardform').method = '';
      };
      break;
    case 'sysshutdownbtn':
      var response = confirm("Are you sure you wish to Shutdown the System?");
      if (response == true) {
              document.getElementById('dashboardform').action = '/system/shutdown';
      } else {
              document.getElementById('dashboardform').action = '/';
              document.getElementById('dashboardform').method = '';
      };
      break;
  }
}
