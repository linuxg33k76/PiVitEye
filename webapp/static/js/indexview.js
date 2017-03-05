function formroute(id){
  var buttonId = id;
  switch (buttonId){
    case 'taillogbtn':
      document.getElementById('dashboardform').action = '/log/tail';
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
      document.getElementById('dashboardform').action = '/video/capture';
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
      document.getElementById('dashboardform').action = '/pcap/start';
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
  }
}
