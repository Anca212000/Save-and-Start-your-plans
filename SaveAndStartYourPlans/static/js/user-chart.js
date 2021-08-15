let labels = ["Plan1", "Plan2", "Plan3", "Plan4", "Plan5", "Plan6"];
let data = [2, 3, 1, 0.5, 0.3, 1.2];

let chartPlans = document.getElementById("circleChart").getContext("2d");

let chart4 = new Chart(chartPlans, {
  type: "pie",
  data: {
    labels: labels,
    datasets: [
      {
        data: data,
        backgroundColor: colors,
      },
    ],
  },
  options: {
    title: {
      text: "See your datagram for plans today",
      display: true,
    },
  },
});
