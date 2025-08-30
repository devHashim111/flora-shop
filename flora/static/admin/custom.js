document.addEventListener("DOMContentLoaded", function() {
    let ctx = document.getElementById("orderChart").getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            datasets: [{
                label: "Orders",
                data: [50, 100, 150, 200, 250, 300],
                backgroundColor: "rgba(54, 162, 235, 0.6)",
            }]
        }
    });
});
