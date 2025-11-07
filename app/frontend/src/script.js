const API_BASE = "/api";
const tableBody = document.getElementById("tableBody");
const sourceFilter = document.getElementById("sourceFilter");
const cveFilter = document.getElementById("cveFilter");

let allBulletins = [];

async function fetchBulletins(source = "all") {
	tableBody.innerHTML = `<tr><td colspan="6" class="text-center p-4 text-gray-500">Ładowanie...</td></tr>`;
	let url = `${API_BASE}/bulletins`;
	if (source !== "all") {
		url += `?product=${source}`;
	}

	try {
		const res = await fetch(url);
		const data = await res.json();
		allBulletins = data.bulletins || [];
		renderTable(allBulletins);
	} catch (err) {
		tableBody.innerHTML = `<tr><td colspan="6" class="text-center text-red-500">Error while loading data...</td></tr>`;
	}
}

function renderTable(data) {
	if (!data.length) {
		tableBody.innerHTML = `<tr><td colspan="6" class="text-center p-4 text-gray-500">No matching results.</td></tr>`;
		return;
	}

	const rows = data.map(
		b => `
      <tr class="border-b hover:bg-gray-50">
        <td class="p-2">${extractSource(b.url)}</td>
        <td class="p-2 font-semibold"><a href="${
			b.url
		}" target="_blank" class="text-blue-600 hover:underline">${
			b.id
		}</a></td>
        <td class="p-2">${b.cves.join(", ")}</td>
        <td class="p-2">${b.managed}</td>
        <td class="p-2">${b.summary}</td>
      </tr>
    `
	);
	tableBody.innerHTML = rows.join("");
}

function extractSource(url) {
	if (url.includes("kubernetes-engine")) return "GKE";
	if (url.includes("compute")) return "Compute Engine";
	if (url.includes("sql")) return "Cloud SQL";
	if (url.includes("service-mesh")) return "Service Mesh";
	return "-";
}

// Eventy filtrowania
sourceFilter.addEventListener("change", e => {
	fetchBulletins(e.target.value);
});

cveFilter.addEventListener("input", e => {
	const value = e.target.value.toLowerCase();
	if (!value) {
		renderTable(allBulletins);
		return;
	}
	const filtered = allBulletins.filter(b =>
		b.cves.some(cve => cve.toLowerCase().includes(value))
	);
	renderTable(filtered);
});

fetchBulletins();
