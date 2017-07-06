function formroute(id){
    var buttonId = id;
    switch (buttonId){
        case 'taillog_btn':
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
        case 'clearlogs_btn':
            var response = confirm("Are you sure you wish to remove ALL Log Files?");
            if (response == true) {
                  document.getElementById('dashboardform').action = '/log/clear';
            } else {
                  document.getElementById('dashboardform').action = '/';
                  document.getElementById('dashboardform').method = '';
            };
            break;
        case 'videocap_btn':
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
        case 'clearvideos_btn':
            var response = confirm("Are you sure you wish to remove ALL Video Files?");
            if (response == true) {
                  document.getElementById('dashboardform').action = '/video/clear';
            } else {
                  document.getElementById('dashboardform').action = '/';
                  document.getElementById('dashboardform').method = '';
            };
            break;
        case 'pcap_btn':
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
        case 'clearpcap_btn':
            var response = confirm("Are you sure you wish to continue?");
            if (response == true) {
                  document.getElementById('dashboardform').action = '/pcap/clear';
            } else {
                  document.getElementById('dashboardform').action = '/';
                  document.getElementById('dashboardform').method = '';
            };
            break;
        case 'speedtest_btn':
            document.getElementById('dashboardform').action = '/speedtest/start';
            break;
        case 'speedtestlog_btn':
            document.getElementById('dashboardform').action = '/speedtest/entries';
            var lines = prompt("Last x lines to show?","30");
            var isNumber =  /^\d+$/.test(lines);
            if (isNumber === true){
                document.getElementById('dashboardform').action = '/speedtest/entries/'+ lines;
            } else {
                alert('Entry is NOT a number.  Command Canceled!\n');
                document.getElementById('dashboardform').action = '/';
                document.getElementById('dashboardform').method = '';
            };
            break;
        case 'motionstart_btn':
            document.getElementById('dashboardform').action = '/motion/start';
            break;
        case 'motionstop_btn':
            var response = confirm("Are you sure you wish to continue?");
            if (response == true) {
                  document.getElementById('dashboardform').action = '/motion/stop';
            } else {
                  document.getElementById('dashboardform').action = '/';
                  document.getElementById('dashboardform').method = '';
            };
            break;
        case 'uptime_btn':
            document.getElementById('dashboardform').action = '/system/uptime';
            break;
        case 'update_btn':
            var response = confirm("Are you sure you wish to continue?");
            if (response == true) {
                  document.getElementById('dashboardform').action = '/system/update';
            } else {
                  document.getElementById('dashboardform').action = '/';
                  document.getElementById('dashboardform').method = '';
            };
            break;
        case 'restart_btn':
            var response = confirm("Are you sure you wish to Restart the System?");
            if (response == true) {
                  document.getElementById('dashboardform').action = '/system/restart';
            } else {
                  document.getElementById('dashboardform').action = '/';
                  document.getElementById('dashboardform').method = '';
            };
            break;
        case 'sysshutdown_btn':
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
