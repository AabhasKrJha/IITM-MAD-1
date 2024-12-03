import { statesAndCities } from '../statesAndCities.js';

const stateSelect = document.getElementById("state-select");
const citySelect = document.getElementById("city-select");

for (const state in statesAndCities) {
    const option = document.createElement("option");
    option.value = state;
    option.textContent = state;
    stateSelect.appendChild(option);
}

stateSelect.addEventListener("change", function () {
    const selectedState = this.value;
    const cities = statesAndCities[selectedState];

    citySelect.innerHTML = '<option value="" disabled selected>Select a city</option>';

    if (cities) {
        cities.forEach(city => {
            const option = document.createElement("option");
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });

        citySelect.disabled = false;
    } else {
        citySelect.disabled = true;
    }
});
