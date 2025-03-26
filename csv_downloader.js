// Need to download the csv file for each test
// after downloading, edit it to include the motor name and propeller name (create two additional columns)
// Process the throttle column (units: microseconds) and convert into throttle percentage (a way to normalize the data)
// ^ must be done per file rather than to the data in general because some ESCs will use different ranges of PWM signals
// ^ could potentially run SQL queries to normalize each "block" after it has all been compiled, but there could be lots of side effects and leaks
// process each csv file after downloading (using Python)

function download_csv(){
    const csv_download_button = document.querySelector(".btn.btn-secondary.buttons-csv.buttons-html5");
    if (csv_download_button) {
        button.click();
        console.log("CSV button clicked.");
    } else {
        console.log("CSV button not found.");
    }
}









